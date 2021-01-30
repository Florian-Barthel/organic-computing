import pandas as pd

file_name = 'population_ws2021.csv'

df = pd.read_csv(file_name)
print(df.to_string())