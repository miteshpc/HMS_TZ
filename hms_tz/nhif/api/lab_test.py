# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from hms_tz.nhif.api.healthcare_utils import create_delivery_note_from_LRPT


@frappe.whitelist()
def get_normals(lab_test_name, patient_age, patient_sex):
    data = {}
    doc = get_lab_test_template(lab_test_name)
    if not doc:
        return data
    if float(patient_age) < 3:
        data["min"] = doc.i_min_range
        data["max"] = doc.i_max_range
        data["text"] = doc.i_text
    elif float(patient_age) < 12:
        data["min"] = doc.c_min_range
        data["max"] = doc.c_max_range
        data["text"] = doc.c_text
    else:
        if patient_sex == "Male":
            data["min"] = doc.m_min_range
            data["max"] = doc.m_max_range
            data["text"] = doc.m_text
        elif patient_sex == "Female":
            data["min"] = doc.f_min_range
            data["max"] = doc.f_max_range
            data["text"] = doc.f_text

    return data


def get_lab_test_template(lab_test_name):
    template_id = frappe.db.exists(
        'Lab Test Template', {'lab_test_name': lab_test_name})
    if template_id:
        return frappe.get_doc('Lab Test Template', template_id)
    return False


def on_submit(doc, methd):
    create_delivery_note(doc)


def create_delivery_note(doc):
    if doc.ref_doctype and doc.ref_docname and doc.ref_doctype == "Patient Encounter":
        patient_encounter_doc = frappe.get_doc(
            doc.ref_doctype, doc.ref_docname)
        create_delivery_note_from_LRPT(doc, patient_encounter_doc)
