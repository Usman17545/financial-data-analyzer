
import pandas as pd
import time 
import random
# Read CSV into DataFrame
df = pd.read_csv('F:/ML IPYNB/financial-data-parser/data/processed/ledger.csv')  # assumes columns 'id' and 'value'
target = pd.read_csv('F:/ML IPYNB/financial-data-parser/data/processed/target.csv',header = None)
# Convert DataFrame into dictionary
ledger_dict = dict(zip(df['Key'], df['Value']))
ledger_dict

len(ledger_dict) # no negative values

len(target)

#convert target dataframe into list
target_list = target[0].to_list()
len(target_list)

#if chnage target change [2] to [3] [4] ....
target_value = target_list[4]
target_value

filtered_dict = {k: v for k, v in ledger_dict.items() if 0 < v < target_value} # only take values less than target
len(filtered_dict)

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

start_time = time.time()
print(f"Target Value is : {target_value}")
results1 = subset_dict_near_zero(filtered_dict, target_value, margin=1)
results2 = subset_dict_near_zero(dict(reversed(filtered_dict.items())), target_value, margin=1)
items = list(filtered_dict.items())
random.shuffle(items)
shuffled_dict = dict(items)
results3 = subset_dict_near_zero(shuffled_dict, target_value, margin=1)
end_time = time.time()
print(f"Time taken: {end_time - start_time:.6f} seconds")
results = results1 + results2 + results3
if results:
    best = sorted(results, key=lambda r: abs(r['remaining']))[0]
    print(f"Start index: {best['start_index']}")
    print(f"Sum: {best['sum']}")
    print(f"Remaining: {best['remaining']}")
    print("Picked:")
    for k, v in best['picked'].items():
        print(f"   {k}: {v}")