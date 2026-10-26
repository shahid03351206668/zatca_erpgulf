frappe.query_reports["VAT Report ZATCA Detailed"] = {
    "filters": [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            reqd: 0,
            default: frappe.defaults.get_user_default("Company")
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 0,
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 0,
            default: frappe.datetime.month_end()
        },
        {
            fieldname: "vat_category",
            label: __("VAT Category"),
            fieldtype: "Select",
            reqd: 1,
            options: [
                "",
                "Standard rated sales",
                "Private Healthcare / Private Education sales to citizens",
                "Zero rated domestic sales",
                "Exports",
                "Exempt sales",
                "Standard rated domestic purchases",
                "Imports subject to VAT paid at customs",
                "Zero rated purchases",
                "Exempt purchases"
            ]
        },
        {
            fieldname: "invoice",
            label: __("Invoice"),
            fieldtype: "Data",
            reqd: 0
        }
    ]
};
