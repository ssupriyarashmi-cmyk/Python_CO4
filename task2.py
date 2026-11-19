# TASK 2 - Biometric Attendance Files
from pathlib import Path


def process_attendance_folder(folder, report_file="attendance_report.txt", error_file="attendance_errors.log"):
    attendance = {}
    errors = []

    for file_path in sorted(Path(folder).glob("*.csv")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    parts = [p.strip() for p in line.rstrip("\n").split(",")]
                    if len(parts) != 3:
                        errors.append(f"{file_path.name}:{line_no} - expected 3 fields")
                        continue
                    register, date, status = parts
                    if status not in ("P", "A"):
                        errors.append(f"{file_path.name}:{line_no} - invalid status '{status}'")
                        continue
                    if register not in attendance:
                        attendance[register] = [0, 0]
                    if status == "P":
                        attendance[register][0] += 1
                    else:
                        attendance[register][1] += 1
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
            errors.append(f"{file_path.name} - file error: {exc}")

    with open(report_file, "w", encoding="utf-8") as rep:
        rep.write("Register,Present,Absent,Percentage,Status\n")
        for register, (present, absent) in sorted(attendance.items()):
            total = present + absent
            percentage = (present / total) * 100 if total > 0 else 0.0
            flag = "BELOW 75%" if percentage < 75 else "OK"
            rep.write(f"{register},{present},{absent},{percentage:.2f}%,{flag}\n")

    with open(error_file, "w", encoding="utf-8") as err:
        for record in errors:
            err.write(record + "\n")

    return attendance, errors


if __name__ == "__main__":
    demo_dir = Path("attendance_demo")
    demo_dir.mkdir(exist_ok=True)
    (demo_dir / "day1.csv").write_text(
        "192311001,2026-10-08,P\n192311002,2026-10-08\n192311003,2026-10-08,A\n",
        encoding="utf-8",
    )
    att, errs = process_attendance_folder(demo_dir)
    print("Attendance:", att)
    print("Errors:", errs)
