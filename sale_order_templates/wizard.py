# -*- coding: utf8 -*-
#
#    Copyright (C) 2016 NDP Systèmes (<http://www.ndp-systemes.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from openerp import models, fields, api, _


class SaleOrderTemplateGeneration(models.TransientModel):
    _name = 'sale.order.template.generation'

    template_id = fields.Many2one('sale.order', string="Sale order template")
    partner_ids = fields.Many2many('res.partner', string="Partners", required=True)

    @api.multi
    def generate_sale_orders(self):
        self.ensure_one()
        new_sale_orders = []
        for partner in self.partner_ids:
            new_sale_order = self.template_id.copy({
                'partner_id': partner.id,
                'is_template': False,
                'template_name': False,
                'created_from_template_id': self.template_id.id,
                'user_id': self.env.user.id
            })
            new_sale_orders += [new_sale_order]
        if len(new_sale_orders) == 1:
            return {
                'name': _("Sale order generated from template %s") % self.template_id.display_name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order',
                'context': self.env.context,
                'res_id': new_sale_order.id,
                'flags': {'form': {'options': {'mode': 'edit'}}}
            }
        elif len(new_sale_orders) > 1:
            return {
                'name': _("Sale orders generated from template %s") % self.template_id.display_name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': self.env.context,
                'domain': [('id', 'in', [order.id for order in new_sale_orders])]
            }
