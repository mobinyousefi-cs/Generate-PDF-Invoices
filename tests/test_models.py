#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: test_models.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================
"""
from decimal import Decimal

from invoice_generator.models import Item, Company, Customer, Invoice


def test_item_totals():
    it = Item(description="x", quantity=Decimal("2"), unit_price=Decimal("10"), tax_rate=Decimal("10"))
    assert it.subtotal() == Decimal("20.00")
    assert it.tax_amount() == Decimal("2.00")
    assert it.total() == Decimal("22.00")


def test_invoice_aggregates():
    items = [
        Item(description="a", quantity=Decimal("1"), unit_price=Decimal("100"), tax_rate=Decimal("0")),
        Item(description="b", quantity=Decimal("2"), unit_price=Decimal("50"), tax_rate=Decimal("10")),
    ]
    inv = Invoice(
        company=Company(name="c", address="addr"),
        customer=Customer(name="u", address="addr"),
        items=items,
    )
    assert inv.subtotal() == Decimal("200.00")
    assert inv.tax_total() == Decimal("10.00")
    assert inv.grand_total() == Decimal("210.00")
