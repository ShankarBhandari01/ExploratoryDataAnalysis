import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px

class CoronaDataPipline:
    def __init__(self, data):
        self.data = data
       # self.print_data()
        
    def print_data(self):
        print(self.data.head())
        
    def print_col(self):
        print(self.data.columns)
        #Index(['theme', 'sub_theme', 'topic', 'geography_type', 'geography', 'metric',
        #     'sex', 'age', 'stratum', 'year', 'date', 'metric_value',
        #    'in_reporting_delay_period'],
        #   dtype='object')
    def get_na_value(self):
        print(self.data[ self.data.isna()].count())
    
    def sort_value_by(self,by):
        # sorting the data by date
        self.data.sort_values(by=by, inplace=True)
    def convert_dateTime(self,colname):
        # converting/type casting date in to date and time 
        self.data[colname]=pd.to_datetime(self.data[colname])
    
    def rolling_data_avg(self,colname,newColName):
        # geting 7 days rolling avg
        self.data[newColName] = self.data[colname].rolling(window=7).mean() 
        
    def clean_data(self):
        self.sort_value_by('date')
        self.convert_dateTime('date')
        self.rolling_data_avg('metric_value',newColName='avg_7_days')
        self.set_groupby('sex')
        
    def get_clean_data(self):
        return self.data
    
    def set_groupby(self,by):
        # grouping data by
       self.data.groupby(by)
        
    def plot(self,type):
        self.clean_data()
        if type =='sns':
           self.plot_sns() 
        else:
            self.plot_ploty()   
    
    def plot_sns(self):
        # Create the line plot
        plt.figure(figsize=(12, 6))
        color = {'f':'#4a32a8','m':'#329ea8'}
        sns.lineplot(data=self.data, x='date', y='metric_value', hue='sex', palette=color,  alpha=0.7, legend='full')
        # Format x-axis dates to 'MMM YYYY' (e.g., 'Nov 2023')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Add labels and title
        plt.title('Case rates by specimen date and sex (7-day rolling average)', fontsize=16)

        # Customise the legend
        handles, labels = plt.gca().get_legend_handles_labels()
        # Mapping for the legend
        label_mapping = {'f': 'Female', 'm': 'Male'}  # Map original to desired labels
        legend_order = ['Female', 'Male']  # Desired order

        # Reorder and rename the legend
        reordered_handles = [handles[labels.index(key)] for key in label_mapping.keys()]
        reordered_labels = [label_mapping[key] for key in label_mapping.keys()]

        plt.legend(
            handles=reordered_handles, 
            labels=reordered_labels,  # Rename labels
            loc='upper center',  # Position 
            ncol=len(legend_order),  # horizontal line
            fontsize=10,  # font size
            title_fontsize=12,  # title font size
            frameon=False,  # border around 
        )

        plt.tight_layout()
        # Show the plot
        plt.show()

    def plot_ploty(self):
        # Create the plot using Plotly
        fig = px.line(
            self.data, 
            x='date', 
            y='metric_value', 
            color='sex', 
            labels={'sex': 'Gender'},  # Rename the sex column for better readability
            title='Case rates by specimen date and sex (7-day rolling average)'
        )

        # Customizing line colors
        fig.update_traces(
            line=dict(color='#329ea8'),  # Default color for Male or 'm'
            selector=dict(name='m')
        )

        fig.update_traces(
            line=dict(color='#4a32a8'),  # Default color for Female or 'f'
            selector=dict(name='f')
        )

        # Format the x-axis dates to 'MMM YYYY'
        fig.update_xaxes(
            tickformat='%b %Y',  # Formatting the dates as 'Nov 2023'
        )

        # Update the legend to show 'Female' first and 'Male' second
        fig.for_each_trace(lambda t: t.update(name='Female') if t.name == 'f' else t.update(name='Male'))

        # Adjust legend settings to be horizontal
        fig.update_layout(
            legend=dict(
                orientation='h',  # Horizontal legend
                x=0.5,  # Centered horizontally
                xanchor='center',
                y=0.9,  # Place the legend below the plot
                yanchor='middle'   
            ),
            font=dict(size=12),  # Font size for text
        )

        # Show the plot
        fig.show()
        
        


   




