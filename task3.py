# TASK 3 - Design the Error Handling


class InvalidRecord(Exception):
    """Raised when an attendance line is invalid."""
    pass


def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, date, status = parts
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    return register, date, status


def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    _, _, status = parse_line(line)
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
                except InvalidRecord as exc:
                    errors.append((line_no, str(exc)))
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
        raise InvalidRecord(f"cannot process {path}: {exc}") from exc
    else:
        return present, absent, errors
    finally:
        pass


if __name__ == "__main__":
    sample_path = "sample_attendance_t3.csv"
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write("192311001,2026-10-08,P\n")
        f.write("192311002,2026-10-08,A\n")
        f.write("192311003,2026-10-08\n")
        f.write("192311004,2026-10-08,L\n")

    print(summarise(sample_path))
