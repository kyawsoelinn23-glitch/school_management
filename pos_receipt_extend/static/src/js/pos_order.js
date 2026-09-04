/** @odoo-module */
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import  { patch } from "@web/core/utils/patch";


patch(PosOrder.prototype, {
    get loyaltyPoints() {
        // console.log('loyaltyPoints', this.priceIncl);
        return Math.round(this.priceIncl/10).toFixed(2);
    },
});

