import itertools
from collections import defaultdict
import random

# --- Current Points Table ---
teams = {
    "Puneri Paltan": 26,
    "Dabang Delhi K.C.": 26,
    "Telugu Titans": 20,
    "Bengaluru Bulls": 20,
    "U Mumba": 20,
    "Tamil Thalaivas": 12,
    "Haryana Steelers": 20,
    "Jaipur Pink Panthers": 16,
    "Gujarat Giants": 12,
    "UP Yoddhas": 12,
    "Bengal Warriorz": 12,
    "Patna Pirates": 14
}

# --- Current Point Difference ---
initial_point_diff = {
    "Puneri Paltan": 88,
    "Dabang Delhi K.C.": 73,
    "Telugu Titans": 45,
    "U Mumba": 11,
    "Bengaluru Bulls": 69,
    "Haryana Steelers": 40,
    "Jaipur Pink Panthers": -33,
    "Gujarat Giants": -45,
    "Tamil Thalaivas": -36,
    "Patna Pirates": -40,
    "UP Yoddhas": -68,
    "Bengal Warriorz": -104
}

# --- Remaining Matches ---
matches = [
    ("Bengaluru Bulls", "Gujarat Giants"),
    ("UP Yoddhas", "U Mumba"),
    ("Patna Pirates", "Jaipur Pink Panthers"),
]

team_names = list(teams.keys())
num_matches = len(matches)
total_simulations = 2 ** num_matches
num_iterations = 1000  # <-- Run 100 full simulations

# --- Aggregated Averages ---
avg_qualification = defaultdict(float)
# --- MODIFICATION: Renamed variables ---
avg_qualifiers = defaultdict(float)  # Was avg_top2
avg_mini_qualifiers = defaultdict(float)  # Was avg_pos3_4
avg_play_ins = defaultdict(float)  # Was avg_pos5_8


def simulate_once():
    qualification = defaultdict(float)
    # --- MODIFICATION: Renamed variables ---
    qualifiers = defaultdict(float)
    mini_qualifiers = defaultdict(float)
    play_ins = defaultdict(float)

    # --- Iterate through all match outcomes ---
    for outcome in itertools.product([0, 1], repeat=num_matches):
        points = teams.copy()
        point_diff = initial_point_diff.copy()

        for i, result in enumerate(outcome):
            winner = matches[i][result]
            loser = matches[i][1 - result]
            points[winner] += 2

            # Random PD difference for the match
            diff = random.randint(0, 25)
            point_diff[winner] += diff
            point_diff[loser] -= diff

        # Sort standings by points then PD
        sorted_points = sorted(points.items(), key=lambda x: (x[1], point_diff[x[0]]), reverse=True)

        # Top slots
        for team, _ in sorted_points[:8]:
            qualification[team] += 1

        # --- MODIFICATION: Use new variable names ---
        for team, _ in sorted_points[:2]:
            qualifiers[team] += 1
        for team, _ in sorted_points[2:4]:
            mini_qualifiers[team] += 1
        for team, _ in sorted_points[4:8]:
            play_ins[team] += 1

    # Convert to percentages
    def pct(val):
        return 100 * val / total_simulations

    results = {}
    for t in team_names:
        # --- MODIFICATION: Use new dictionary keys ---
        results[t] = {
            "Qualification": pct(qualification[t]),
            "Qualifiers": pct(qualifiers[t]),
            "Mini-Qualifiers": pct(mini_qualifiers[t]),
            "Play-ins": pct(play_ins[t])
        }
    return results


# --- Run N Iterations and Average ---
for i in range(num_iterations):
    res = simulate_once()
    for t in team_names:
        # --- MODIFICATION: Aggregate using new keys/variables ---
        avg_qualification[t] += res[t]["Qualification"]
        avg_qualifiers[t] += res[t]["Qualifiers"]
        avg_mini_qualifiers[t] += res[t]["Mini-Qualifiers"]
        avg_play_ins[t] += res[t]["Play-ins"]

# --- Average Across Iterations ---
for t in team_names:
    # --- MODIFICATION: Average using new variables ---
    avg_qualification[t] /= num_iterations
    avg_qualifiers[t] /= num_iterations
    avg_mini_qualifiers[t] /= num_iterations
    avg_play_ins[t] /= num_iterations

# --- Prepare Final Table ---
summary = []
for team in team_names:
    # --- MODIFICATION: Build summary with new keys ---
    summary.append({
        "Team": team,
        "Qualification Chances": round(avg_qualification[team], 2),
        "Qualifiers": round(avg_qualifiers[team], 2),
        "Mini-Qualifiers": round(avg_mini_qualifiers[team], 2),
        "Play-ins": round(avg_play_ins[team], 2)
    })

summary.sort(key=lambda x: x["Qualification Chances"], reverse=True)

# --- MODIFICATION: Updated print header ---
print(f"{'Team':25s} {'Qualification%':>16s} {'Qualifiers%':>13s} {'Mini-Qualifiers%':>18s} {'Play-ins%':>12s}")
print("-" * 86)  # Adjusted line length
for s in summary:
    # --- MODIFICATION: Print using new keys ---
    print(
        f"{s['Team']:25s} {s['Qualification Chances']:16.2f} {s['Qualifiers']:13.2f} {s['Mini-Qualifiers']:18.2f} {s['Play-ins']:12.2f}")
print("-" * 86)  # Adjusted line length