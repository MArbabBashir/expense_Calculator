# # Expense calculator
#
# from __future__ import annotations
# import json
# import time
# from datetime import datetime
# from pathlib import Path
#
# from rich import style
#
# try:
#     from rich.console import Console
#     from rich.table import Table
#
#     RICH = True
#     console = Console()
# except ImportError as e:
#     RICH = False
#     console = None
#     print(f"error: {e}")
#
#
# DATA_FILE = Path(__file__).resolve().with_name("expenses.json")
# print(DATA_FILE)
#
# def say(msg:str = "", style:str | None = None) ->None:
#     if RICH:
#         console.print(msg, style=style)
#     else:
#         print(msg)
#
#
#
# def load() -> list[dict]:
#     "read expenses.json file. Returns [] if the file is missing or unusable "
#     if not DATA_FILE.exists():
#         print("no expenses.json yet- will create on first save")
#         return []
#     print(f"loading ...  {DATA_FILE}")
#
#     try:
#         with DATA_FILE.open(encoding = "utf-8") as f:
#             data = json.load(f)
#     except json.JSONDecodeError as exc:
#         backup = DATA_FILE.with_name(
#             f"{DATA_FILE}.corrupt-{int(time.time())}.json"
#         )
#         DATA_FILE.replace(backup)
#         say(f"!{DATA_FILE} was not valid JSON({exec}).", "bold red")
#         return []
#     except OSError as exc:
#         say(f"!{DATA_FILE} could not read {DATA_FILE.name}:{exc}.", "bold red")
#         return []
#     if not isinstance(data, list):
#         say("! Unexpected data format; starting empty.", "bold red")
#         return []
#     return data
#
#
#
# def save(items: list[dict]) -> None:
#     """writes the list back to disk. writes to a temp file """
#     tmp = DATA_FILE.with_name(DATA_FILE.name + ".tmp")
#     with tmp.open("w", encoding="utf-8") as f:
#         json.dump(items,f, indent=4, ensure_ascii=False)
#         f.write("\n")
#         tmp.replace(DATA_FILE)
#
# def add_expense(
#         items:list[dict],
#         amount: float,
#         category:str,
#         note:str=""
# )->list[dict]:
#     expense = {
#         "id" : int(time.time() * 1000),
#         "amount": round(float(amount),2),
#         "category": category.strip().lower(),
#         "date": datetime.now().isoformat(timespec="seconds")
#     }
#     return items + expense
#
#
#
# def summarize(items:list[dict])-> dict[str, float]:
#     totals: dict[str, float] = {}
#     for e in items:
#         totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
#     return totals
#
#
# def delete_expense(items: list[dict], expense_id:int) -> tuple[list[dict], bool]:
#     kept = [e for e in items if e["id"] != expense_id  ]
#     removed = len(kept) != len(items)
#     return kept, removed
#
# def prompt_amount() -> float | None:
#     while True:
#         raw = input("Amount(blank to cancel)").strip()
#         if not raw:
#             return None
#         try:
#             value = float(raw)
#         except ValueError:
#             return say("not a number- try again(e.g 12.50).", "yellow")
#         continue
#         if value < 0:
#             say("amount must be greater than 0","yellow")
#             continue
#         return value
#
#
#
#
# def prompt_category():
#     raw = input("Category (e.g food, transport, blank to  other)").strip()
#     return raw.lower() if raw else "other"
#
# def prompt_note() -> str:
#     return input("Note(blank to cancel)").strip()
#
# def pause() -> None:
#     try:
#         input("\n press enter to continue....")
#     except EOFError:
#         pass
#
#
# def cmd_Add() -> None:
#     say()
#     say("-New Expense_", "bold green")
#     amount = prompt_amount()
#     if amount is None:
#         say("Cancelled", "Yellow")
#         return
#
#     category = prompt_category()
#     note = prompt_note()
#
#     save(add_expense(load(), amount, category, note))
#     say(f"Added {amount: .2f} under '{category}'." , "green")
#     pause()
#
#
#
# def cmd_list() -> None:
#     items = load()
#     if not items:
#         say("\n no expenses found", "yellow")
#         pause()
#         return
#     items = sorted(items, key = lambda e:e["date"])
#     total = sum(e["amount"] for e in items)
#
#     if RICH:
#         table = Table(title = f"Expense ({len(items)})")
#         table.add_column("ID", justify = "right", style = "dim")
#         table.add_column("Date")
#         table.add_column("Category")
#         table.add_column("Amount", justify="right")
#         table.add_column("Note")
#
#         for e in items:
#             table.addrow(
#                 str(e["id"]),
#                 e["date"].replace("T", " "),
#                 e["category"],
#                 f"{e['amount']:.2f}",
#                 e.get("note") or ""
#             )
#         console.print(table)
#         console.print(f"Total: {total:.2f}", style = "bold green")
#     else:
#         print()
#         print(f"{'ID':>14} {'Date':<19} {'Category':>9} Note")
#         print("-" * 78)
#         for e in items:
#             print(
#                 f"{e['id']:>14}  {e['date'].replace('T', ' '):<19}  "
#                 f"{e['category']:<12}  {e['amount']:>9.2f}  {e.get('note') or ''}"
#             )
#         print("-" * 78)
#         print(f"Total: {total:.2f}")
#
#     pause()
#
#
#
#
#
#
# say("test message")
# load()
# # 120
# # 130
#



#!/usr/bin/env python3
"""expense_calculator.py — a tiny interactive personal expense tracker."""

# --------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------

# Store type hints as strings instead of evaluating them immediately.
# Lets `list[dict]` and `float | None` work on older Python versions.
from __future__ import annotations

# json — reads/writes expenses.json.
import json

# time — used to generate unique IDs and backup filenames.
import time

# datetime — stamps each expense with "when it was added".
from datetime import datetime

# Path — cross-platform file paths.
from pathlib import Path


# --------------------------------------------------------------------------
# OPTIONAL PRETTY OUTPUT — works fine without rich.
# --------------------------------------------------------------------------
try:
    # console = printer that understands styles like "[bold red]text[/]".
    from rich.console import Console
    # table = builds the box-drawing tables used in list/summary.
    from rich.table import Table

    RICH = True
    console = Console()
except ImportError:
    # rich isn't installed — fall back to plain print.
    RICH = False
    console = None


# Data file lives in the same folder as this script.
DATA_FILE = Path(__file__).resolve().with_name("expenses.json")


# --------------------------------------------------------------------------
# Tiny helper — every message goes through here, so the rest of the code
# doesn't have to care whether rich is installed.
# --------------------------------------------------------------------------
def say(msg: str = "", style: str | None = None) -> None:
    if RICH:
        console.print(msg, style=style)   # colored
    else:
        print(msg)                        # plain


# ==========================================================================
# DATA LAYER — pure functions, no input(), no print().
# ==========================================================================


def load() -> list[dict]:
    """Read expenses.json. Returns [] if missing or corrupt."""

    # First run: no file yet. That's normal, not an error.
    if not DATA_FILE.exists():
        return []

    try:
        # ------------------------------------------------------------------
        # THE `with` BLOCK
        # ------------------------------------------------------------------
        # `with X as f:` guarantees the file is CLOSED when the block ends —
        # even if an exception happens inside.
        #
        # Without `with`, a crash here would leave the file open, which
        # locks it on Windows (can't rename/delete until the program exits).
        #
        # DATA_FILE.open()      → returns a file handle
        # encoding="utf-8"      → read as UTF-8 (emoji, accents survive)
        # as f                  → name the handle `f`
        # ------------------------------------------------------------------
        with DATA_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
        # ↑ file is now closed automatically.

    except json.JSONDecodeError as exc:
        # File exists but isn't valid JSON (hand-edited, corrupted, etc.).
        # Move it aside — never silently wipe user data.
        backup = DATA_FILE.with_name(
            f"{DATA_FILE.stem}.corrupt-{int(time.time())}.json"
        )
        DATA_FILE.replace(backup)
        say(f"! {DATA_FILE.name} was not valid JSON ({exc}).", "bold red")
        say(f"  Moved it to {backup.name} and starting fresh.", "yellow")
        return []

    except OSError as exc:
        # Permission denied, disk full, file locked, etc.
        say(f"! Could not read {DATA_FILE.name}: {exc}", "bold red")
        return []

    # Our data is always a LIST of dicts. Refuse anything else.
    if not isinstance(data, list):
        say("! Unexpected data format; starting empty.", "bold red")
        return []
    return data


def save(items: list[dict]) -> None:
    """Write the list to disk atomically (temp file → rename)."""

    # Write to expenses.json.tmp first, then rename over expenses.json.
    # Why? If we crash mid-write, the ORIGINAL expenses.json is untouched.
    # The user never ends up with a half-written file.
    tmp = DATA_FILE.with_name(DATA_FILE.name + ".tmp")

    # ----------------------------------------------------------------------
    # THE `with` BLOCK — write mode
    # ----------------------------------------------------------------------
    # mode="w"     → create-or-overwrite
    # The file closes automatically when this block ends.
    # We write to `.tmp`, NOT to `expenses.json` directly.
    # ----------------------------------------------------------------------
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")
    # ↑ file closed here.

    # ----------------------------------------------------------------------
    # ATOMIC RENAME
    # ----------------------------------------------------------------------
    # Now that `tmp` is closed, we can rename it over `expenses.json`.
    # This would FAIL on Windows if the file were still open — that's
    # exactly why we used `with` above.
    # ----------------------------------------------------------------------
    tmp.replace(DATA_FILE)


def add_expense(
    items: list[dict],
    amount: float,
    category: str,
    note: str = "",
) -> list[dict]:
    """Return a NEW list with the expense appended."""
    expense = {
        "id": int(time.time() * 1000),                    # ms timestamp = unique-ish
        "amount": round(float(amount), 2),                # 12.50, not 12.4999999
        "category": category.strip().lower(),             # "Food " → "food"
        "note": note.strip(),
        "date": datetime.now().isoformat(timespec="seconds"),
    }
    # `+` on lists returns a new list — original is untouched.
    return items + [expense]


def summarize(items: list[dict]) -> dict[str, float]:
    """Category → total spent."""
    totals: dict[str, float] = {}
    for e in items:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return totals


def delete_expense(items: list[dict], expense_id: int) -> tuple[list[dict], bool]:
    """Return (new_list, was_removed)."""
    kept = [e for e in items if e["id"] != expense_id]
    removed = len(kept) != len(items)
    return kept, removed


# ==========================================================================
# INTERACTIVE LAYER — prompts and printing.
# ==========================================================================


def prompt_amount() -> float | None:
    """Ask until valid positive number. None = user cancelled."""
    while True:
        raw = input("  Amount (blank to cancel): ").strip()

        if not raw:
            return None                       # user bailed

        try:
            value = float(raw)
        except ValueError:
            say("  Not a number — try again (e.g. 12.50).", "yellow")
            continue                          # re-ask

        if value <= 0:
            say("  Amount must be greater than zero.", "yellow")
            continue                          # re-ask

        return value


def prompt_category() -> str:
    raw = input("  Category (e.g. food, transport; blank = other): ").strip()
    return raw.lower() if raw else "other"


def prompt_note() -> str:
    return input("  Note (optional): ").strip()


def pause() -> None:
    """Give the user time to read output before the menu reprints."""
    try:
        input("\nPress Enter to continue...")
    except EOFError:
        pass


def cmd_add() -> None:
    say()
    say("— New expense —", "bold")

    amount = prompt_amount()
    if amount is None:
        say("Cancelled.", "yellow")
        return

    category = prompt_category()
    note = prompt_note()

    # load → add_expense → save, in one expression.
    save(add_expense(load(), amount, category, note))
    say(f"Added {amount:.2f} under '{category}'.", "green")
    pause()


def cmd_list() -> None:
    items = load()
    if not items:
        say("\nNo expenses yet — add one first.", "yellow")
        pause()
        return

    items = sorted(items, key=lambda e: e["date"])     # oldest first
    total = sum(e["amount"] for e in items)

    if RICH:
        table = Table(title=f"Expenses ({len(items)})")
        table.add_column("ID", justify="right", style="dim")
        table.add_column("Date")
        table.add_column("Category")
        table.add_column("Amount", justify="right")
        table.add_column("Note")
        for e in items:
            table.add_row(
                str(e["id"]),
                e["date"].replace("T", " "),
                e["category"],
                f"{e['amount']:.2f}",
                e.get("note") or "",
            )
        console.print(table)
        console.print(f"Total: {total:.2f}", style="bold")
    else:
        print()
        print(f"{'ID':>14}  {'DATE':<19}  {'CATEGORY':<12}  {'AMOUNT':>9}  NOTE")
        print("-" * 78)
        for e in items:
            print(
                f"{e['id']:>14}  {e['date'].replace('T', ' '):<19}  "
                f"{e['category']:<12}  {e['amount']:>9.2f}  {e.get('note') or ''}"
            )
        print("-" * 78)
        print(f"Total: {total:.2f}")

    pause()


def cmd_summary() -> None:
    items = load()
    if not items:
        say("\nNo expenses yet.", "yellow")
        pause()
        return

    totals = summarize(items)
    grand = sum(totals.values())
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)

    if RICH:
        table = Table(title="Spending by category")
        table.add_column("Category")
        table.add_column("Total", justify="right")
        table.add_column("Share", justify="right")
        for cat, amt in ranked:
            table.add_row(cat, f"{amt:.2f}", f"{amt / grand * 100:.0f}%")
        console.print(table)
        console.print(f"Grand total: {grand:.2f}", style="bold")
    else:
        print()
        for cat, amt in ranked:
            print(f"  {cat:<14} {amt:>10.2f}  {amt / grand * 100:>3.0f}%")
        print("  " + "-" * 32)
        print(f"  {'TOTAL':<14} {grand:>10.2f}")

    pause()


def cmd_delete() -> None:
    items = load()
    if not items:
        say("\nNothing to delete.", "yellow")
        pause()
        return

    raw = input("  ID of the expense to delete (blank to cancel): ").strip()
    if not raw:
        say("Cancelled.", "yellow")
        return

    try:
        target = int(raw)
    except ValueError:
        say("  IDs are whole numbers.", "yellow")
        pause()
        return

    kept, removed = delete_expense(items, target)
    if not removed:
        say(f"  No expense with ID {target}.", "yellow")
        pause()
        return

    save(kept)
    say(f"Deleted expense {target}.", "green")
    pause()


# ==========================================================================
# MAIN LOOP
# ==========================================================================

MENU = """
========================================
  Spend tracker — what do you want to do?
========================================
  1) Add an expense
  2) List expenses
  3) Summary by category
  4) Delete an expense
  5) Quit
"""

# Menu key → function to call.
ACTIONS = {
    "1": cmd_add,
    "2": cmd_list,
    "3": cmd_summary,
    "4": cmd_delete,
}


def main() -> None:
    say(f"Data file: {DATA_FILE}", "dim")

    while True:
        say(MENU, "bold cyan")

        try:
            choice = input("  > ").strip()
        except EOFError:
            say("\nBye.", "green")
            return

        if choice in ("5", "q", "quit"):
            say("Bye.", "green")
            return

        action = ACTIONS.get(choice)
        if action is None:
            say("Not a valid choice — pick 1–5.", "yellow")
            continue

        action()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say("\nInterrupted — bye.", "green")