import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

# ==========================================
# PART A: HEXAGONAL FREQUENCY REUSE PLANNING
# ==========================================
def get_hex_centers(rings, R):
    centers = []
    for q in range(-rings, rings + 1):
        for r in range(max(-rings, -q - rings), min(rings, -q + rings) + 1):
            x = R * np.sqrt(3) * (q + r / 2)
            y = R * 1.5 * r
            centers.append((x, y, q, r))
    return centers

def plot_reuse_pattern(N, i, j, R=1.0, rings=2):
    fig, ax = plt.subplots(figsize=(5, 5))
    centers = get_hex_centers(rings, R)
    
    offset_q, offset_r = i, j
    
    for x, y, q, r in centers:
        freq_group = (q * offset_r - r * offset_q) % N
        color = plt.cm.tab20(freq_group / max(N, 1))
        
        hexagon = RegularPolygon((x, y), numVertices=6, radius=R, 
                                 orientation=np.pi/6, facecolor=color, edgecolor='k', alpha=0.7)
        ax.add_patch(hexagon)
        ax.text(x, y, str(freq_group + 1), ha='center', va='center', fontsize=8, fontweight='bold')

    ax.set_aspect('equal')
    Q = np.sqrt(3 * N)
    ax.set_title(f"Reuse Pattern: N = {N}, Q = {Q:.2f}")
    plt.axis('off')
    
    # SAVE THE FIGURE BEFORE SHOWING
    plt.savefig(f"hexagon_N{N}.png", dpi=300, bbox_inches='tight')
    plt.show()

def run_part_a():
    print("\n--- PART A: Frequency Reuse Layouts ---")
    configs = {1: (1, 0), 3: (1, 1), 4: (2, 0), 7: (2, 1)}
    print("N\tQ\tConfig (i,j)")
    for N, (i, j) in configs.items():
        Q = np.sqrt(3 * N)
        print(f"{N}\t{Q:.2f}\t({i},{j})")
        plot_reuse_pattern(N, i, j, R=1.0, rings=2)

# ==========================================
# PART B: HANDOVER DECISION LOGIC
# ==========================================
def generate_signals(num_samples=300):
    np.random.seed(42) 
    t = np.arange(num_samples)
    
    # Increased noise slightly to show the ping-pong effect better
    serving_trend = -0.05 * t + 80
    serving_noise = np.cumsum(np.random.normal(0, 0.8, num_samples)) + np.random.normal(0, 1.5, num_samples)
    serving = serving_trend + serving_noise
    
    neighbor_trend = 0.05 * t + 75
    neighbor_noise = np.cumsum(np.random.normal(0, 0.8, num_samples)) + np.random.normal(0, 1.5, num_samples)
    neighbor = neighbor_trend + neighbor_noise
    
    return serving, neighbor

def simulate_handovers(serving, neighbor, policy="naive", hysteresis=3.0, ttt=5):
    handovers = []
    current_serving = serving.copy()
    current_neighbor = neighbor.copy()
    
    ttt_counter = 0
    
    for t in range(len(serving)):
        if policy == "naive":
            condition = current_neighbor[t] > current_serving[t]
        else:
            condition = current_neighbor[t] > (current_serving[t] + hysteresis)
            
        if condition:
            ttt_counter += 1
            if policy == "naive" or ttt_counter >= ttt:
                handovers.append(t)
                current_serving, current_neighbor = current_neighbor, current_serving
                ttt_counter = 0 
        else:
            ttt_counter = 0 
            
    return handovers, current_serving, current_neighbor

def run_part_b():
    print("\n--- PART B: Handover Decision Logic ---")
    serving, neighbor = generate_signals()
    
    ho_naive, s_n, n_n = simulate_handovers(serving, neighbor, "naive")
    ho_hyst, s_h, n_h = simulate_handovers(serving, neighbor, "hyst", hysteresis=3.0, ttt=1)
    ho_hyst_ttt, s_ht, n_ht = simulate_handovers(serving, neighbor, "hyst", hysteresis=3.0, ttt=5)
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    configs = [
        ("Naive Trigger (Ping-Pong)", ho_naive, s_n, n_n),
        ("Hysteresis Only (3dB)", ho_hyst, s_h, n_h),
        ("Hysteresis + TTT (3dB, 5 samples)", ho_hyst_ttt, s_ht, n_ht)
    ]
    
    for ax, (title, hos, s_curr, n_curr) in zip(axs, configs):
        ax.plot(serving, label="Cell A (Original)", linestyle='--', color='gray')
        ax.plot(neighbor, label="Cell B (Original)", linestyle='--', color='lightblue')
        ax.plot(s_curr, label="Current Serving", color='blue', linewidth=2)
        
        for ho in hos:
            ax.axvline(ho, color='red', linestyle=':', alpha=0.7)
            
        ax.set_title(f"{title} - Total Handovers: {len(hos)}")
        ax.set_ylabel("RSRP (dBm)")
        ax.legend(loc="lower left")
        ax.grid(True, alpha=0.3)
        
    axs[-1].set_xlabel("Time (Samples)")
    plt.tight_layout()
    
    # SAVE THE FIGURE BEFORE SHOWING
    plt.savefig("handover_results.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nHandover Counts:")
    print(f"Naive: {len(ho_naive)}")
    print(f"Hysteresis Only: {len(ho_hyst)}")
    print(f"Hysteresis + TTT: {len(ho_hyst_ttt)}")

if __name__ == "__main__":
    run_part_a()
    run_part_b()