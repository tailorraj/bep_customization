# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.accounts.report.non_billed_report import get_ordered_to_be_billed_data

def execute(filters=None):
	columns = get_column()
	# args = get_args()
	# data = get_ordered_to_be_billed_data(args)
	data = get_data()
	return columns, data

def get_column():
	return [
		_("Sales Order") + ":Link/Sales Order:120", _("Status") + "::120", _("Date") + ":Date:100",
		_("Suplier") + ":Link/Customer:120", _("Customer Name") + "::120",
		_("Project") + ":Link/Project:120", _("Item Code") + ":Link/Item:120",
		_("Amount") + ":Currency:100", _("Billed Amount") + ":Currency:100", _("Pending Amount") + ":Currency:100",
		_("Item Name") + "::120", _("Description") + "::120", _("Company") + ":Link/Company:120",
	]

def get_args():
	return {'doctype': 'Sales Order', 'party': 'customer',
		'date': 'transaction_date', 'order': 'transaction_date', 'order_by': 'asc'}

def get_data():
	data = frappe.db.sql("""
		Select
			`tabSales Order`.name as 'sales_order', `tabSales Order`.transaction_date as date, `tabSales Order`.status,
			`tabSales Order`.customer as suplier, `tabSales Order`.customer_name,
			`tabSales Order Item`.item_code,
			`tabSales Order Item`.base_amount as amount,
			(`tabSales Order Item`.billed_amt * ifnull(`tabSales Order`.conversion_rate, 1)) as billed_amount,
			(`tabSales Order Item`.base_rate * ifnull(`tabSales Order Item`.returned_qty, 0)),
			(`tabSales Order Item`.base_amount - (`tabSales Order Item`.billed_amt * ifnull(`tabSales Order`.conversion_rate, 1)) -	(`tabSales Order Item`.base_rate * ifnull(`tabSales Order Item`.returned_qty, 0))) as pending_amount,
			`tabSales Order Item`.item_name, `tabSales Order Item`.description,
			project, `tabSales Order`.company
		from
			`tabSales Order`, `tabSales Order Item`
		where
			`tabSales Order`.name = `tabSales Order Item`.parent and `tabSales Order`.docstatus = 1
			and `tabSales Order`.status not in ('Closed', 'Completed')
			and `tabSales Order Item`.amount > 0
			and (`tabSales Order Item`.base_amount -
			round(`tabSales Order Item`.billed_amt * ifnull(`tabSales Order`.conversion_rate, 1), 2) -
			(`tabSales Order Item`.base_rate * ifnull(`tabSales Order Item`.returned_qty, 0))) > 0
		order by
			`tabSales Order`.transaction_date asc
	""", as_dict = True)

	return data