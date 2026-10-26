import importlib

import frappe
from frappe import _

# The main report's folder name contains "&", so it cannot be used in a plain import statement.
MAIN_REPORT = (
    "zatca_erpgulf.zatca_erpgulf.report."
    "vat_report_zatca_on_sales_&_purchase.vat_report_zatca_on_sales_&_purchase"
)

# category label (as shown in the main report) -> (invoice doctype, key in the main report's totals)
CATEGORIES = {
    "Standard rated sales": ("Sales Invoice", "Standard"),
    "Private Healthcare / Private Education sales to citizens": ("Sales Invoice", "HealthcareEdu"),
    "Zero rated domestic sales": ("Sales Invoice", "Zero Rated"),
    "Exports": ("Sales Invoice", "Exports"),
    "Exempt sales": ("Sales Invoice", "Exempt"),
    "Standard rated domestic purchases": ("Purchase Invoice", "Standard"),
    "Imports subject to VAT paid at customs": ("Purchase Invoice", "ImportsCustoms"),
    "Zero rated purchases": ("Purchase Invoice", "Zero Rated"),
    "Exempt purchases": ("Purchase Invoice", "Exempt"),
}

# The main report always shows 0 VAT for these categories
ZERO_VAT_CATEGORIES = {
    "Zero rated domestic sales",
    "Exempt sales",
    "Zero rated purchases",
    "Exempt purchases",
}

NUMERIC_FIELDS = ["amount_without_vat", "amount", "adjustment_without_vat", "adjustment", "vat"]


def execute(filters=None):
    filters = frappe._dict(filters or {})
    category = filters.get("vat_category")
    if not category:
        frappe.throw(_("Please select a VAT Category"))
    if category not in CATEGORIES:
        frappe.throw(_("Unknown VAT Category: {0}").format(category))

    doctype, key = CATEGORIES[category]
    main = importlib.import_module(MAIN_REPORT)
    if doctype == "Sales Invoice":
        breakdown = main.get_sales_invoice_breakdown(filters)
    else:
        breakdown = main.get_purchase_invoice_breakdown(filters)

    search = (filters.get("invoice") or "").strip().lower()
    data = []
    total = {f: 0 for f in NUMERIC_FIELDS}

    for name, inv in sorted(breakdown.items(), key=lambda kv: (kv[1]["posting_date"] or "", kv[0])):
        vals = dict(inv["totals"][key])
        if not any(vals.values()):
            continue
        if search and search not in name.lower():
            continue
        if category in ZERO_VAT_CATEGORIES:
            vals["vat"] = 0
        data.append({"invoice": name, "posting_date": inv["posting_date"], "party_name": inv["party_name"], **vals})
        for f in NUMERIC_FIELDS:
            total[f] += vals[f]

    count = len(data)
    data.append({"invoice": _("Total"), "party_name": _("{0} invoice(s)").format(count), **total})

    return get_columns(doctype), data, None, None, get_report_summary(count, total)


def get_report_summary(count, total):
    return [
        {"value": count, "label": _("Invoices"), "datatype": "Int"},
        {"value": total["amount_without_vat"], "label": _("Amount W/O VAT"), "datatype": "Currency"},
        {"value": total["amount"], "label": _("Amount With VAT"), "datatype": "Currency"},
        {"value": total["vat"], "label": _("VAT Amount"), "datatype": "Currency"},
    ]


def get_columns(doctype):
    party_label = _("Customer") if doctype == "Sales Invoice" else _("Supplier")
    return [
        {"label": _("Invoice"), "fieldname": "invoice", "fieldtype": "Link", "options": doctype, "width": 200},
        {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
        {"label": party_label, "fieldname": "party_name", "fieldtype": "Data", "width": 220},
        {"label": _("Amount W/O VAT(SAR)"), "fieldname": "amount_without_vat", "fieldtype": "Currency", "width": 180},
        {"label": _("Amount With VAT(SAR)"), "fieldname": "amount", "fieldtype": "Currency", "width": 180},
        {"label": _("Adjustment W/O VAT (SAR)"), "fieldname": "adjustment_without_vat", "fieldtype": "Currency", "width": 180},
        {"label": _("Adjustment With VAT(SAR)"), "fieldname": "adjustment", "fieldtype": "Currency", "width": 180},
        {"label": _("VAT Amount (SAR)"), "fieldname": "vat", "fieldtype": "Currency", "width": 180},
    ]
