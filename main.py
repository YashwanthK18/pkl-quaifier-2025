import itertools
from collections import defaultdict

# --- Current Points Table ---
teams = {
    "Puneri Paltan": 26,
    "Dabang Delhi K.C.": 24,
    "Telugu Titans": 16,
    "Bengaluru Bulls": 16,
    "U Mumba": 16,
    "Tamil Thalaivas": 12,
    "Haryana Steelers": 16,
    "Jaipur Pink Panthers": 12,
    "Gujarat Giants": 12,
    "UP Yoddhas": 12,
    "Bengal Warriorz": 10,
    "Patna Pirates": 8
}

matches = [
    ("Bengal Warriorz", "Patna Pirates"),
    ("Tamil Thalaivas", "Dabang Delhi K.C."),
    ("Jaipur Pink Panthers", "UP Yoddhas"),
    ("Bengaluru Bulls", "Dabang Delhi K.C."),
    ("Telugu Titans", "Puneri Paltan"),
    ("Bengal Warriorz", "Jaipur Pink Panthers"),
    ("Telugu Titans", "Gujarat Giants"),
    ("U Mumba", "Haryana Steelers"),
    ("Patna Pirates", "Puneri Paltan"),
    ("Bengal Warriorz", "Tamil Thalaivas"),
    ("U Mumba", "Jaipur Pink Panthers"),
    ("Haryana Steelers", "Gujarat Giants"),
    ("Haryana Steelers", "Telugu Titans"),
    ("Bengaluru Bulls", "Bengal Warriorz"),
    ("Dabang Delhi K.C.", "Patna Pirates"),
    ("Bengaluru Bulls", "Gujarat Giants"),
    ("UP Yoddhas", "U Mumba"),
    ("Patna Pirates", "Jaipur Pink Panthers"),
]

qualification = defaultdict(float)
top2 = defaultdict(float)
pos3_4 = defaultdict(float)
pos5_8 = defaultdict(float)

team_names = list(teams.keys())
num_matches = len(matches)

# --- Function to distribute slots fairly at tie boundaries ---
def distribute_slots(sorted_points, total_slots, target_dict):
    if total_slots > len(sorted_points):
        total_slots = len(sorted_points)
    cutoff_points = sorted_points[total_slots - 1][1]
    above = [(t, p) for t, p in sorted_points if p > cutoff_points]
    tied = [(t, p) for t, p in sorted_points if p == cutoff_points]
    remaining_slots = total_slots - len(above)
    share = remaining_slots / len(tied) if tied else 0
    for t, _ in above:
        target_dict[t] += 1
    for t, _ in tied:
        target_dict[t] += share

# --- Generate all possible outcomes ---
# Each match has 2 outcomes, so use itertools.product
for outcome in itertools.product([0, 1], repeat=num_matches):
    points = teams.copy()
    for i, result in enumerate(outcome):
        winner = matches[i][result]  # 0 → team A wins, 1 → team B wins
        points[winner] += 2

    sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
    distribute_slots(sorted_points, 8, qualification)
    distribute_slots(sorted_points, 2, top2)
    distribute_slots(sorted_points[2:], 2, pos3_4)
    distribute_slots(sorted_points[4:], 4, pos5_8)

total_simulations = 2 ** num_matches

# --- Convert to percentages ---
def pct(value): return round(100 * value / total_simulations, 2)

summary = []
for team in team_names:
    summary.append({
        "Team": team,
        "Qualification Chances": pct(qualification[team]),
        "Top 2": pct(top2[team]),
        "Pos 3-4": pct(pos3_4[team]),
        "Pos 5-8": pct(pos5_8[team])
    })

summary.sort(key=lambda x: x["Qualification Chances"], reverse=True)

# --- Display table ---
print(f"{'Team':25s} {'Qualification%':>16s} {'Top 2%':>10s} {'Pos 3-4%':>10s} {'Pos 5-8%':>10s}")
print("-" * 80)
total_qualify = 0
for s in summary:
    total_qualify += s["Qualification Chances"]
    print(f"{s['Team']:25s} {s['Qualification Chances']:16.2f} {s['Top 2']:10.2f} {s['Pos 3-4']:10.2f} {s['Pos 5-8']:10.2f}")

print("-" * 80)
