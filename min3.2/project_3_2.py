import math
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. CONFIGURATION PARAMETERS
# ==========================================
TOTAL_SPECTRUM_MHZ = 50.0
CHANNEL_BW_KHZ = 200.0
COVERAGE_AREA_KM2 = 1000.0
CELL_RADIUS_KM = 2.0  # Original cell radius

# Convert to consistent units
TOTAL_SPECTRUM_KHZ = TOTAL_SPECTRUM_MHZ * 1000
TOTAL_CHANNELS = TOTAL_SPECTRUM_KHZ / CHANNEL_BW_KHZ

# Area of a hexagon with radius R = (3 * sqrt(3) / 2) * R^2
def hex_area(R):
    return (3 * math.sqrt(3) / 2) * (R ** 2)

# ==========================================
# 2. CAPACITY CALCULATIONS
# ==========================================
def calculate_capacity(N, R):
    channels_per_cell = math.floor(TOTAL_CHANNELS / N)
    cell_area = hex_area(R)
    num_cells = math.floor(COVERAGE_AREA_KM2 / cell_area)
    total_capacity = channels_per_cell * num_cells
    Q = math.sqrt(3 * N)
    return channels_per_cell, num_cells, total_capacity, Q

def print_results():
    print("\n--- MINI PROJECT 3.2: CAPACITY PLANNING ---")
    print(f"Total Available Channels: {int(TOTAL_CHANNELS)}")
    print(f"Coverage Area: {COVERAGE_AREA_KM2} km²")
    print(f"Original Cell Radius: {CELL_RADIUS_KM} km\n")
    
    print(f"{'N':<5} | {'Q':<5} | {'Chan/Cell':<10} | {'Total Cells':<12} | {'Total Capacity':<15}")
    print("-" * 60)
    
    candidate_Ns = [1, 3, 4, 7]
    results = []
    
    for N in candidate_Ns:
        chan, cells, cap, Q = calculate_capacity(N, CELL_RADIUS_KM)
        print(f"{N:<5} | {Q:<5.2f} | {chan:<10} | {cells:<12} | {cap:<15}")
        results.append((N, Q, cap))
        
    print("\n--- CELL SPLITTING SCENARIO (Using N=7) ---")
    print(f"{'Radius (km)':<12} | {'Total Cells':<12} | {'Total Capacity':<15} | {'Capacity Gain':<15}")
    print("-" * 65)
    
    base_cap = calculate_capacity(7, CELL_RADIUS_KM)[2]
    
    for multiplier, label in [(1.0, "Original"), (0.5, "Splitting /2"), (0.25, "Splitting /4")]:
        new_R = CELL_RADIUS_KM * multiplier
        chan, cells, cap, Q = calculate_capacity(7, new_R)
        gain = cap / base_cap
        print(f"{new_R:<12.2f} | {cells:<12} | {cap:<15} | {gain:<15.1f}x")
        
    return results

# ==========================================
# 3. PLOTTING
# ==========================================
def plot_charts(results):
    Ns = [r[0] for r in results]
    Qs = [r[1] for r in results]
    caps = [r[2] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Chart 1: Capacity vs N
    ax1.plot(Ns, caps, marker='o', color='blue', linewidth=2, markersize=8)
    for i, txt in enumerate(caps):
        ax1.annotate(f"{txt}", (Ns[i], caps[i]), textcoords="offset points", xytext=(0,10), ha='center')
    ax1.set_title("Total System Capacity vs Reuse Factor (N)")
    ax1.set_xlabel("Reuse Factor (N)")
    ax1.set_ylabel("Total System Capacity (Channels)")
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(Ns)

    # Chart 2: Capacity vs Q
    ax2.plot(Qs, caps, marker='s', color='red', linewidth=2, markersize=8)
    for i, txt in enumerate(caps):
        ax2.annotate(f"N={Ns[i]}", (Qs[i], caps[i]), textcoords="offset points", xytext=(0,10), ha='center')
    ax2.set_title("Total System Capacity vs Co-channel Reuse Ratio (Q)")
    ax2.set_xlabel("Co-channel Reuse Ratio (Q)")
    ax2.set_ylabel("Total System Capacity (Channels)")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("capacity_charts.png", dpi=300, bbox_inches='tight')
    plt.show()

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    results = print_results()
    plot_charts(results)