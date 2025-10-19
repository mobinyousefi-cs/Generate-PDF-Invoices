#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: test_pdf.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================
"""
from pathlib import Path
from datetime import date
from decimal import Decimal

from invoice_generator.models import Company, Customer, Item, Invoice
from invoice_generator.pdf import build_pdf


def test_build_pdf(tmp_path: Path):
    inv = Invoice(
        company=Company(name="c", address="a"),
        customer=Customer(name="u", address="a"),
        items=[Item(description="x", quantity=Decimal("1"), unit_price=Decimal("9.99"), tax_rate=Decimal("5"))],
        invoice_number="INV-TEST",
        invoice_date=date.today(),
        currency="EUR",
    )
    out = tmp_path / "test.pdf"
    build_pdf(inv, out)
    assert out.exists() and out.stat().st_size > 0
