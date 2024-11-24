import pandas as pd
import sqlite3

class ProductSales:
    def __init__(self, csv_path, db_path):
        """Initializes the class with CSV path and SQLite DB path."""
        self.csv_path = csv_path
        self.db_path = db_path
        self.conn = None
        self.df = None
    
    def load_data(self):
        """Loads data from the CSV file into a pandas DataFrame."""
        self.df = pd.read_csv(self.csv_path, delimiter='\t')
    
    def create_connection(self):
        """Creates a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
    
    def insert_data(self):
        """Inserts data into the SQLite database (normalized form)."""
        # Insert the file into a SQLite database using pandas
        self.df.to_sql("master_sales_data", self.conn, if_exists="replace", index=False)

        # Normalize the data and insert into separate tables
        self._insert_table("products", self.df[["UPC", "GroupName", "DepartmentName", "PrimaryUPC"]].drop_duplicates())
        self._insert_table("vendors", self.df[["VendorCode", "Description"]].drop_duplicates())
        self._insert_table("sales", self.df[["UPC", "RegionName", "YearlySales", "YearlyCost", "YearlyQuantitySold", "WWCSBranch", "ZIP", "BuyerCode"]])
        self._insert_table("stock", self.df[["UPC", "DailyDate", "DailyStocklevel"]])
        self._insert_table("department", self.df[["DepartmentName"]])
        self._insert_table("groups", self.df[["GroupName"]])
    
    def _insert_table(self, table_name, data):
        """Helper method to insert data into a table."""
        data.to_sql(table_name, self.conn, if_exists="replace", index=False)
    
    def create_indexes(self):
        """Creates indexes on the database tables for improved query performance."""
        cursor = self.conn.cursor()

        # Create indexes for faster querying
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_upc ON products (UPC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendors_code ON vendors (VendorCode)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_yearly_sales ON sales (YearlySales)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_date ON stock (DailyDate)")

        self.conn.commit()
    
    def run_query(self, query):
        """Executes a given SQL query and returns the result as a DataFrame."""
        return pd.read_sql_query(query, self.conn)
    
    def top_selling_products(self):
        """Returns the top 3 selling products by branch and item."""
        query = """
        WITH RankedSales AS (
            SELECT 
                WWCSBranch,
                UPC,
                SUM(YearlyQuantitySold) AS TotalQuantity,
                RANK() OVER (PARTITION BY WWCSBranch ORDER BY SUM(YearlyQuantitySold) DESC) AS Rank
            FROM sales
            GROUP BY WWCSBranch, UPC
        )
        SELECT 
            WWCSBranch,
            UPC,
            TotalQuantity
        FROM RankedSales
        WHERE Rank <= 3;
        """
        return self.run_query(query)
    
    def three_day_moving_avg(self):
        """Calculates the 3-day moving average of daily stock levels by branch and UPC."""
        query = """
        WITH DailyStockWithRow AS (
            SELECT 
                s.WWCSBranch,
                s.UPC,
                strftime('%Y-%m-%d', stock.DailyDate) AS DailyDate,
                stock.DailyStocklevel,
                ROW_NUMBER() OVER (PARTITION BY s.WWCSBranch, s.UPC ORDER BY stock.DailyDate) AS RowNum
            FROM stock
            JOIN sales s ON stock.UPC = s.UPC
        )
        SELECT 
            a.WWCSBranch,
            a.UPC,
            a.DailyDate,
            ROUND(AVG(b.DailyStocklevel), 2) AS MovingAverage
        FROM DailyStockWithRow a
        JOIN DailyStockWithRow b
            ON a.WWCSBranch = b.WWCSBranch
            AND a.UPC = b.UPC
            AND b.RowNum BETWEEN a.RowNum - 2 AND a.RowNum
        GROUP BY a.WWCSBranch, a.UPC, a.DailyDate;
        """
        return self.run_query(query)
    
    def lowest_selling_item(self):
        """Finds the lowest selling item for each product group."""
        query = """
        WITH GroupSales AS (
            SELECT 
                p.GroupName,
                s.UPC,
                SUM(s.YearlyQuantitySold) AS TotalQuantity
            FROM sales s
            JOIN products p ON s.UPC = p.UPC
            GROUP BY p.GroupName, s.UPC
        ),
        RankedGroupSales AS (
            SELECT 
                GroupName,
                UPC,
                TotalQuantity,
                RANK() OVER (PARTITION BY GroupName ORDER BY TotalQuantity ASC) AS Rank
            FROM GroupSales
        )
        SELECT 
            GroupName,
            UPC,
            TotalQuantity
        FROM RankedGroupSales
        WHERE Rank = 1;
        """
        return self.run_query(query)
    
    def best_selling_item(self):
        """Finds the best-selling item for each department and branch."""
        query = """
        WITH DepartmentSales AS (
            SELECT 
                s.WWCSBranch,
                p.DepartmentName,
                s.UPC,
                SUM(s.YearlyQuantitySold) AS TotalQuantity
            FROM sales s
            JOIN products p ON s.UPC = p.UPC
            GROUP BY s.WWCSBranch, p.DepartmentName, s.UPC
        ),
        RankedDepartmentSales AS (
            SELECT 
                WWCSBranch,
                DepartmentName,
                UPC,
                TotalQuantity,
                RANK() OVER (PARTITION BY WWCSBranch, DepartmentName ORDER BY TotalQuantity DESC) AS Rank
            FROM DepartmentSales
        )
        SELECT 
            WWCSBranch,
            DepartmentName,
            UPC,
            TotalQuantity
        FROM RankedDepartmentSales
        WHERE Rank = 1;
        """
        return self.run_query(query)
    
    def product_association(self):
        """Finds associations between products and their primary UPC."""
        query = """
        SELECT 
            UPC, 
            PrimaryUPC, 
            COUNT(*) AS CountAssociatedItems
        FROM products
        GROUP BY PrimaryUPC, UPC
        ORDER BY PrimaryUPC, CountAssociatedItems DESC;
        """
        return self.run_query(query)
    
    def close_connection(self):
        """Closes the connection to the SQLite database."""
        if self.conn:
            self.conn.close()
            
    def executeAllTasks(self):
        self.load_data()
        self.create_connection()
        self.insert_data()
        self.create_indexes()

        print("Top 3 Selling Products by Branch and Item:")
        print(self.top_selling_products())

        print("\n3-Day Moving Average of Daily Stock Levels:")
        print(self.three_day_moving_avg())

        print("\nLowest Selling Item for Each Group:")
        print(self.lowest_selling_item())

        print("\nBest Selling Item for Each Department by Branch:")
        print(self.best_selling_item())

        print("\nProduct Association (UPC and PrimaryUPC):")
        print(self.product_association())

        # Close the connection to the database
        self.close_connection()