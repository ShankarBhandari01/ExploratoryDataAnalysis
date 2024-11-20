import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class Analysis:
    # Initialise the class
    def __init__(self,dataset):
        self.dataset = dataset
   
    #print the data
    def print_data(self):
        print(self.dataset.head())
    
    def count_missing_value(self):
        # Check for missing values
        print(f'counts: {self.dataset.isnull().sum()}')
        
    def handle_missing_values(self):
        print(f'handling missing values')
        # handling missing values
        self.dataset['Date'] = self.dataset['Date'].fillna(method='ffill')  # Forward fill for Date
        self.dataset['Time'] = self.dataset['Time'].fillna(method='ffill')  # Forward fill
        self.dataset['Status'] =self.dataset['Status'].fillna(self.dataset['Status'].mode()[0])
        # Convert 'Ozone' to numeric, if necessary (strip units or handle errors)
        self.dataset['Ozone'] = pd.to_numeric(self.dataset['Ozone'], errors='coerce')
        self.dataset['Ozone'] = self.dataset['Ozone'].fillna(self.dataset['Ozone'].mean())
       
    def typeCasting(self):
        print('handling date and time data')
        # Combine 'Date' and 'Time' into a single datetime column
        self.dataset['Datetime'] = pd.to_datetime(self.dataset['Date'] + ' ' + self.dataset['Time'], errors='coerce')
        # Set the 'Datetime' column as the index
        self.dataset.set_index('Datetime', inplace=True)

        
    def select_col(self):
        print('selecting columns')
        # Drop unnecessary columns (like 'Date' and 'Time') and focus on 'Ozone'
        self.dataset = self.dataset[['Ozone']]
        
    def convert_toNumpy(self):
        print('converting to numpy')
        # Convert the DataFrame to a NumPy array
        self.dataset = self.dataset.to_numpy()
        
    def execute_analysis(self):
        self.count_missing_value()
        self.handle_missing_values()
        self.typeCasting()
        self.select_col()
        self.plot()

    def plot(self):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
        # Plot ozone levels
        axes[0].plot(self.dataset.index, self.dataset['Ozone'], label='Ozone Levels', color='blue')
        axes[0].set_title('Hourly Ozone Levels Over Time')
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Ozone (ugm-3)')
        axes[0].legend()
        axes[0].grid(True)
        
        
        self.hotwinter_cal()
        for h in range(self.seasonal_period):
            self.forecast[self.n + h] = self.level + self.seasonal[(self.n + h) % self.seasonal_period]

        # Debug: Check fitted and forecast values
        print(f"Last Level: {self.level}")
        print(f"Updated Seasonal Components: {self.seasonal}")
        print(f"Forecast for next {self.seasonal_period} periods: {self.forecast[self.n:]}")
    
        # Step 4: Plot the Results
        axes[1].plot(self.dataset, label="Original Data", color="blue")
        axes[1].plot(self.fitted, label="Fitted Values", color="orange")
        axes[1].plot(range(self.n,self.n + self.seasonal_period), self.forecast[self.n:], label="Forecast", color="green", linestyle="dashed")
        axes[1].set_title("Holt-Winters (No Trend) Predicted Values")
        axes[1].set_xlabel("Time")
        axes[1].set_ylabel('Ozone (ugm-3)')
        axes[1].legend()
        
        # Adjust layout to avoid overlap
        plt.tight_layout()

        # Show the plot
        plt.show()
                
    def hotwinter_cal(self):
       # Calculate the initial values
       self.alpha = 0.3  # Smoothing parameter for level
       self.beta = 0.2   # Smoothing parameter for seasonality
       self.seasonal_period = 12  # Example: 12 for monthly data
    
       # Step 1: Prepare the Data
       self.convert_toNumpy()
       # Step 2: Initialize Components
       self.n = len(self.dataset)
       self.seasonal = np.zeros(self.seasonal_period)  
       self.level = np.mean(self.dataset[:self.seasonal_period]) 
       self.forecast = np.zeros(self.n + self.seasonal_period) 
       # Step 4: Estimate Initial Seasonality
       for i in range(self.seasonal_period):
           self.seasonal[i] = self.dataset[i] - self.level
           # Debug: Check initial seasonal components
           print(f"Initial Level: {self.level}")
           print(f"Initial Seasonal Components: {self.seasonal}")
           
    
        # Step 5: Apply Holt-Winters
       self.fitted = np.zeros(self.n)  # Fitted values
       for t in range(self.n):
            if t >= self.seasonal_period:
                # Update level
                self.level_new = self.alpha * (self.dataset[t] - self.seasonal[t % self.seasonal_period]) + (1 - self.alpha) * self.level
                
                # Update seasonal component
                self.seasonal[t % self.seasonal_period] = self.beta * (self.dataset[t] - self.level) + (1 - self.beta) * self.seasonal[t % self.seasonal_period]
                
                # Replace level with updated level
                self.level = self.level_new

            # Compute fitted value
            self.fitted[t] = self.level + self.seasonal[t % self.seasonal_period]

       
        

    

    
