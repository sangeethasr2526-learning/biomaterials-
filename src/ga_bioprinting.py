# ============================================================
# GA-Based Optimization of Bioprinting Parameters (Terminal)
# Dataset: CECT Bioprinting Database
# ============================================================

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import os
import sys

# ------------------------------------------------------------
# 1. Paths
# ------------------------------------------------------------

ROOT_DIR = r"C:\Users\SANGEETHA SUNDAR\Downloads\sem-4-projects\biomaterials"
DATA_PATH = os.path.join(ROOT_DIR, "data", "cect-3d-printing-db-all-materials.csv")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

# ------------------------------------------------------------
# 2. Load Dataset
# ------------------------------------------------------------

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print("❌ Dataset not found. Check DATA_PATH.")
    sys.exit()

# ------------------------------------------------------------
# 3. Data Cleaning Functions
# ------------------------------------------------------------

def parse_pressure(p):
    if pd.isna(p):
        return None
    p = str(p).lower()
    try:
        if "bar" in p:
            nums = [float(x) for x in p.replace("bar", "").split("-")]
            return np.mean(nums) * 100  # bar → kPa
        if "kpa" in p:
            nums = [float(x) for x in p.replace("kpa", "").split("-")]
            return np.mean(nums)
    except:
        return None
    return None

def parse_speed(s):
    try:
        return float(s)
    except:
        return None

def parse_needle(n):
    if pd.isna(n):
        return None
    n = str(n).lower()
    if "µm" in n:
        return float(n.split("µm")[0])
    if "gauge" in n:
        return 400
    return None

def parse_cells(c):
    if pd.isna(c):
        return 0
    nums = [float(s) for s in str(c).split() if s.replace('.', '').isdigit()]
    return nums[0] if nums else 0

# ------------------------------------------------------------
# 4. Apply Cleaning
# ------------------------------------------------------------

df["Pressure_kPa"] = df["Pressure"].apply(parse_pressure)
df["Speed_mm_s"] = df["Speed (mm/s)"].apply(parse_speed)
df["Needle_um"] = df["Needle"].apply(parse_needle)
df["Cells_e6_ml"] = df["Cells (e6/ml)"].apply(parse_cells)

df_clean = df.dropna(subset=["Pressure_kPa", "Speed_mm_s", "Needle_um"])

print("\n✅ Clean dataset size:", len(df_clean))

# ------------------------------------------------------------
# 5. Parameter Ranges
# ------------------------------------------------------------

pressure_range = (df_clean["Pressure_kPa"].min(), df_clean["Pressure_kPa"].max())
speed_range = (df_clean["Speed_mm_s"].min(), df_clean["Speed_mm_s"].max())
needle_range = (df_clean["Needle_um"].min(), df_clean["Needle_um"].max())
cells_range = (0, df_clean["Cells_e6_ml"].max())

print("\n📊 PARAMETER RANGES FROM DATASET")
print(f"Pressure     : {pressure_range[0]:.2f} – {pressure_range[1]:.2f} kPa")
print(f"Speed        : {speed_range[0]:.2f} – {speed_range[1]:.2f} mm/s")
print(f"Needle Size  : {needle_range[0]:.0f} – {needle_range[1]:.0f} µm")
print(f"Cell Density : 0 – {cells_range[1]:.2f} ×10⁶ cells/ml")

# ------------------------------------------------------------
# 6. User Input (Terminal)
# ------------------------------------------------------------

print("\n🧑‍🔬 ENTER YOUR PREFERENCE (press Enter to skip)")

try:
    target_speed = input("Preferred speed (mm/s): ")
    target_speed = float(target_speed) if target_speed else np.mean(speed_range)
except:
    target_speed = np.mean(speed_range)

try:
    max_pressure = input("Maximum allowed pressure (kPa): ")
    max_pressure = float(max_pressure) if max_pressure else pressure_range[1]
except:
    max_pressure = pressure_range[1]

# ------------------------------------------------------------
# 7. Fitness Function
# ------------------------------------------------------------

def fitness(ind):
    pressure, speed, needle, cells = ind

    if pressure > max_pressure:
        return -999  # hard constraint

    cell_safety = (1 / (pressure + 1)) + (needle / needle_range[1])
    speed_match = np.exp(-abs(speed - target_speed))
    cell_penalty = -0.05 * cells

    return cell_safety + speed_match + cell_penalty

# ------------------------------------------------------------
# 8. Genetic Algorithm
# ------------------------------------------------------------

POP_SIZE = 40
GENERATIONS = 25
MUTATION_RATE = 0.2

def random_individual():
    return [
        random.uniform(*pressure_range),
        random.uniform(*speed_range),
        random.uniform(*needle_range),
        random.uniform(*cells_range)
    ]

population = [random_individual() for _ in range(POP_SIZE)]
fitness_history = []

print("\n🚀 RUNNING GENETIC ALGORITHM\n")

for gen in range(GENERATIONS):
    population = sorted(population, key=fitness, reverse=True)
    best_fit = fitness(population[0])
    fitness_history.append(best_fit)

    print(
        f"Generation {gen+1:02d} | "
        f"Best Fitness: {best_fit:.4f} | "
        f"Pressure: {population[0][0]:.1f} kPa | "
        f"Speed: {population[0][1]:.1f} mm/s"
    )

    new_population = population[:5]  # elitism

    while len(new_population) < POP_SIZE:
        p1, p2 = random.sample(population[:20], 2)
        cut = random.randint(1, 3)
        child = p1[:cut] + p2[cut:]

        if random.random() < MUTATION_RATE:
            idx = random.randint(0, 3)
            child[idx] *= random.uniform(0.9, 1.1)

        new_population.append(child)

    population = new_population

# ------------------------------------------------------------
# 9. Final Result
# ------------------------------------------------------------

best = max(population, key=fitness)

print("\n✅ OPTIMIZED BIOPRINTING PARAMETERS")
print(f"Pressure      : {best[0]:.2f} kPa")
print(f"Speed         : {best[1]:.2f} mm/s")
print(f"Needle        : {best[2]:.0f} µm")
print(f"Cell Density  : {best[3]:.2f} ×10⁶ cells/ml")

# ------------------------------------------------------------
# 10. Plot & Save Convergence
# ------------------------------------------------------------

plt.figure()
plt.plot(fitness_history, marker='o')
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("GA Convergence Curve")
plt.grid(True)

plot_path = os.path.join(RESULTS_DIR, "ga_convergence.png")
plt.savefig(plot_path)
plt.show()

print("\n📈 Convergence plot saved at:", plot_path)
