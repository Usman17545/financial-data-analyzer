import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.core.data_storage import DataStorage 
data = {
    'Department': ['Sales', 'Sales', 'HR', 'HR', 'IT'],
    'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Salary': [50000, 55000, 48000, 52000, 60000],
    'Experience': [3, 4, 2, 5, 7]
}
df = pd.DataFrame(data)
ds = DataStorage()
metadata = ds.extract_metadata(df)
ds.store_data(df, metadata)
print("Metadata:")
print(ds.metadata)
ds.create_indexes(['Department'])
print("\nData with Department as index:")
print(ds.df)
filters = {'Experience': (3, 6)}
filtered_df = ds.query_by_criteria(filters)
print("\nFiltered Data (Experience 3 to 6):")
print(filtered_df)
aggregated = ds.aggregate_data(
    group_by='Department',
    measures={'Salary': 'mean', 'Experience': 'max'}
)
print("\nAggregated Data (Avg Salary & Max Experience by Department):")
print(aggregated)
