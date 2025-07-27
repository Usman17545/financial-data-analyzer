import pandas as pd
class DataStorage:
    def __init__(self):
        self.df = pd.DataFrame()
        self.metadata = {}
        self.indexed_columns = []
    def extract_metadata(self,df):
        return {
            "num_rows": df.shape[0],
            "num_columns": df.shape[1],
            "columns": list(df.columns),
            "null_counts": df.isnull().sum().to_dict()
            }
    def store_data(self, dataframe, metadata=None):
        self.df = dataframe.copy()
        if metadata:
            self.metadata = metadata
    def create_indexes(self, columns):
        self.indexed_columns = columns
        self.df.set_index(columns, inplace=True)

    def query_by_criteria(self, filters):
        df = self.df.copy()
        for column, condition in filters.items():
            if isinstance(condition, tuple) and len(condition) == 2:
                start, end = condition
                df = df[(df[column] >= start) & (df[column] <= end)]
            else:
                df = df[df[column] == condition]
        return df
    def aggregate_data(self, group_by, measures):
        agg_result = self.df.groupby(group_by).agg(measures)
        return agg_result
