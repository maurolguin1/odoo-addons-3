# -*- coding: utf8 -*-
#
# Copyright (C) 2014 NDP Systèmes (<http://www.ndp-systemes.fr>).
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

from openerp import fields, models, api

class stock_split_only_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.one
    def do_split_only(self):
        self.with_context(do_only_split=True).do_detailed_transfer()


class stock_split_picking(models.Model):
    _inherit = 'stock.picking'

    @api.one
    def action_split_from_ui(self):
        """ called when button 'done' is pushed in the barcode scanner UI """
        #write qty_done into field product_qty for every package_operation before doing the transfer
        for operation in self.pack_operation_ids:
            operation.write({'product_qty': operation.qty_done})
        self.do_split()