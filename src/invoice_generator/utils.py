#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: utils.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
Helper utilities for validation, currency formatting, and safe Decimal parsing.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional


def parse_decimal(value: str, default: str = "0") -> Decimal:
    try:
        # strip spaces and replace common comma decimals
        cleaned = value.strip().replace(",", ".")
        return Decimal(cleaned)
    except (InvalidOperation, AttributeError):
        return Decimal(default)


def format_currency(amount: Decimal, currency: str = "EUR") -> str:
    return f"{amount:,.2f} {currency}".replace(",", "_").replace(".", ",").replace("_", ".")


def non_empty(text: Optional[str]) -> bool:
    return bool(text and text.strip())
