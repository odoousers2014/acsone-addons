# -*- coding: utf-8 -*-
##############################################################################
#
# Author: Stéphane Bidoul
# Copyright (c) 2012 Acsone SA/NV (http://www.acsone.eu)
# All Right Reserved
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv


class account_analytic_account(osv.Model):
    _inherit = 'account.analytic.account'

    _columns = {
        'project_id': fields.many2one('project.project', 'Project',
                                      ondelete='set null'),
    }

    def init(self, cr):
        '''
        Initialize the project_id field in case the module is
        installed when projects already exist
        '''
        cr.execute("""
            update account_analytic_account
                set project_id = (select id
                    from project_project where
                    analytic_account_id = account_analytic_account.id)
        """)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default['project_id'] = False
        return super(account_analytic_account, self).copy(
            cr, uid, id, default, context=context)


class project_project(osv.Model):
    _inherit = 'project.project'

    def create(self, cr, uid, vals, context=None):
        project_id = super(project_project, self).create(
            cr, uid, vals, context=context)
        project = self.browse(cr, uid, project_id, context=context)
        analytic_account_obj = self.pool.get('account.analytic.account')
        analytic_account_obj.write(
            cr, SUPERUSER_ID, [project.analytic_account_id.id],
            {'project_id': project_id}, context=context)
        return project_id
