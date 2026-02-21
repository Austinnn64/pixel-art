import os
import subprocess
from datetime import datetime, timedelta

TEXT = "AUSTIN"
START_DATE = datetime(2026, 2, 23)
COMMITS_PER_PIXEL = 4


FONT = {
    "A": [" 1 ", "1 1", "111", "1 1", "1 1", "   ", "   "],
    "U": ["1 1", "1 1", "1 1", "1 1", "111", "   ", "   "],
    "S": ["111", "1  ", "111", "  1", "111", "   ", "   "],
    "T": ["111", " 1 ", " 1 ", " 1 ", " 1 ", "   ", "   "],
    "I": ["111", " 1 ", " 1 ", " 1 ", "111", "   ", "   "],
    "N": ["1 1", "111", "111", "111", "1 1", "   ", "   "],
}


def build_matrix(text):
    matrix = [""] * 7
    for char in text:
        pattern = FONT.get(char.upper())
        if not pattern:
            continue
        for i in range(7):
            matrix[i] += pattern[i] + "  "
    return matrix


def generate_commits(matrix):
    for col in range(len(matrix[0])):
        for row in range(7):
            if matrix[row][col] == "1":
                date = START_DATE + timedelta(days=col * 7 + row)
                for _ in range(COMMITS_PER_PIXEL):
                    env = os.environ.copy()
                    d = date.strftime("%Y-%m-%dT12:00:00")
                    env["GIT_AUTHOR_DATE"] = d
                    env["GIT_COMMITTER_DATE"] = d
                    subprocess.run(
                        ["git", "commit", "--allow-empty", "-m", "pixel"],
                        env=env,
                    )


if __name__ == "__main__":
    matrix = build_matrix(TEXT)
    generate_commits(matrix)
    print("Done. Now run: git push")
