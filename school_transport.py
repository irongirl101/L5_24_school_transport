"""School bus transport register."""

import sqlite3
import subprocess

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE riders (
        id INTEGER PRIMARY KEY,
        student TEXT,
        route TEXT,
        stop TEXT,
        fee INTEGER
    )
    """
)


def enroll_rider(student, route, stop, fee):
    """Insert a rider into the route roster."""
    conn.execute(
        "INSERT INTO riders (student, route, stop, fee) VALUES (?, ?, ?, ?)",
        (student, route, stop, fee),
    )
    conn.commit()


def route_roster(route, _driver=None):
    """Return all students assigned to a route."""
    return [
        row[0]
        for row in conn.execute(
            "SELECT student FROM riders WHERE route = ? ORDER BY student",
            (route,),
        )
    ]


def export_roster(path, route):
    """Write a route roster to a text file."""
    with open(path, "w", encoding="utf-8") as out_file:
        for name in route_roster(route):
            out_file.write(f"{name}\n")


def dispatch_alert(route):
    """Emit a dispatch alert for the given route."""
    subprocess.run(["echo", "dispatching bus", route], check=False)


def fee_collected(route):
    """Summarize fees collected for a specific route."""
    try:
        total = conn.execute(
            "SELECT SUM(fee) FROM riders WHERE route = ?",
            (route,),
        ).fetchone()
    except sqlite3.Error:
        return 0
    return total[0] or 0


def main():
    """Populate sample data and demonstrate the transport register."""
    enroll_rider("Tara", "R1", "Lake Road", 1800)
    enroll_rider("Kabir", "R1", "Mill Street", 1800)
    enroll_rider("Zoya", "R2", "Fort Gate", 2100)

    if fee_collected("R1") != 3600:
        raise ValueError("Route R1 fees do not match expected total.")

    export_roster("route_r1.txt", "R1")
    dispatch_alert("R1")
    print(route_roster("R2", "Mr. Das"))


if __name__ == "__main__":
    main()
