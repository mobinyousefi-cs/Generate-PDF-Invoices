#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: cli.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
Simple CLI to render a JSON invoice file to PDF.

Usage:
python scripts/cli.py path/to/invoice.json
"""
from __future__ import annotations

import argparse
from pathlib import Path

from invoice_generator.storage import load_invoice_json
from invoice_generator.pdf import build_pdf
from invoice_generator.storage import pdf_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render JSON invoice to PDF")
    parser.add_argument("json", type=Path, help="Path to invoice JSON")
    parser.add_argument("--out", type=Path, default=None, help="Output PDF path (optional)")
    args = parser.parse_args(argv)

    inv = load_invoice_json(args.json)
    out = args.out or pdf_path(inv.invoice_number or None)
    out.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(inv, out)
    print(f"PDF written to {out}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
