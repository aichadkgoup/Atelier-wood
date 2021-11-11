odoo.define('theme_prime.product_comparison', function (require) {
"use strict";

require('website_sale_comparison.comparison');
var publicWidget = require('web.public.widget');

publicWidget.registry.ProductComparison.include({
    // change selector
    selector: '#wrap, .oe_website_sale:not(.tp-product-quick-view-layout):not(.d_website_sale)',
    // don't append to quick_view dialog
    events: _.extend({
        'click .d_product_comparison': '_onClickCompareBtn',
    }, publicWidget.registry.ProductComparison.prototype.events),

    /**
     * @override
     */
    start: function () {
        let defs = [];

        // Right now we are calling super if #wrap contains .droggol_product_snippet
        // For V15 we only call super if wishlist feature is enabled for snippet.

        // var comparisonEnabled = false;
        // var $snippets = this.$('.droggol_product_snippet[data-user-params]');
        // _.each($snippets, function (snippet) {
        //     var $snippet = $(snippet);
        //     var userParams = $snippet.attr('data-user-params');
        //     userParams = userParams ? JSON.parse(userParams) : false;
        //     if (userParams && userParams.comparison) {
        //         comparisonEnabled = true;
        //     }
        // });
        if (this.$('.droggol_product_snippet').length || this.$target.hasClass('oe_website_sale') || this.$('.oe_website_sale').length) {
            defs.push(this._super.apply(this, arguments));
        }
        return Promise.all(defs);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
    _onClickCompareBtn: function (ev) {
        if (this.productComparison.comparelist_product_ids.length < this.productComparison.product_compare_limit) {
            this.productComparison._addNewProducts(parseInt($(ev.currentTarget).get(0).dataset.productProductId));
        } else {
            this.productComparison.$el.find('.o_comparelist_limit_warning').show();
            $('#comparelist .o_product_panel_header').popover('show');
        }
    },
});
});
