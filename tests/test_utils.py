#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: test_utils.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================
"""
from decimal import Decimal

from invoice_generator.utils import parse_decimal, format_currency, non_empty


def test_parse_decimal():
    assert parse_decimal("12.34") == Decimal("12.34")
    assert parse_decimal("12,34") == Decimal("12.34")
    assert parse_decimal("oops", default="1") == Decimal("1")


def test_format_currency():
    s = format_currency(Decimal("1234.50"), "EUR")
    assert "EUR" in s


def test_non_empty():
    assert non_empty(" a ") is True
    assert non_empty("") is False
