#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: models.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
Typed domain models for Company, Customer, Item, and Invoice. Uses Decimal for monetary accuracy.

Usage:
python -m invoice_generator  # runs the GUI which uses these models

Notes:
- Monetary calculations use Decimal with quantize for currency rounding.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import List, Optional

getcontext().prec = 28

Currency = str


def as_money(value: Decimal, ndigits: int = 2) -> Decimal:
    quant = Decimal("1." + ("0" * ndigits))
    return value.quantize(quant, rounding=ROUND_HALF_UP)


@dataclass(slots=True)
class Company:
    name: str
    address: str
    gst_number: str = ""
    email: str = ""
    phone: str = ""


@dataclass(slots=True)
class Customer:
    name: str
    address: str
    email: str = ""
    phone: str = ""


@dataclass(slots=True)
class Item:
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal = Decimal("0.0")  # percent (e.g., 9.0 for 9%)

    def subtotal(self) -> Decimal:
        return as_money(self.quantity * self.unit_price)

    def tax_amount(self) -> Decimal:
        return as_money(self.subtotal() * (self.tax_rate / Decimal("100")))

    def total(self) -> Decimal:
        return as_money(self.subtotal() + self.tax_amount())


@dataclass(slots=True)
class Invoice:
    company: Company
    customer: Customer
    items: List[Item] = field(default_factory=list)
    invoice_number: str = ""
    invoice_date: date = field(default_factory=date.today)
    due_date: Optional[date] = None
    currency: Currency = "EUR"
    notes: str = ""
    authorized_by: str = ""  # signature name

    def subtotal(self) -> Decimal:
        return as_money(sum((i.subtotal() for i in self.items), Decimal("0")))

    def tax_total(self) -> Decimal:
        return as_money(sum((i.tax_amount() for i in self.items), Decimal("0")))

    def grand_total(self) -> Decimal:
        return as_money(self.subtotal() + self.tax_total())

    def to_dict(self) -> dict:
        # Convert Decimals and dates to strings for JSON persistence
        def _convert(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, date):
                return obj.isoformat()
            return obj

        d = asdict(self)
        d["items"] = [
            {
                "description": it.description,
                "quantity": str(it.quantity),
                "unit_price": str(it.unit_price),
                "tax_rate": str(it.tax_rate),
            }
            for it in self.items
        ]
        d["invoice_date"] = self.invoice_date.isoformat()
        d["due_date"] = self.due_date.isoformat() if self.due_date else None
        return d

    @staticmethod
    def from_dict(data: dict) -> "Invoice":
        company = Company(**data["company"]) if isinstance(data.get("company"), dict) else Company(
            name=data.get("company", {}).get("name", ""),
            address=data.get("company", {}).get("address", ""),
            gst_number=data.get("company", {}).get("gst_number", ""),
            email=data.get("company", {}).get("email", ""),
            phone=data.get("company", {}).get("phone", ""),
        )
        customer = (
            Customer(**data["customer"]) if isinstance(data.get("customer"), dict) else Customer(
                name=data.get("customer", {}).get("name", ""),
                address=data.get("customer", {}).get("address", ""),
                email=data.get("customer", {}).get("email", ""),
                phone=data.get("customer", {}).get("phone", ""),
            )
        )
        items = [
            Item(
                description=i.get("description", ""),
                quantity=Decimal(str(i.get("quantity", "0"))),
                unit_price=Decimal(str(i.get("unit_price", "0"))),
                tax_rate=Decimal(str(i.get("tax_rate", "0"))),
            )
            for i in data.get("items", [])
        ]
        inv = Invoice(
            company=company,
            customer=customer,
            items=items,
            invoice_number=data.get("invoice_number", ""),
            invoice_date=date.fromisoformat(data.get("invoice_date", date.today().isoformat())),
            due_date=(date.fromisoformat(data["due_date"]) if data.get("due_date") else None),
            currency=data.get("currency", "EUR"),
            notes=data.get("notes", ""),
            authorized_by=data.get("authorized_by", ""),
        )
        return inv
