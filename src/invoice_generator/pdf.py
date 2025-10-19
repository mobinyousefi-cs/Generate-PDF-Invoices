#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: pdf.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
PDF renderer using ReportLab. Generates a clean A4 invoice with headers, items table, and totals.
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

from .models import Invoice
from .utils import format_currency


PAGE_MARGIN = 18 * mm


def build_pdf(invoice: Invoice, output_path: Path) -> Path:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=PAGE_MARGIN,
        rightMargin=PAGE_MARGIN,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        name="Title",
        parent=styles["Heading1"],
        spaceAfter=6,
    )
    normal = styles["Normal"]
    small = ParagraphStyle(name="Small", parent=normal, fontSize=9, leading=11)

    story = []

    # Header
    story.append(Paragraph("<b>INVOICE</b>", title))

    company_block = f"""
        <b>{invoice.company.name}</b><br/>
        {invoice.company.address}<br/>
        GST/VAT: {invoice.company.gst_number}<br/>
        {invoice.company.email} | {invoice.company.phone}
    """

    meta_block = f"""
        <b>Invoice #</b>: {invoice.invoice_number or '-'}<br/>
        <b>Date</b>: {invoice.invoice_date.isoformat()}<br/>
        <b>Due</b>: {invoice.due_date.isoformat() if invoice.due_date else '-'}<br/>
        <b>Currency</b>: {invoice.currency}
    """

    info_table = Table(
        [[Paragraph(company_block, normal), Paragraph(meta_block, normal)]],
        colWidths=[100 * mm, 60 * mm],
        hAlign="LEFT",
    )
    story.append(info_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", color=colors.black))
    story.append(Spacer(1, 8))

    # Bill to
    bill_to = f"""
        <b>Bill To</b><br/>
        {invoice.customer.name}<br/>
        {invoice.customer.address}<br/>
        {invoice.customer.email} | {invoice.customer.phone}
    """
    story.append(Paragraph(bill_to, normal))
    story.append(Spacer(1, 8))

    # Items table
    table_data = [["Description", "Qty", "Unit Price", "Tax %", "Line Total"]]

    for it in invoice.items:
        table_data.append(
            [
                Paragraph(it.description, normal),
                f"{it.quantity}",
                format_currency(it.unit_price, invoice.currency),
                f"{it.tax_rate}%",
                format_currency(it.total(), invoice.currency),
            ]
        )

    tbl = Table(table_data, colWidths=[90 * mm, 20 * mm, 30 * mm, 20 * mm, 30 * mm])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(tbl)
    story.append(Spacer(1, 10))

    # Totals
    totals = Table(
        [
            ["Subtotal", format_currency(invoice.subtotal(), invoice.currency)],
            ["Tax", format_currency(invoice.tax_total(), invoice.currency)],
            ["Total", format_currency(invoice.grand_total(), invoice.currency)],
        ],
        colWidths=[40 * mm, 30 * mm],
        hAlign="RIGHT",
    )
    totals.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F0F0F0")),
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
            ]
        )
    )
    story.append(totals)

    # Notes & signature
    if invoice.notes:
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Notes</b>", normal))
        story.append(Paragraph(invoice.notes.replace("\n", "<br/>"), small))

    if invoice.authorized_by:
        story.append(Spacer(1, 18))
        story.append(Paragraph(f"Authorized by: <b>{invoice.authorized_by}</b>", normal))

    doc.build(story)
    return output_path
