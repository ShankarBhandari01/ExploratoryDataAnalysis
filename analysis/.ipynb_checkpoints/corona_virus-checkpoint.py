import pandas as pd 
# import the data
data = pd.read_csv('analysis/data/ukhsaChartData.csv')
print(data.head())
# print the columns name
print(data.columns)