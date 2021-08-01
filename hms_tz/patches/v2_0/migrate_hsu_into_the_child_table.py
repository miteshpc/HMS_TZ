# Copyright (c) 2021, Aakvatech and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


def execute():
    frappe.reload_doc("hms_tz", "doctype", "lab_test_template")
    frappe.reload_doc("hms_tz", "doctype", "therapy_type")
    frappe.reload_doc("hms_tz", "doctype", "radiology_examination_template")
    frappe.reload_doc("hms_tz", "doctype", "clinical_procedure_template")
    frappe.reload_doc("hms_tz", "doctype", "service_unit_company")

    def update_docs(doc_list, doctype):
        for doc_name in doc_list:
            doc = frappe.get_doc(doctype, doc_name.get("name"))
            if not doc.healthcare_service_unit:
                continue
            company = frappe.get_value(
                "Healthcare Service Unit", doc.healthcare_service_unit, "company"
            )
            row = doc.append("service_units", {})
            row.company = company
            row.service_unit = doc.healthcare_service_unit
            row.db_update()
            doc.healthcare_service_unit = None
            doc.db_update()

    doctypes = [
        "Lab Test Template",
        "Therapy Type",
        "Radiology Examination Template",
        "Clinical Procedure Template",
    ]

    for doctype in doctypes:
        doc_list = frappe.get_all(
            doctype, filters={"healthcare_service_unit": ["not in", ["", None]]}
        )
        update_docs(doc_list, doctype)