import pandas as pd
from  Analysis import Analysis
from CoronaVirus import CoronaDataPipline

# Create a new instance of the Analysis class
def load_time_series():
    # Load dataset
    dataset = pd.read_csv('analysis/data/AirQualityDataHourly.csv',
                   skiprows=10)
    analysis = Analysis(dataset=dataset)
    analysis.execute_analysis()
# create a new instance of the CoronaDataPipline class    
def reconstructPlot(type):
    data = pd.read_csv('analysis/data/ukhsaChartData.csv')
    pipe = CoronaDataPipline(data=data)
    pipe.plot(type=type)
    
load_time_series() # Load time series data
reconstructPlot('sns') # This will run the analysis and plot the data



