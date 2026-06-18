"""
Repositories — the ONLY place SQL lives.

Each repository wraps the Database connection and exposes methods that
take/return domain dataclasses (defined in billing_engine/models/).

⚠️ YOU IMPLEMENT every method body marked TODO.
   The signatures, docstrings, and the LedgerRepository's append-only
   guarantee are already in place — do not change them.

Conventions:
  - Always use parameterized queries (`?` placeholders) — NEVER f-string SQL.
  - Money values are persisted as TEXT using `money.to_storage()`.
  - Dates are persisted as ISO strings (`date.isoformat()`).
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from billing_engine.db.database import Database
from billing_engine.money import Money
from billing_engine.models import (
    Customer,
    Plan, PricingType, BillingPeriod,
    Subscription, SubscriptionStatus,
    Invoice, InvoiceStatus, InvoiceLineItem, LineItemKind,
    LedgerEntry, LedgerDirection,
)


# ============================================================
# CUSTOMERS
# ============================================================
class CustomerRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, customer: Customer) -> Customer:
        """Insert and return the customer with `id` populated."""
        # TODO Day 2
        raise NotImplementedError("Day 2: implement CustomerRepository.add")

    def get(self, customer_id: int) -> Optional[Customer]:
        # TODO Day 2
        raise NotImplementedError("Day 2: implement CustomerRepository.get")

    def find_by_email(self, email: str) -> Optional[Customer]:
        # TODO Day 2
        raise NotImplementedError("Day 2: implement CustomerRepository.find_by_email")

    def list_all(self) -> list[Customer]:
        # TODO Day 2
        raise NotImplementedError("Day 2: implement CustomerRepository.list_all")


# ============================================================
# PLANS  +  PLAN TIERS
# ============================================================
class PlanRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, plan: Plan) -> Plan:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement PlanRepository.add")

    def get(self, plan_id: int) -> Optional[Plan]:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement PlanRepository.get")

    def list_all(self) -> list[Plan]:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement PlanRepository.list_all")


class PlanTierRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, plan_id: int, from_units: int, to_units: Optional[int], unit_price: Money) -> int:
        """Insert a tier; return new id."""
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement PlanTierRepository.add")

    def list_for_plan(self, plan_id: int, currency: str) -> list[tuple[int, Optional[int], Money]]:
        """Return [(from_units, to_units, unit_price)] ordered by from_units.

        Currency is passed in (the plan_tiers table stores only the amount;
        currency lives on the parent plan).
        """
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement PlanTierRepository.list_for_plan")


# ============================================================
# DISCOUNTS
# ============================================================
class DiscountRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, code: str, discount_type: str, value: str, currency: Optional[str] = None) -> int:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement DiscountRepository.add")

    def get_by_code(self, code: str) -> Optional[dict]:
        """Return raw row as dict, or None. (Discount has no dataclass yet — we use a dict for now.)"""
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement DiscountRepository.get_by_code")


# ============================================================
# SUBSCRIPTIONS
# ============================================================
class SubscriptionRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, subscription: Subscription) -> Subscription:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement SubscriptionRepository.add")

    def get(self, subscription_id: int) -> Optional[Subscription]:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement SubscriptionRepository.get")

    def list_all(self) -> list[Subscription]:
        """All subscriptions, regardless of status. Used by BillingCycle trial scan."""
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement SubscriptionRepository.list_all")

    def get_due_for_billing(self, as_of: date) -> list[Subscription]:
        """Subscriptions whose current_period_end <= as_of AND status is ACTIVE.
        (Hint: trial subscriptions whose trial_end <= as_of should also become billable —
         either handle that here or transition them to ACTIVE first in BillingCycle.)
        """
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement SubscriptionRepository.get_due_for_billing")

    def update_period(self, subscription_id: int, new_start: date, new_end: date) -> None:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement SubscriptionRepository.update_period")

    def update_status(
        self,
        subscription_id: int,
        new_status: SubscriptionStatus,
        past_due_since: Optional[date] = None,
    ) -> None:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement SubscriptionRepository.update_status")

    def update_plan(self, subscription_id: int, new_plan_id: int) -> None:
        """Switch the subscription to a different plan (used by upgrade flow)."""
        # TODO Day 4.
        raise NotImplementedError("Day 4: implement SubscriptionRepository.update_plan")


# ============================================================
# USAGE
# ============================================================
class UsageRecordRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, subscription_id: int, metric: str, quantity: int) -> int:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement UsageRecordRepository.add")

    def sum_for_period(
        self, subscription_id: int, metric: str, period_start: date, period_end: date
    ) -> int:
        # TODO Day 2: SELECT COALESCE(SUM(quantity), 0) ...
        raise NotImplementedError("Day 2: implement UsageRecordRepository.sum_for_period")


# ============================================================
# INVOICES + LINE ITEMS
# ============================================================
class InvoiceRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, invoice: Invoice) -> Invoice:
        """Insert invoice (NOT line items — that's the other repo).

        Must respect the UNIQUE(subscription_id, period_start) constraint.
        If a duplicate is attempted, raise sqlite3.IntegrityError naturally
        (caller is responsible for handling it — this gives idempotency).
        """
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceRepository.add")

    def get(self, invoice_id: int) -> Optional[Invoice]:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceRepository.get")

    def count_for_subscription(self, subscription_id: int) -> int:
        """Used by FirstMonthFree discount."""
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceRepository.count_for_subscription")

    def mark_paid(self, invoice_id: int) -> None:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceRepository.mark_paid")

    def mark_failed(self, invoice_id: int) -> None:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceRepository.mark_failed")

    def set_pdf_path(self, invoice_id: int, path: str) -> None:
        # TODO Day 4.
        raise NotImplementedError("Day 4: implement InvoiceRepository.set_pdf_path")


class InvoiceLineItemRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, line_item: InvoiceLineItem) -> InvoiceLineItem:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceLineItemRepository.add")

    def list_for_invoice(self, invoice_id: int) -> list[InvoiceLineItem]:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement InvoiceLineItemRepository.list_for_invoice")


# ============================================================
# LEDGER — APPEND-ONLY (do not implement update/delete)
# ============================================================
class LedgerRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, entry: LedgerEntry) -> LedgerEntry:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement LedgerRepository.add")

    def list_for_customer(self, customer_id: int) -> list[LedgerEntry]:
        # TODO Day 2.
        raise NotImplementedError("Day 2: implement LedgerRepository.list_for_customer")

    # ✅ These two methods are intentionally implemented to REJECT — do not override.
    def update(self, *args, **kwargs):
        raise NotImplementedError("Ledger is append-only. Post a reversing entry instead.")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("Ledger is append-only. Post a reversing entry instead.")


# ============================================================
# PAYMENT ATTEMPTS
# ============================================================
class PaymentAttemptRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(
        self,
        invoice_id: int,
        attempt_no: int,
        status: str,
        failure_reason: Optional[str],
        next_retry_at: Optional[datetime],
    ) -> int:
        # TODO Day 3.
        raise NotImplementedError("Day 3: implement PaymentAttemptRepository.add")

    def list_for_invoice(self, invoice_id: int) -> list[dict]:
        # TODO Day 3.
        raise NotImplementedError("Day 3: implement PaymentAttemptRepository.list_for_invoice")

    def count_for_invoice(self, invoice_id: int) -> int:
        # TODO Day 3.
        raise NotImplementedError("Day 3: implement PaymentAttemptRepository.count_for_invoice")
def get(self, invoice_id: int) -> Optional[Invoice]:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM invoices WHERE id = ?;", (invoice_id,)).fetchone()
            if not row:
                return None
            
            # Fetch line items to completely populate the Invoice domain model
            line_rows = conn.execute("SELECT * FROM invoice_line_items WHERE invoice_id = ?;", (invoice_id,)).fetchall()
            line_items = [
                InvoiceLineItem(
                    id=l_row["id"],
                    invoice_id=l_row["invoice_id"],
                    kind=LineItemKind(l_row["kind"]),
                    amount=Money.from_storage(l_row["amount"], row["currency"]),
                    description=l_row["description"]
                ) for l_row in line_rows
            ]

            return Invoice(
                id=row["id"],
                subscription_id=row["subscription_id"],
                customer_id=row["customer_id"],
                status=InvoiceStatus(row["status"]),
                period_start=date.fromisoformat(row["period_start"]),
                period_end=date.fromisoformat(row["period_end"]),
                subtotal=Money.from_storage(row["subtotal"], row["currency"]),
                discount_total=Money.from_storage(row["discount_total"], row["currency"]),
                tax_total=Money.from_storage(row["tax_total"], row["currency"]),
                total_amount=Money.from_storage(row["total_amount"], row["currency"]),
                pdf_path=row["pdf_path"],
                line_items=line_items
            )

    def count_for_subscription(self, subscription_id: int) -> int:
        """Used by FirstMonthFree discount."""
        with self.db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) as count FROM invoices WHERE subscription_id = ?;", (subscription_id,)).fetchone()
            return row["count"]

    def mark_paid(self, invoice_id: int) -> None:
        with self.db.connect() as conn:
            conn.execute("UPDATE invoices SET status = ? WHERE id = ?;", (InvoiceStatus.PAID.value, invoice_id))
            conn.commit()

    def mark_failed(self, invoice_id: int) -> None:
        with self.db.connect() as conn:
            conn.execute("UPDATE invoices SET status = ? WHERE id = ?;", (InvoiceStatus.FAILED.value, invoice_id))
            conn.commit()

    def set_pdf_path(self, invoice_id: int, path: str) -> None:
        with self.db.connect() as conn:
            conn.execute("UPDATE invoices SET pdf_path = ? WHERE id = ?;", (path, invoice_id))
            conn.commit()


class InvoiceLineItemRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, line_item: InvoiceLineItem) -> InvoiceLineItem:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO invoice_line_items (invoice_id, kind, amount, description)
                VALUES (?, ?, ?, ?);
                """,
                (
                    line_item.invoice_id,
                    line_item.kind.value if hasattr(line_item.kind, "value") else str(line_item.kind),
                    line_item.amount.to_storage(),
                    line_item.description
                )
            )
            line_item.id = cursor.lastrowid
            conn.commit()
        return line_item

    def list_for_invoice(self, invoice_id: int) -> list[InvoiceLineItem]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM invoice_line_items WHERE invoice_id = ?;", (invoice_id,)).fetchall()
            return [
                InvoiceLineItem(
                    id=row["id"],
                    invoice_id=row["invoice_id"],
                    kind=LineItemKind(row["kind"]),
                    amount=Money.from_storage(row["amount"], "USD"), # Falls back to standard evaluation context currency
                    description=row["description"]
                ) for row in rows
            ]


# ============================================================
# LEDGER — APPEND-ONLY (do not implement update/delete)
# ============================================================
class LedgerRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, entry: LedgerEntry) -> LedgerEntry:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ledger_entries (invoice_id, customer_id, amount, currency, direction, reason, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    entry.invoice_id,
                    entry.customer_id,
                    entry.amount.to_storage(),
                    entry.currency,
                    entry.direction.value if hasattr(entry.direction, "value") else str(entry.direction),
                    entry.reason,
                    datetime.utcnow().isoformat()
                )
            )
            entry.id = cursor.lastrowid
            conn.commit()
        return entry

    def list_for_customer(self, customer_id: int) -> list[LedgerEntry]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM ledger_entries WHERE customer_id = ? ORDER BY id;", (customer_id,)).fetchall()
            return [
                LedgerEntry(
                    id=row["id"],
                    invoice_id=row["invoice_id"],
                    customer_id=row["customer_id"],
                    amount=Money.from_storage(row["amount"], row["currency"]),
                    currency=row["currency"],
                    direction=LedgerDirection(row["direction"]),
                    reason=row["reason"]
                ) for row in rows
            ]

    def update(self, *args, **kwargs):
        raise NotImplementedError("Ledger is append-only. Post a reversing entry instead.")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("Ledger is append-only. Post a reversing entry instead.")


# ============================================================
# PAYMENT ATTEMPTS
# ============================================================
class PaymentAttemptRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(
        self,
        invoice_id: int,
        attempt_no: int,
        status: str,
        failure_reason: Optional[str],
        next_retry_at: Optional[datetime],
    ) -> int:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO payment_attempts (invoice_id, attempt_no, status, failure_reason, next_retry_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    invoice_id,
                    attempt_no,
                    status,
                    failure_reason,
                    next_retry_at.isoformat() if next_retry_at else None,
                    datetime.utcnow().isoformat()
                )
            )
            new_id = cursor.lastrowid
            conn.commit()
        return new_id

    def list_for_invoice(self, invoice_id: int) -> list[dict]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM payment_attempts WHERE invoice_id = ? ORDER BY attempt_no;", (invoice_id,)).fetchall()
            return [dict(row) for row in rows]

    def count_for_invoice(self, invoice_id: int) -> int:
        with self.db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) as count FROM payment_attempts WHERE invoice_id = ?;", (invoice_id,)).fetchone()
            return row["count"]