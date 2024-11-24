import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

class StoreType:
    
    def __init__(self, file_path='data/input/DS_SAMPLE.csv'):
        """
        Initializes the StoreType class and reads the data from a CSV file.
        """
        self.df = pd.read_csv(file_path)
        self.preprocess_dates()
    
    def preprocess_dates(self):
        """
        Converts date columns to datetime and adds day of the week column.
        """
        self.df['SCHEDULE DATE'] = pd.to_datetime(self.df['SCHEDULE DATE'], errors='coerce')
        self.df['CREATION DATE'] = pd.to_datetime(self.df['CREATION DATE'], errors='coerce')
        self.df['DAY_OF_WEEK'] = self.df['SCHEDULE DATE'].dt.dayofweek
    
    def task_1a(self):
        """
        Counts the number of "PO NUMBER" for each "TYPE" grouped by "WHS".
        """
        result = self.df.groupby(["TYPE", "WHS"])["PO NUMBER"].count().reset_index()
        result = result.rename(columns={"PO NUMBER": "COUNT_PO_NUMBER"})
        self._print_result('Counts the number of "PO NUMBER" for each "TYPE" grouped by "WHS":', result)

    def task_1b(self):
        """
        Calculates the sum of "PALLET", "TOTAL CUBE", "TOTAL CASES", and "TOTAL WGHT"
        grouped by "TYPE" and "VENDOR NUMBER".
        """
        result = self.df.groupby(["TYPE", "VENDOR NUMBER"])[["PALLET", "TOTAL CUBE", "TOTAL CASES", "TOTAL WGHT"]].sum().reset_index()
        result = result.rename(columns={
            "PALLET": "SUM_PALLET",
            "TOTAL CUBE": "SUM_TOTAL_CUBE",
            "TOTAL CASES": "SUM_TOTAL_CASES",
            "TOTAL WGHT": "SUM_TOTAL_WGHT"
        })
        self._print_result('Calculates the sum of "PALLET", "TOTAL CUBE", "TOTAL CASES", and "TOTAL WGHT" grouped by "TYPE" and "VENDOR NUMBER":', result)

    def task_2a(self):
        """
        Calculates the mean number of "PALLET" by day of the week using the "SCHEDULE DATE".
        """
        mean_pallet_by_day = self.df.groupby('DAY_OF_WEEK')['PALLET'].mean().reset_index()
        self._print_result("Mean of PALLET by Day of the Week:", mean_pallet_by_day)
        
    def task_2b(self):
        """
        Calculates the average number of days between "CREATION DATE" and "SCHEDULE DATE".
        """
        self.df['DIFF_DAYS'] = (self.df['SCHEDULE DATE'] - self.df['CREATION DATE']).dt.days
        avg_difference = self.df['DIFF_DAYS'].mean()
        print("Avg No. of Days between 'CREATION DATE' & 'SCHEDULE DATE':", avg_difference)
        
    def task_2c(self):
        """
        Visualizes Days Difference Between Creation and Schedule Dates using Boxplot and Z-Score.
        Identifies outliers based on Z-Score and visualizes the data distribution.
        """
        # Box plot
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.df['DIFF_DAYS'])
        plt.title('Boxplot of Days Difference Between Creation and Schedule Dates')
        plt.xlabel('Days Difference')
        plt.show()
        
        # Z-score for outlier detection
        self.df['Z_SCORE'] = zscore(self.df['DIFF_DAYS'])
        outliers = self.df[self.df['Z_SCORE'].abs() > 3]
        print("Outliers based on Z-Score:", outliers[['CREATION DATE', 'SCHEDULE DATE', 'DIFF_DAYS', 'Z_SCORE']])

    def task_2d(self):
        """
        Generates a time series plot showing the "TOTAL WGHT" over time.
        """
        self.df = self.df.sort_values('SCHEDULE DATE')
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['SCHEDULE DATE'], self.df['TOTAL WGHT'], marker='o', linestyle='-', color='blue', label='Total Weight')
        plt.title('Total Weight Over Time', fontsize=14)
        plt.xlabel('Schedule Date', fontsize=12)
        plt.ylabel('Total Weight', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.show()

    def task_2e(self):
        """
        Identifies the "UPC" with the most "TOTAL CASES" ordered for each "BYR".
        """
        grouped_data = self.df.groupby(['BYR', 'UPC'])['TOTAL CASES'].sum().reset_index()
        max_cases_per_byr = grouped_data.loc[grouped_data.groupby('BYR')['TOTAL CASES'].idxmax()]
        max_cases_per_byr = max_cases_per_byr.rename(columns={'TOTAL CASES': 'MAX TOTAL CASES'})
        self._print_result("UPC with the most TOTAL CASES for each BYR:", max_cases_per_byr)
        
    def _print_result(self, description, result):
        """
        Helper method to print the result with a description.
        """
        print(description)
        print(result)
        print("\n" + "-"*50 + "\n")

    def execute_all_tasks(self):
        """
        Executes all tasks in sequence.
        """
        self.task_1a()
        self.task_1b()
        self.task_2a()
        self.task_2b()
        self.task_2c()
        self.task_2d()
        self.task_2e()


