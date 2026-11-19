# TASK 4 - File and Exception Forensics


def append_return(log_file, record):
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(record + "\n")
    except (PermissionError, OSError) as exc:
        with open("errors.log", "a", encoding="utf-8") as err:
            err.write(f"Failed to write return: {exc}\n")
        raise


if __name__ == "__main__":
    append_return("daily_returns.log", "2026-11-19 | ITEM-101 | Qty: 2")
    append_return("daily_returns.log", "2026-11-19 | ITEM-205 | Qty: 1")
    with open("daily_returns.log", "r", encoding="utf-8") as f:
        print("Log contents:\n" + f.read())
