// Categories that drill down to the detailed report
const VAT_DRILLDOWN_CATEGORIES = [
    "Standard rated sales",
    "Private Healthcare / Private Education sales to citizens",
    "Zero rated domestic sales",
    "Exports",
    "Exempt sales",
    "Standard rated domestic purchases",
    "Imports subject to VAT paid at customs",
    "Zero rated purchases",
    "Exempt purchases"
];

function open_vat_detailed_report(category) {
    const f = frappe.query_report.get_filter_values();
    frappe.set_route("query-report", "VAT Report ZATCA Detailed", {
        company: f.company,
        from_date: f.from_date,
        to_date: f.to_date,
        vat_category: category
    });
}

frappe.query_reports["VAT Report ZATCA on Sales & Purchase"] = {
    "filters": [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            reqd: 0,  // optional
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
        }
    ],
    formatter: function (value, row, column, data, default_formatter) {
        if (column.fieldname === "category" && VAT_DRILLDOWN_CATEGORIES.includes(data.category)) {
            return `<a href="#" onclick="open_vat_detailed_report(${JSON.stringify(data.category).replace(/"/g, "&quot;")}); return false;">${frappe.utils.escape_html(data.category)}</a>`;
        }
        return default_formatter(value, row, column, data);
    }
};
