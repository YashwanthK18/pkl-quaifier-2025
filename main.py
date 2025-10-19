import itertools
from collections import defaultdict
import random

# --- Current Points Table ---
teams = {
    "Puneri Paltan": 26,
    "Dabang Delhi K.C.": 26,
    "Telugu Titans": 18,
    "Bengaluru Bulls": 18,
    "U Mumba": 16,
    "Tamil Thalaivas": 12,
    "Haryana Steelers": 16,
    "Jaipur Pink Panthers": 16,
    "Gujarat Giants": 12,
    "UP Yoddhas": 12,
    "Bengal Warriorz": 10,
    "Patna Pirates": 10
}

# --- Remaining Matches ---
matches = [
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

team_names = list(teams.keys())
num_matches = len(matches)
total_simulations = 2 ** num_matches
num_iterations = 100  # <-- Run 25 full simulations

# --- Aggregated Averages ---
avg_qualification = defaultdict(float)
avg_top2 = defaultdict(float)
avg_pos3_4 = defaultdict(float)
avg_pos5_8 = defaultdict(float)

def simulate_once():
    qualification = defaultdict(float)
    top2 = defaultdict(float)
    pos3_4 = defaultdict(float)
    pos5_8 = defaultdict(float)

    # --- Iterate through all match outcomes ---
    for outcome in itertools.product([0, 1], repeat=num_matches):
        points = teams.copy()
        point_diff = {team: 0 for team in team_names}

        for i, result in enumerate(outcome):
            winner = matches[i][result]
            loser = matches[i][1 - result]
            points[winner] += 2

            # Random PD difference
            diff = random.randint(0, 20)
            point_diff[winner] += diff
            point_diff[loser] -= diff

        # Sort standings by points then PD
        sorted_points = sorted(points.items(), key=lambda x: (x[1], point_diff[x[0]]), reverse=True)

        # Top slots
        for team, _ in sorted_points[:8]:
            qualification[team] += 1
        for team, _ in sorted_points[:2]:
            top2[team] += 1
        for team, _ in sorted_points[2:4]:
            pos3_4[team] += 1
        for team, _ in sorted_points[4:8]:
            pos5_8[team] += 1

    # Convert to percentages
    def pct(val): return 100 * val / total_simulations

    results = {}
    for t in team_names:
        results[t] = {
            "Qualification": pct(qualification[t]),
            "Top2": pct(top2[t]),
            "Pos3_4": pct(pos3_4[t]),
            "Pos5_8": pct(pos5_8[t])
        }
    return results


# --- Run 25 Iterations and Average ---
for _ in range(num_iterations):
    res = simulate_once()
    for t in team_names:
        avg_qualification[t] += res[t]["Qualification"]
        avg_top2[t] += res[t]["Top2"]
        avg_pos3_4[t] += res[t]["Pos3_4"]
        avg_pos5_8[t] += res[t]["Pos5_8"]

# --- Average Across Iterations ---
for t in team_names:
    avg_qualification[t] /= num_iterations
    avg_top2[t] /= num_iterations
    avg_pos3_4[t] /= num_iterations
    avg_pos5_8[t] /= num_iterations

# --- Prepare Final Table ---
summary = []
for team in team_names:
    summary.append({
        "Team": team,
        "Qualification Chances": round(avg_qualification[team], 2),
        "Top 2": round(avg_top2[team], 2),
        "Pos 3-4": round(avg_pos3_4[team], 2),
        "Pos 5-8": round(avg_pos5_8[team], 2)
    })

summary.sort(key=lambda x: x["Qualification Chances"], reverse=True)

# --- Display Table ---
print(f"{'Team':25s} {'Qualification%':>16s} {'Top 2%':>10s} {'Pos 3-4%':>10s} {'Pos 5-8%':>10s}")
print("-" * 80)
for s in summary:
    print(f"{s['Team']:25s} {s['Qualification Chances']:16.2f} {s['Top 2']:10.2f} {s['Pos 3-4']:10.2f} {s['Pos 5-8']:10.2f}")
print("-" * 80)
