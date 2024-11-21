import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class Analysis:
    # Initialise the class
    def __init__(self,dataset):
         # Convert the dataset to a numpy array
        self.dataset = self.convert_toNumpy(dataset)
        # Get the ozone column
        self.ozone = self.dataset[:,2].astype(np.float64) 
        # Replace 'No Data' with np.nan (if the data is a string type)
        self.ozone = np.where(self.ozone == 'No Data', np.nan, self.ozone)     
        #Convert the array to float, ignoring 'No Data' which is now np.nan
        mean = np.nanmean(self.ozone)
        # replace 'No Data' with the mean
        self.ozone[np.isnan(self.ozone)]= mean 
        
    def convert_toNumpy(self,data):
        print('# Convert the DataFrame to a NumPy array')
        data['Ozone'] = pd.to_numeric(data['Ozone'], errors='coerce')
        data[['Time', 'Date',]] = data[['Time', 'Date',]].ffill()  # Forward fill
        self.dateTime = pd.to_datetime(data['Date'] + ' ' + data['Time'], errors='coerce')
        return data.to_numpy()
        
    def execute_analysis(self):
        self.plot() 

    def plot(self):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
        # Plot ozone levels
        axes[0].plot(self.dateTime, self.ozone, label='Ozone Levels', color='blue')
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
        axes[1].plot(self.dateTime, self.ozone, label="Original Data", color="blue")
        axes[1].plot(self.dateTime,self.fitted, label="Fitted Values", color="orange")
        axes[1].set_title("Holt-Winters (No Trend) Predicted Values")
        axes[1].set_xlabel("Time")
        axes[1].set_ylabel('Ozone (ugm-3)')
        axes[1].legend()
        axes[1].grid(True)
        
        # Adjust layout to avoid overlap
        plt.tight_layout()

        # Show the plot
        plt.show()
                
    def hotwinter_cal(self):
       # Calculate the initial values
       self.alpha = 0.3  # Smoothing parameter for level
       self.beta = 0.2   # Smoothing parameter for seasonality
       self.seasonal_period = 12  # Example: 12 for monthly data
       

       # Step 2: Initialize Components
       self.n = len(self.ozone)
       self.seasonal = np.zeros(self.seasonal_period)  
       self.level = np.mean(self.ozone[:self.seasonal_period]) 
       self.forecast = np.zeros(self.n + self.seasonal_period) 
       # Step 4: Estimate Initial Seasonality
       for i in range(self.seasonal_period):
           self.seasonal[i] = self.ozone[i] - self.level
           # Debug: Check initial seasonal components
           print(f"Initial Level: {self.level}")
           print(f"Initial Seasonal Components: {self.seasonal}")
           
    
        # Step 5: Apply Holt-Winters
       self.fitted = np.zeros(self.n)  # Fitted values
       for t in range(self.n):
            if t >= self.seasonal_period:
                # Update level
                self.level_new = self.alpha * (self.ozone[t] - self.seasonal[t % self.seasonal_period]) + (1 - self.alpha) * self.level
                
                # Update seasonal component
                self.seasonal[t % self.seasonal_period] = self.beta * (self.ozone[t] - self.level) + (1 - self.beta) * self.seasonal[t % self.seasonal_period]
                
                # Replace level with updated level
                self.level = self.level_new

            # Compute fitted value
            self.fitted[t] = self.level + self.seasonal[t % self.seasonal_period]

       

 

    
