#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: storage.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
Local filesystem persistence for invoices (JSON) and emitted PDFs.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Tuple

from .models import Invoice

BASE_DIR = Path.cwd()
INVOICES_DIR = BASE_DIR / "invoices"
INVOICES_DIR.mkdir(parents=True, exist_ok=True)


def iso_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def json_path(invoice_number: str | None = None) -> Path:
    name = invoice_number or f"invoice-{iso_stamp()}"
    return INVOICES_DIR / f"{name}.json"


def pdf_path(invoice_number: str | None = None) -> Path:
    name = invoice_number or f"invoice-{iso_stamp()}"
    return INVOICES_DIR / f"{name}.pdf"


def save_invoice_json(invoice: Invoice, path: Path | None = None) -> Path:
    target = path or json_path(invoice.invoice_number or None)
    data = invoice.to_dict()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def load_invoice_json(path: Path) -> Invoice:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Invoice.from_dict(data)


def ensure_output_paths(invoice: Invoice) -> Tuple[Path, Path]:
    j = json_path(invoice.invoice_number or None)
    p = pdf_path(invoice.invoice_number or None)
    return j, p
