# Copyright 2019 VentorTech OU
# License OPL-1.0 or later.

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


SECURITY_GROUP = 'printnode_base.printnode_security_group_user'


class PrintNodeScenario(models.Model):
    """
    Scenarios to print reports
    """
    _name = 'printnode.scenario'
    _description = 'PrintNode Scenarios'

    _rec_name = 'report_id'

    action = fields.Many2one(
        'printnode.scenario.action',
        string='Print Scenario Action',
        required=True,
        help="""Choose a print action to listen""",
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help="""Activate or Deactivate the print scenario.
                If no active then move to the status \'archive\'.
                Still can by found using filters button""",
    )

    description = fields.Char(
        string='Description',
        size=200,
        help="""Text field for notes and memo.""",
    )

    domain = fields.Text(
        string='Domain',
        default='[]',
    )

    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        related='action.model_id',
    )

    model = fields.Char(
        string='Related Document Model',
        related='model_id.model',
    )

    number_of_copies = fields.Integer(string="Number of Copies", default=1)

    report_id = fields.Many2one(
        'ir.actions.report',
        string='Report',
        required=True,
        # compute=_get_reports,
        help="""Choose a report that will be printed""",
    )

    printer_id = fields.Many2one(
        'printnode.printer',
        string='Printer',
    )

    @api.constrains('number_of_copies')
    def _check_number_of_copies(self):
        for record in self:
            if record.number_of_copies < 1:
                raise ValidationError(_("Number of Copies can't be less than 1"))

    def edit_domain(self):
        domain_editor = self.env.ref(
            'printnode_base.printnode_scenario_domain_editor',
            raise_if_not_found=False,
        )
        action = {
            'name': _('Domain Editor'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'printnode.scenario',
            'res_id': self.id,
            'view_id': domain_editor.id,
            'target': 'self',
        }
        return action

    def print_reports(self, action, model_id, ids_list):
        """
        Find all scenarios and print reports for each of them.

        Returns True when at least a single scenario found. In other cases returns False.
        """
        user = self.env.user
        if (
            not user.has_group(SECURITY_GROUP) or
            not user.company_id.printnode_enabled or
            not user.printnode_enabled
        ):
            return False

        scenarios = self.search([
            ('active', '=', True),
            ('action.code', '=', action),
            ('model_id', '=', model_id),  # Left to avoid printing reports for wrong models
        ])

        for scenario in scenarios:
            objects = scenario._apply_domain(ids_list)
            if objects.exists():
                printer = scenario._get_printer()
                printer.printnode_print(
                    scenario.report_id,
                    objects,
                    copies=scenario.number_of_copies)

                return True

        # No scenarios found
        return False

    def _apply_domain(self, ids_list):
        """
        Get objects by IDs with applied domain
        """
        self.ensure_one()

        if self.domain == '[]':
            return self.env[self.model_id.model].browse(ids_list)
        return self.env[self.model_id.model].search(
            expression.AND([[('id', 'in', ids_list)], eval(self.domain)])
        )

    def _get_printer(self):
        """
        Return printer to use for current scenario or raise exception
        when printer cannot be selected
        """
        self.ensure_one()

        user = self.env.user
        external_printer_id = user._get_report_printer(self.report_id.id)
        printer = self.printer_id or external_printer_id

        if not printer:
            raise UserError(_(
                'Neither on scenario level, no on user rules level, no on user level, '
                'no on company level printer is defined for report "%s". '
                'Please, define it.' % self.report_id.name
            ))
        return printer


class PrintNodeScenarioAction(models.Model):
    """ Action for scenarios
    """
    _name = 'printnode.scenario.action'
    _description = 'PrintNode Scenario Action'

    name = fields.Char(
        string='Name',
        size=64,
        required=True,
    )

    code = fields.Char(
        string='Code',
        size=64,
        required=True,
    )

    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
    )


class PrintNodeScenarioMixin(models.AbstractModel):
    _name = 'printnode.scenario.mixin'
    _description = 'Abstract scenario printing mixin'

    def print_scenarios(self, action, ids_list=[]):
        """
        Find all scenarios for current model and print reports.

        Returns True when something printed or False in other cases.
        """
        return self.env['printnode.scenario'].print_reports(
            action=action, model_id=self._name, ids_list=ids_list or self.mapped('id'))
