import sqlite3
from datetime import datetime

# Path to your SQLite database
DB_PATH = "result.sqlite"
OUTPUT_FILE = "../pontok.html"

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
        f.write("<html><head>")
        f.write("""
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
          .score-table {
            border-collapse: collapse;
            font-family: Arial, sans-serif;
          }

          .score-table th {
            border: 1px solid #ccc;   /* thin, light gray */
            font-weight: normal;
            padding: 1px 10px;       /* vertical | horizontal */
          }
          
          .score-table td {
            border: 1px solid #ccc;   /* thin, light gray */
            padding: 1px 10px;       /* vertical | horizontal */
          }
          
          .score-table td:nth-child(2) {
            font-variant-numeric: tabular-nums;
            text-align: right;
          }
          
        </style>
        """)
        f.write("</head><body>")
        
        # Write timestamp
        timestamp = datetime.now().strftime("%Y.%m.%d %H:%M")
        f.write(f"Frissítve: {timestamp}<br>")

        if not rows:
            f.write("Error.<br>")
            return

        # Print header
        f.write("<br>")  # blank line before summary
        
        f.write("""
        <table class="score-table">
          <thead>
            <tr>
              <th>Összesítés</th>
              <th style='text-align:right'>Pont</th>
            </tr>
          </thead>
          <tbody>
        """)
        
        for user, total_points in rows:
            # Write row
            f.write(f"  <tr><td>{user}</td><td>{total_points}</td></tr>")

        f.write("</tbody></table>")
        f.write("<br>")  # blank line before rounds



    cursor.execute(QUERY)
    rows = cursor.fetchall()
    conn.close()

    # Open the output file
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        if not rows:
            f.write("Error.<br>")
            return

        current_round = None

        for user, round_num, total_points in rows:
            # Detect round change → new section
            if round_num != current_round:
                if current_round is not None:
                    f.write("</tbody></table>") # closing table of previous round
                    f.write("<br>")  # blank line between rounds

                current_round = round_num
                f.write(f"""
                <table class="score-table">
                   <thead>
                     <tr>
                       <th>Forduló: {round_num}</th>
                       <th style='text-align:right'>Pont</th>
                     </tr>
                   </thead>
                   <tbody>
                """)

            # Write row
            f.write(f"  <tr><td>{user}</td><td>{total_points}</td></tr>")

    print(f"Report written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
