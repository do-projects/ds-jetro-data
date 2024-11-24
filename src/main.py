from task1 import StoreType
from task2 import BankSystem
from task3 import ProductSales

def main():
    while True:
        print("\n*****************************************")
        print("\n\nWelcome to JETRO Console! !!!!!")
        print("Please select from the following options")
        print("1. Run Task 1 for Store Type")
        print("2. Run Task 2 for Bank System")
        print("3. Run Task 3 SQL Product Sales")
        print("4. Exit")

        choice = input("Enter the number of your choice: ")
        
        if choice == '1':
            print("\nRunning Store Type Task...")
            store = StoreType(file_path='data/input/DS_SAMPLE.csv')
            store.execute_all_tasks()
            
        elif choice == '2':
            print("\nRunning Bank System Task...")
            user = BankSystem()
            user.deposit(1000, 'checking')
            user.deposit(500, 'savings')
            user.transfer(500, 'checking', 'savings')
            user.deposit(250, 'checking')
            user.withdraw(500, 'savings')

            print("\nActivity history:")
            user.show_records()
            
        elif choice == '3':
            print("\nRunning Product Sales Task...")
            ds_sales = ProductSales(csv_path='data/input/SQL_SAMPLE.csv', db_path='product_sales.db')
            ds_sales.executeAllTasks()

        elif choice == '4':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
