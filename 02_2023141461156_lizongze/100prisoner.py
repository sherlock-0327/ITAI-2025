import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_round(N, K, strategy):
    """
    Simulate one round of the prisoner and boxes problem.
    strategy: 'random' or 'loop'
    Returns the number of prisoners who found their number in K attempts.
    """
    boxes = list(range(1, N + 1))
    random.shuffle(boxes)

    found_count = 0
    for prisoner in range(1, N + 1):
        if strategy == 'random':
            attempts = random.sample(range(N), K)
            if prisoner in [boxes[i] for i in attempts]:
                found_count += 1
        else:
            pos = prisoner - 1
            for _ in range(K):
                if boxes[pos] == prisoner:
                    found_count += 1
                    break
                pos = boxes[pos] - 1
    return found_count

def run_simulation(N, K, T):
    """
    Run T simulations for both strategies and collect statistics.
    Returns:
      results: {
        'random': {'all_success': int, 'counts': list},
        'loop':   {'all_success': int, 'counts': list}
      }
    """
    results = {
        'random': {'all_success': 0, 'counts': []},
        'loop':   {'all_success': 0, 'counts': []}
    }
    for _ in range(T):
        for strat in ['random', 'loop']:
            found = simulate_round(N, K, strat)
            results[strat]['counts'].append(found)
            if found == N:
                results[strat]['all_success'] += 1
    return results

# Parameters
T = 10000
# Original scenario: N=100, K=50
orig_N, orig_K = 100, 50
results_orig = run_simulation(orig_N, orig_K, T)
rate_orig_loop = results_orig['loop']['all_success'] / T
rate_orig_random = results_orig['random']['all_success'] / T

# Extension scenario: N=50, K=25
ext_N, ext_K = 50, 25
results_ext = run_simulation(ext_N, ext_K, T)
rate_ext_loop = results_ext['loop']['all_success'] / T
rate_ext_random = results_ext['random']['all_success'] / T

# Sweep K for N=100
Ks = list(range(10, 101, 10))
rates_loop = []
rates_random = []
for K in Ks:
    res = run_simulation(100, K, T)
    rates_random.append(res['random']['all_success'] / T)
    rates_loop.append(res['loop']['all_success'] / T)

# Plot histograms: original and extension
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(results_orig['loop']['counts'], bins=range(orig_N+2), align='left', edgecolor='k')
plt.title(f'N={orig_N}, K={orig_K} (Loop)')
plt.xlabel('Number of Prisoners Succeeded')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(results_ext['loop']['counts'], bins=range(ext_N+2), align='left', edgecolor='k')
plt.title(f'N={ext_N}, K={ext_K} (Loop)')
plt.xlabel('Number of Prisoners Succeeded')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Plot success rate vs K for both strategies
plt.figure()
plt.plot(Ks, [r*100 for r in rates_random], label='Random', marker='o')
plt.plot(Ks, [r*100 for r in rates_loop], label='Loop', marker='o')
plt.xlabel('Max Attempts per Prisoner (K)')
plt.ylabel('Full-group Success Rate (%)')
plt.title('Success Rate vs K for N=100')
plt.legend()
plt.grid(True)
plt.show()
