import random
from collections import defaultdict

# --- Current Points Table ---
teams = {
    "Puneri Paltan": 24,
    "Dabang Delhi K.C.": 24,
    "Telugu Titans": 16,
    "Bengaluru Bulls": 16,
    "U Mumba": 14,
    "Tamil Thalaivas": 12,
    "Haryana Steelers": 14,
    "Jaipur Pink Panthers": 12,
    "Gujarat Giants": 10,
    "UP Yoddhas": 12,
    "Bengal Warriorz": 8,
    "Patna Pirates": 8,
}

# --- Remaining Matches ---
matches = [
    ("Telugu Titans", "Bengal Warriorz"),
    ("Jaipur Pink Panthers", "Puneri Paltan"),
    ("Gujarat Giants", "Tamil Thalaivas"),
    ("Bengaluru Bulls", "Patna Pirates"),
    ("Telugu Titans", "U Mumba"),
    ("UP Yoddhas", "Haryana Steelers"),
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

# --- Simulation Parameters ---
SIMULATIONS = 2000000  # Try 200k (≈ few seconds), can increase up to 1M

top2 = defaultdict(int)
top8 = defaultdict(int)
pos3_4 = defaultdict(int)
pos5_8 = defaultdict(int)

team_names = list(teams.keys())

for _ in range(SIMULATIONS):
    points = teams.copy()

    for a, b in matches:
        # Randomly pick a winner (50/50)
        winner = random.choice([a, b])
        points[winner] += 2

    # Rank teams by points (descending)
    ranked = sorted(points.items(), key=lambda x: x[1], reverse=True)
    ranks = {team: i+1 for i, (team, _) in enumerate(ranked)}

    for team, rank in ranks.items():
        if rank <= 2:
            top2[team] += 1
        if rank <= 8:
            top8[team] += 1
        if rank in [3, 4]:
            pos3_4[team] += 1
        if rank in [5, 6, 7, 8]:
            pos5_8[team] += 1

# --- Compute Probabilities ---
def pct(count): return round(100 * count / SIMULATIONS, 2)

summary = []
for team in team_names:
    summary.append({
        "Team": team,
        "Top 2": pct(top2[team]),
        "Top 8": pct(top8[team]),
        "Pos 3-4": pct(pos3_4[team]),
        "Pos 5-8": pct(pos5_8[team])
    })

# Sort teams by Top 6 chances
summary.sort(key=lambda x: x["Top 8"], reverse=True)

# --- Display Results ---
print(f"{'Team':25s} {'Top 8%':>11s} {'Qualifier':>13s} {'Mini Qualifier':>15s} {'Play In':>8s}")
print("-"*88)
for s in summary:
    print(f"{s['Team']:25s} {s['Top 8']:11.2f} {s['Top 2']:11.2f} {s['Pos 3-4']:13.2f} {s['Pos 5-8']:11.2f}")
