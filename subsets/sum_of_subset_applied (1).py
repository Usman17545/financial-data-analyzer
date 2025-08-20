import pandas as pd
import random
import time

# Read CSV into DataFrame
df = pd.read_csv('F:/ML IPYNB/financial-data-parser/data/processed/ledger.csv')  # assumes columns 'id' and 'value'
target = pd.read_csv('F:/ML IPYNB/financial-data-parser/data/processed/target.csv',header = None)
# Convert DataFrame into dictionary
ledger_dict = dict(zip(df['Document No.'], df['Amount']))

#convert target dataframe into list
target.iloc[:, 0] = pd.to_numeric(target.iloc[:, 0], errors='coerce')
target = target.dropna().reset_index(drop=True)
target_list = target.iloc[:, 0].astype(float).tolist()

def subset_dict_near_zero(filtered_dict, target_value, margin):
    results = []
    keys = list(filtered_dict.keys())
    values = list(filtered_dict.values())
    target_int = int(target_value)

    for start in range(len(values)):
        picked_keys = []
        picked_values = []
        remaining = target_int

        for i in range(start, len(values)):
            if values[i] <= remaining:
                picked_keys.append(keys[i])
                picked_values.append(values[i])
                remaining -= values[i]

            if remaining == 0:
                break

        total = sum(picked_values)
        # Store only if remaining is 0 or very close (within margin)
        if abs(remaining) <= margin:
            results.append({
                "start_index": start,
                "picked": dict(zip(picked_keys, picked_values)),
                "sum": total,
                "remaining": remaining
            })

    return results

def CalSubset(filtered_dict,target_value,margin):
    results1 = subset_dict_near_zero(filtered_dict, target_value, margin)
    results2 = subset_dict_near_zero(dict(reversed(filtered_dict.items())), target_value, margin)
    items = list(filtered_dict.items())
    random.shuffle(items)
    shuffled_dict = dict(items)
    results3 = subset_dict_near_zero(shuffled_dict, target_value, margin)
    results = results1 + results2 + results3
    return results

#if chnage target change [2] to [3] [4] ....
target_value = target_list[5]
filtered_dict = {k: v for k, v in ledger_dict.items() if 0 < v < target_value} # only take values less than target

start_time = time.time()
print(f"Target Value is : {target_value}")
results = CalSubset(filtered_dict,target_value,1)
end_time = time.time()
print(f"Time taken: {end_time - start_time:.6f} seconds")
if results:
    # sort results by abs remaining
    sorted_results = sorted(results, key=lambda r: abs(r['remaining']))

    seen = set()
    unique_results = []
    for r in sorted_results:
        sum_rounded = round(r['sum'], 2)
        remaining_rounded = round(r['remaining'], 2)
        picked_tuple = tuple(sorted((k, round(v, 2)) for k, v in r['picked'].items()))
        key = (sum_rounded, remaining_rounded, picked_tuple)

        if key not in seen:
            seen.add(key)
            r['sum'] = sum_rounded
            r['remaining'] = remaining_rounded
            r['picked'] = dict(picked_tuple)
            unique_results.append(r)

    for r in unique_results:
        picked_str = " | ".join(f"{k}:{v}" for k, v in r['picked'].items())
        print(
            f"Start {r['start_index']} -> Sum={r['sum']} | Remaining={r['remaining']} | Picked= {picked_str}"
        )
