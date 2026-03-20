import random
from collections import defaultdict

# -----------------------------
# DATA
# -----------------------------
people = ["Hugo", "Ivan", "Emilio", "Christian", "William", "Ahmed", "Jesus"]
activities = ["QRewrite", "GWS", "iGA", "superroot", "assistant", "Mars", "LPM", "PolyQUS"]

heavy_activities = {"GWS", "Mars", "LPM"}
MIN_SKILLS = 6

# Vacations: week_index -> list of people OFF
vacations = {
    1: ["Ivan"],
    2: ["Ahmed"],
}

# -----------------------------
# SKILLS
# -----------------------------
def generate_valid_skills():
    while True:
        skills = {p: set(random.sample(activities, MIN_SKILLS)) for p in people}
        ok = True
        for act in activities:
            if sum(act in skills[p] for p in people) < 4:
                ok = False
                break
        if ok:
            return skills

# -----------------------------
# FEASIBILITY
# -----------------------------
def heavy_feasible(active_people):
    return len(active_people) >= 6

# -----------------------------
# SCORING
# -----------------------------
def score_schedule(schedule, prev_schedule):
    """Lower is better"""
    score = 0

    # penalties
    REPEAT_PRIMARY = 10
    REPEAT_PAIR = 6
    REPEAT_HEAVY = 8
    IMBALANCE = 2

    load = defaultdict(int)

    for act, roles in schedule.items():
        p = roles["primary"]
        s = roles["secondary"]

        load[p] += 1
        if s:
            load[s] += 0  # secondary doesn't count for imbalance here

        if prev_schedule:
            prev = prev_schedule.get(act, {})

            if p == prev.get("primary"):
                score += REPEAT_PRIMARY

            if (p, s) == (prev.get("primary"), prev.get("secondary")):
                score += REPEAT_PAIR

            if act in heavy_activities:
                if p in prev.values() or s in prev.values():
                    score += REPEAT_HEAVY

    # imbalance penalty
    vals = list(load.values())
    if vals:
        score += IMBALANCE * (max(vals) - min(vals))

    return score

# -----------------------------
# GENERATE ONE CANDIDATE
# -----------------------------
def generate_candidate(skills, active_people, prev_schedule):
    schedule = {}
    primary_count = {p: 0 for p in active_people}
    heavy_count = {p: 0 for p in active_people}

    feasible_heavy = heavy_feasible(active_people)

    for act in activities:
        eligible = [p for p in active_people if act in skills[p]]
        if len(eligible) < 1:
            return None

        random.shuffle(eligible)
        assigned = False

        for p in eligible:
            if primary_count[p] >= 2:
                continue

            for s in eligible:
                if p == s:
                    continue

                # heavy constraints
                if act in heavy_activities:
                    if heavy_count[p] >= 1:
                        continue

                    if feasible_heavy and heavy_count[s] >= 1:
                        continue

                # assign
                if act in heavy_activities and not feasible_heavy and heavy_count[s] >= 1:
                    schedule[act] = {"primary": p, "secondary": None}
                else:
                    schedule[act] = {"primary": p, "secondary": s}

                primary_count[p] += 1

                if act in heavy_activities:
                    heavy_count[p] += 1
                    if schedule[act]["secondary"]:
                        heavy_count[s] += 1

                assigned = True
                break

            if assigned:
                break

        if not assigned:
            return None

    return schedule

# -----------------------------
# OPTIMIZATION LOOP
# -----------------------------
def generate_schedule(skills, active_people, prev_schedule=None, trials=2000):
    best = None
    best_score = float("inf")

    if not heavy_feasible(active_people):
        print("WARNING: Not enough people for full heavy coverage → some secondaries will be None")

    for _ in range(trials):
        cand = generate_candidate(skills, active_people, prev_schedule)
        if not cand:
            continue

        s = score_schedule(cand, prev_schedule)

        if s < best_score:
            best = cand
            best_score = s

    if best is None:
        raise ValueError("No valid schedule found")

    return best

# -----------------------------
# MULTI-WEEK
# -----------------------------
def generate_weeks(num_weeks=4):
    skills = generate_valid_skills()
    weeks = []
    prev = None

    for w in range(num_weeks):
        off = vacations.get(w, [])
        active = [p for p in people if p not in off]

        print(f"\n>>> Week {w+1} OFF: {off if off else 'None'}")

        sched = generate_schedule(skills, active, prev)
        weeks.append(sched)
        prev = sched

    return skills, weeks

# -----------------------------
# PRINT
# -----------------------------
def print_skills(skills):
    print("\n=== SKILLS ===")
    for p, a in skills.items():
        print(f"{p:10}: {sorted(a)}")


def print_schedule(schedule, i):
    print(f"\n=== WEEK {i} ===")
    for act, r in schedule.items():
        sec = r['secondary'] if r['secondary'] else "None"
        print(f"{act:10} | P: {r['primary']:10} | S: {sec:10}")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    skills, weeks = generate_weeks(5)

    print_skills(skills)

    for i, w in enumerate(weeks, 1):
        print_schedule(w, i)

