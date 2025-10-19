#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
Module entry point. Launches the Tkinter GUI. Also provides a --sample-json helper.

Usage:
python -m invoice_generator            # start GUI
python -m invoice_generator --sample-json   # write a sample invoice JSON into ./invoices/
"""
from __future__ import annotations

import argparse
import json
import sys
import tkinter as tk
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal

from .gui import App
from .models import Company, Customer, Item, Invoice
from .storage import INVOICES_DIR, save_invoice_json


SAMPLE_JSON_NAME = "sample"


def write_sample_json() -> Path:
    inv = Invoice(
        company=Company(
            name="Mobin Yousefi — Solutions",
            address="Via Roma 1, 00100 Roma, Italy",
            gst_number="IT12345678901",
            email="info@example.com",
            phone="+39 0123 456789",
        ),
        customer=Customer(
            name="Acme Corp.",
            address="123 Business Rd, 75000 Paris, France",
            email="billing@acme.com",
            phone="+33 1 23 45 67 89",
        ),
        items=[
            Item(description="Consulting Services — Week 41", quantity=Decimal("8"), unit_price=Decimal("120"), tax_rate=Decimal("22")),
            Item(description="Prototype Implementation", quantity=Decimal("1"), unit_price=Decimal("950"), tax_rate=Decimal("22")),
        ],
        invoice_number="INV-2025-001",
        invoice_date=date.today(),
        due_date=date.today() + timedelta(days=14),
        currency="EUR",
        notes="Thank you for your business!",
        authorized_by="Mobin Yousefi",
    )
    INVOICES_DIR.mkdir(parents=True, exist_ok=True)
    path = INVOICES_DIR / f"{SAMPLE_JSON_NAME}.json"
    save_invoice_json(inv, path)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="invoice_generator", description="Invoice Generator GUI/CLI")
    parser.add_argument("--sample-json", action="store_true", help="Write a sample invoice JSON and exit")
    args = parser.parse_args(argv)

    if args.sample_json:
        path = write_sample_json()
        print(json.dumps({"sample_json": str(path)}, indent=2))
        return 0

    root = tk.Tk()
    App(root)
    root.mainloop()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
