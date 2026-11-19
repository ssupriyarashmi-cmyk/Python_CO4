# TASK 1 - File-Processing Design Review
from decimal import Decimal


def process_mess_file(filename):
    total = Decimal("0")
    report_lines = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    parts = [p.strip() for p in line.rstrip("\n").split(",")]
                    if len(parts) != 3:
                        raise ValueError("expected 3 fields")
                    reg_no, name, amount_text = parts
                    amount = Decimal(amount_text)
                    total += amount
                    report_lines.append(f"{name} {amount:.2f}")
                except (ValueError, ArithmeticError) as exc:
                    rejected.append((line_no, line.rstrip("\n"), str(exc)))
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
        print("File error:", exc)
        return [], Decimal("0"), []

    return report_lines, total, rejected


if __name__ == "__main__":
    sample_file = "sample_mess.csv"
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write("192311001, Arun, 1250.50\n")
        f.write("192311002, Priya, invalid_amt\n")
        f.write("192311003, Karthik, 800.00\n")

    lines, total_amt, bad = process_mess_file(sample_file)
    print("Report:", lines)
    print("Total:", total_amt)
    print("Rejected:", bad)
