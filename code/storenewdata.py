import re
from collections import defaultdict
from datetime import datetime
import sqlite3

# Input HTML file
input_file = "page_actual.html"

# Regex patterns
pont_pattern = re.compile(r'<div class="col-4">(\d+)\s+pont</div>')
user_pattern = re.compile(r'href="usertipp\?azon=\d+">([^<]+)</a>')
round_pattern = re.compile(r'<b>(\d+)\. forduló')

last_user = None
current_round = None
conn = sqlite3.connect("result.sqlite")
cursor = conn.cursor()
newly_added = 0

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        # Check if line contains a round
        round_match = round_pattern.search(line)
        if round_match:
            current_round = int(round_match.group(1))

        # Check if line contains a user link
        user_match = user_pattern.search(line)
        if user_match:
            last_user = user_match.group(1).strip()

        # Check if line contains points
        pont_match = pont_pattern.search(line)
        if pont_match and last_user and current_round is not None:
            points = int(pont_match.group(1))
            print(f"newly added round: {current_round} user: {last_user} points: {points}")
            cursor.execute("INSERT INTO points (user, round, point) VALUES (?,?,?)", (last_user, current_round, points))
            conn.commit()
            newly_added += 1

conn.close()
print(f"newly added records: {newly_added}")

