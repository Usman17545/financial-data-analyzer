import pandas as pd
import random
import time
# Read CSV into DataFrame
df = pd.read_csv('F:/ML IPYNB/financial-data-parser/data/processed/ledger.csv')  # assumes columns 'id' and 'value'
target = pd.read_csv('F:/ML IPYNB/financial-data-parser/data/processed/target.csv',header = None)
# Convert DataFrame into dictionary
ledger_dict = dict(zip(df['Document No.'], df['Amount']))

target.iloc[:, 0] = pd.to_numeric(target.iloc[:, 0], errors='coerce')
target = target.dropna().reset_index(drop=True)
target_list = target.iloc[:, 0].astype(float).tolist()


def subset_sum(nums, target, margin=0):
    results = []
    keys = list(nums.keys())
    values = list(nums.values())

    for start in range(len(values)):
        total = 0.0
        picked_keys = []
        picked_values = []
        for i in range(start, len(values)):
            remaining = target - total
            if values[i] <= remaining:
                if (total + values[i]) >= 0:
                    total += float(values[i])
                    picked_keys.append(keys[i])
                    picked_values.append(values[i])

                    if abs(total - target) <= margin:
                        results.append({
                            "target": target,
                            "start_index": start,
                            "picked": dict(zip(picked_keys, picked_values)),
                            "sum": total,
                            "remaining": target - total
                        })
    return results

def CalSubset1(ledger_dict,target_value,margin):
    results1 = subset_sum(ledger_dict, target_value, margin)
    results2 = subset_sum(dict(reversed(ledger_dict.items())), target_value, margin)
    items = list(ledger_dict.items())
    random.shuffle(items)
    shuffled_dict = dict(items)
    results3 = subset_sum(shuffled_dict, target_value, margin)
    results = results1 + results2 + results3
    return results

filtered_dict = {k: v for k, v in ledger_dict.items() if v != 0.0}

#if change target change [2] to [3] [4] ....
target_value = target_list[108]

start_time = time.time()
print(f"Target Value is : {target_value}")
results = CalSubset1(filtered_dict,target_value,1)
end_time = time.time()
print(f"Time taken: {end_time - start_time:.6f} seconds")
if results:
    sorted_results = sorted(results, key=lambda r: abs(r['remaining']))

    seen_picked = set()
    unique_results = []

    for r in sorted_results:
        picked_key = tuple(sorted((k, round(float(v), 6)) for k, v in r['picked'].items()))

        if picked_key not in seen_picked:
            seen_picked.add(picked_key)
            unique_results.append(r)

    for i, r in enumerate(unique_results, start=1):
        picked_str = " | ".join(f"{k}:{v}" for k, v in r['picked'].items())
        r['sum'] = round(r['sum'], 2)
        r['remaining'] = round(r['remaining'], 2)
        print(f"Subset {i} -> Sum={r['sum']} | Remaining={r['remaining']} | Picked= {picked_str}")
