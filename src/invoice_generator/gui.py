#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================================================================
Project: Invoice Generator (Tkinter + ReportLab)
File: gui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
============================================================================================================================

Description:
Tkinter GUI: forms for company/customer, dynamic items table, and buttons to save JSON or export PDF.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
from decimal import Decimal

from .models import Company, Customer, Item, Invoice
from .utils import parse_decimal
from .storage import save_invoice_json, load_invoice_json, pdf_path
from .pdf import build_pdf


class LabeledEntry(ttk.Frame):
    def __init__(self, master, text: str, width: int = 40):
        super().__init__(master)
        ttk.Label(self, text=text, width=18, anchor="w").pack(side="left")
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, width=width)
        self.entry.pack(side="left", fill="x", expand=True)

    def get(self) -> str:
        return self.var.get().strip()

    def set(self, value: str) -> None:
        self.var.set(value)


class ItemsTable(ttk.Frame):
    COLS = ("description", "quantity", "unit_price", "tax_rate")

    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=self.COLS, show="headings", height=8)
        headings = [
            ("description", "Description"),
            ("quantity", "Qty"),
            ("unit_price", "Unit Price"),
            ("tax_rate", "Tax %"),
        ]
        for key, label in headings:
            self.tree.heading(key, text=label)
            self.tree.column(key, width=150 if key == "description" else 90, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")

        btns = ttk.Frame(self)
        ttk.Button(btns, text="Add", command=self.add_row).pack(fill="x")
        ttk.Button(btns, text="Edit", command=self.edit_row).pack(fill="x")
        ttk.Button(btns, text="Delete", command=self.delete_row).pack(fill="x")
        btns.pack(side="right", padx=6)

    def add_row(self, item: Item | None = None):
        dlg = ItemDialog(self, item)
        self.wait_window(dlg)
        if dlg.result:
            it = dlg.result
            self.tree.insert("", "end", values=(it.description, str(it.quantity), str(it.unit_price), str(it.tax_rate)))

    def edit_row(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Edit Item", "Select a row to edit.")
            return
        values = self.tree.item(sel[0], "values")
        it = Item(description=values[0], quantity=Decimal(values[1]), unit_price=Decimal(values[2]), tax_rate=Decimal(values[3]))
        dlg = ItemDialog(self, it)
        self.wait_window(dlg)
        if dlg.result:
            self.tree.item(sel[0], values=(dlg.result.description, str(dlg.result.quantity), str(dlg.result.unit_price), str(dlg.result.tax_rate)))

    def delete_row(self):
        sel = self.tree.selection()
        for s in sel:
            self.tree.delete(s)

    def items(self) -> list[Item]:
        out: list[Item] = []
        for child in self.tree.get_children(""):
            d, q, u, t = self.tree.item(child, "values")
            out.append(Item(description=d, quantity=Decimal(q), unit_price=Decimal(u), tax_rate=Decimal(t)))
        return out


class ItemDialog(tk.Toplevel):
    def __init__(self, master, item: Item | None = None):
        super().__init__(master)
        self.title("Item")
        self.resizable(False, False)
        self.result: Item | None = None

        self.desc = LabeledEntry(self, "Description:")
        self.qty = LabeledEntry(self, "Quantity:")
        self.uprice = LabeledEntry(self, "Unit Price:")
        self.tax = LabeledEntry(self, "Tax %:")

        self.desc.pack(fill="x", padx=8, pady=2)
        self.qty.pack(fill="x", padx=8, pady=2)
        self.uprice.pack(fill="x", padx=8, pady=2)
        self.tax.pack(fill="x", padx=8, pady=2)

        btns = ttk.Frame(self)
        ttk.Button(btns, text="OK", command=self.on_ok).pack(side="left", padx=5)
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", padx=5)
        btns.pack(pady=6)

        if item:
            self.desc.set(item.description)
            self.qty.set(str(item.quantity))
            self.uprice.set(str(item.unit_price))
            self.tax.set(str(item.tax_rate))

        self.transient(master)
        self.grab_set()
        self.desc.entry.focus_set()

    def on_ok(self):
        try:
            it = Item(
                description=self.desc.get(),
                quantity=parse_decimal(self.qty.get()),
                unit_price=parse_decimal(self.uprice.get()),
                tax_rate=parse_decimal(self.tax.get()),
            )
        except Exception as e:  # pragma: no cover (UI path)
            messagebox.showerror("Invalid input", str(e))
            return
        self.result = it
        self.destroy()


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Invoice Generator — Mobin Yousefi")
        master.geometry("980x720")
        master.minsize(860, 600)

        # Notebook tabs
        nb = ttk.Notebook(self)
        self.company_tab = ttk.Frame(nb)
        self.customer_tab = ttk.Frame(nb)
        self.items_tab = ttk.Frame(nb)
        nb.add(self.company_tab, text="Company")
        nb.add(self.customer_tab, text="Customer")
        nb.add(self.items_tab, text="Items")
        nb.pack(fill="both", expand=True)

        # Company form
        self.c_name = LabeledEntry(self.company_tab, "Company Name:")
        self.c_addr = LabeledEntry(self.company_tab, "Address:")
        self.c_gst = LabeledEntry(self.company_tab, "GST/VAT No:")
        self.c_email = LabeledEntry(self.company_tab, "Email:")
        self.c_phone = LabeledEntry(self.company_tab, "Phone:")
        for w in (self.c_name, self.c_addr, self.c_gst, self.c_email, self.c_phone):
            w.pack(fill="x", padx=12, pady=4)

        # Customer form
        self.u_name = LabeledEntry(self.customer_tab, "Customer Name:")
        self.u_addr = LabeledEntry(self.customer_tab, "Address:")
        self.u_email = LabeledEntry(self.customer_tab, "Email:")
        self.u_phone = LabeledEntry(self.customer_tab, "Phone:")
        for w in (self.u_name, self.u_addr, self.u_email, self.u_phone):
            w.pack(fill="x", padx=12, pady=4)

        # Invoice meta + items
        meta = ttk.Frame(self.items_tab)
        self.inv_no = LabeledEntry(meta, "Invoice Number:", width=20)
        self.inv_date = LabeledEntry(meta, "Invoice Date (YYYY-MM-DD):", width=20)
        self.due_date = LabeledEntry(meta, "Due Date (YYYY-MM-DD):", width=20)
        self.currency = LabeledEntry(meta, "Currency (e.g., EUR):", width=12)
        self.notes = LabeledEntry(meta, "Notes:", width=60)
        self.auth = LabeledEntry(meta, "Authorized By:", width=30)
        for w in (self.inv_no, self.inv_date, self.due_date, self.currency, self.notes, self.auth):
            w.pack(fill="x", padx=12, pady=3)
        meta.pack(fill="x", pady=6)

        self.items_table = ItemsTable(self.items_tab)
        self.items_table.pack(fill="both", expand=True, padx=12, pady=6)

        # Actions
        actions = ttk.Frame(self)
        ttk.Button(actions, text="New", command=self.clear_all).pack(side="left", padx=4)
        ttk.Button(actions, text="Open JSON…", command=self.open_json).pack(side="left", padx=4)
        ttk.Button(actions, text="Save JSON", command=self.save_json).pack(side="left", padx=4)
        ttk.Button(actions, text="Export PDF", command=self.export_pdf).pack(side="left", padx=4)
        actions.pack(fill="x", pady=6)

        self.pack(fill="both", expand=True)
        self.prefill_defaults()

    # Helpers
    def prefill_defaults(self):
        self.currency.set("EUR")
        self.inv_date.set(date.today().isoformat())

    def build_invoice(self) -> Invoice:
        company = Company(
            name=self.c_name.get(),
            address=self.c_addr.get(),
            gst_number=self.c_gst.get(),
            email=self.c_email.get(),
            phone=self.c_phone.get(),
        )
        customer = Customer(
            name=self.u_name.get(),
            address=self.u_addr.get(),
            email=self.u_email.get(),
            phone=self.u_phone.get(),
        )
        inv = Invoice(
            company=company,
            customer=customer,
            items=self.items_table.items(),
            invoice_number=self.inv_no.get(),
            invoice_date=date.fromisoformat(self.inv_date.get() or date.today().isoformat()),
            due_date=(date.fromisoformat(self.due_date.get()) if self.due_date.get() else None),
            currency=self.currency.get() or "EUR",
            notes=self.notes.get(),
            authorized_by=self.auth.get(),
        )
        return inv

    # Actions
    def clear_all(self):
        for entry in (
            self.c_name,
            self.c_addr,
            self.c_gst,
            self.c_email,
            self.c_phone,
            self.u_name,
            self.u_addr,
            self.u_email,
            self.u_phone,
            self.inv_no,
            self.inv_date,
            self.due_date,
            self.currency,
            self.notes,
            self.auth,
        ):
            entry.set("")
        for ch in self.items_table.tree.get_children(""):
            self.items_table.tree.delete(ch)
        self.prefill_defaults()

    def save_json(self):
        inv = self.build_invoice()
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=(inv.invoice_number or "invoice"),
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return
        save_invoice_json(inv, Path(path))
        messagebox.showinfo("Saved", f"Invoice saved to\n{path}")

    def open_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        inv = load_invoice_json(Path(path))
        self.load_into_form(inv)

    def load_into_form(self, inv: Invoice):
        self.c_name.set(inv.company.name)
        self.c_addr.set(inv.company.address)
        self.c_gst.set(inv.company.gst_number)
        self.c_email.set(inv.company.email)
        self.c_phone.set(inv.company.phone)

        self.u_name.set(inv.customer.name)
        self.u_addr.set(inv.customer.address)
        self.u_email.set(inv.customer.email)
        self.u_phone.set(inv.customer.phone)

        self.inv_no.set(inv.invoice_number)
        self.inv_date.set(inv.invoice_date.isoformat())
        self.due_date.set(inv.due_date.isoformat() if inv.due_date else "")
        self.currency.set(inv.currency)
        self.notes.set(inv.notes)
        self.auth.set(inv.authorized_by)

        for ch in self.items_table.tree.get_children(""):
            self.items_table.tree.delete(ch)
        for it in inv.items:
            self.items_table.tree.insert("", "end", values=(it.description, str(it.quantity), str(it.unit_price), str(it.tax_rate)))

    def export_pdf(self):
        inv = self.build_invoice()
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=(inv.invoice_number or "invoice"),
            filetypes=[("PDF", "*.pdf")],
        )
        if not path:
            return
        build_pdf(inv, Path(path))
        messagebox.showinfo("Exported", f"PDF written to\n{path}")
