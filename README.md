# Qualitest

# 🗂️ Workgroup Activity Scheduler

This project implements a **constraint-based and optimization-driven scheduler** for assigning activities within a workgroup.

It ensures:
- Full activity coverage
- Fair workload distribution
- Robustness to absences (vacations)
- Smooth rotation across weeks

---

# 🧠 Core Idea

Each week, the system assigns:

- **Primary** → main responsible person  
- **Secondary** → backup (if feasible)

The scheduler:
1. Generates many valid schedules
2. Scores them based on quality
3. Selects the **best schedule**

---

# 🔒 HARD CONSTRAINTS (Always Enforced)

These rules are **never violated**.

## 👤 Maximum Primary Load
- A person cannot be **Primary in more than 2 activities per week**

---

## 👥 Valid Assignments
For each activity:
- Primary ≠ Secondary  
- Both must **know the activity**

---

## 🧠 Skill Requirement
- A person can only be assigned to activities they are trained in

---

## 🏖️ Vacations / Availability
- People marked as “off” are:
  - Completely excluded from scheduling

Example:
```python
vacations = {
    1: ["Ivan"],
    2: ["Ahmed"]
}
```
---

## ⚖️ Heavy Activity Constraint
Heavy activities:
GWS
Mars
LPM
Rule:
Each person can handle at most 1 heavy activity per week

---

## ⚠️ Feasibility Fallback
- If there are not enough people (e.g. due to vacations):
- The system detects infeasibility:
- heavy slots = 6 (3 activities × 2 roles)
- capacity = number of active people
- If infeasible:
✅ Always assign Primary
❌ Allow Secondary = None
- Example:
GWS   | P: Hugo   | S: None



---

## ⚙️ SOFT CONSTRAINTS (Optimized via Scoring)
- These are not strictly enforced, but minimized using penalties.
📊 SCORING SYSTEM
- The scheduler assigns a score to each candidate schedule.
- Lower score = better schedule
Penalties:
- Condition	Penalty
- Same primary as previous week	+10
- Same (primary, secondary) pair	+6
- Same person repeats same heavy activity	+8
- Load imbalance	+2 × (max_primary - min_primary)

---

## 💡 Future Improvements
- Multi-week memory (beyond previous week)
- Priority ranking of activities
- Deterministic scheduling (fixed seed)




