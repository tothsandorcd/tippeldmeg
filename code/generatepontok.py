import sqlite3
from datetime import datetime

# Path to your SQLite database
DB_PATH = "result.sqlite"
OUTPUT_FILE = "../pontok.txt"

# SQL query (cleaned)
QUERY = """
SELECT user, round, SUM(point) AS total_points
FROM points
GROUP BY user, round
ORDER BY round DESC, total_points DESC, user;
"""
QUERY_SUM = """
SELECT user, SUM(point) AS total_points
FROM points
GROUP BY user
ORDER BY total_points DESC, user;
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(QUERY_SUM)
    rows = cursor.fetchall()

    # Open the output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Write timestamp
        timestamp = datetime.now().strftime("%Y.%m.%d %H:%M")
        f.write(f"Frissítve: {timestamp}\n")

        if not rows:
            f.write("Error.\n")
            return

        # Print header
        f.write("\n")  # blank line before summary
        f.write(f"Összesítés:\n")
        f.write("-" * 14 + "\n")

        for user, total_points in rows:
            # Write row
            f.write(f"{user:<9} {total_points:>4}\n")

        f.write("\n")  # blank line before rounds

    cursor.execute(QUERY)
    rows = cursor.fetchall()
    conn.close()

    # Open the output file
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        if not rows:
            f.write("Error.\n")
            return

        current_round = None

        for user, round_num, total_points in rows:
            # Detect round change → new section
            if round_num != current_round:
                if current_round is not None:
                    f.write("\n")  # blank line between rounds
                current_round = round_num
                f.write(f"Forduló: {round_num}\n")
                f.write("-" * 14 + "\n")

            # Write row
            f.write(f"{user:<9} {total_points:>4}\n")

    print(f"Report written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
