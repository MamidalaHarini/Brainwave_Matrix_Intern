import os
import json
import hashlib
from datetime import datetime
import getpass  

# Data file to store users account details
DATA_FILE = "atm_data.json"

# Load the user data
def to_load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def to_save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Hash passwords for security
def security_hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Class to represent an ATM account
class Functional_ATM:
    def __init__(self, user_id):
        self.data = to_load_data()
        self.user_id = user_id

    def create_account(self, password):
        if self.user_id in self.data:
            return "An Account with this ID already exists."
        hashed_password = security_hash_password(password)
        self.data[self.user_id] = {
            "password": hashed_password,
            "balance": 0,
            "transactions": []
        }
        to_save_data(self.data)
        return "Your Account has been created successfully!"

    def reset_password(self, new_password):
        if self.user_id not in self.data:
            return "No account exists for this User ID.Kindly create one."
        hashed_password = security_hash_password(new_password)
        self.data[self.user_id]["password"] = hashed_password
        to_save_data(self.data)
        return "Your password has been reset. You can now access your account with the new password."

    def authenticate(self, password):
        hashed_password = security_hash_password(password)
        user = self.data.get(self.user_id)
        if user and user["password"] == hashed_password:
            return True
        return False

    def deposit(self, amount):
        if amount <= 0:
            return "Please enter a valid amount to deposit:"
        self.data[self.user_id]["balance"] += amount
        self._add_transaction(f"Deposited: ${amount}")
        to_save_data(self.data)
        return f"${amount} deposited successfully."

    def withdraw(self, amount):
        if amount <= 0:
            return "Please provide a valid amount to withdraw:"
        if self.data[self.user_id]["balance"] < amount:
            return "Transaction declined due to low balance."
        self.data[self.user_id]["balance"] -= amount
        self._add_transaction(f"Withdrew: ${amount}")
        to_save_data(self.data)
        return f"${amount} withdrawn successfully."

    def check_balance(self):
        return f"Your current balance is: ${self.data[self.user_id]['balance']}"

    def transaction_history(self):
        transactions = self.data[self.user_id]["transactions"]
        if not transactions:
            return "Your account has no transaction records yet."
        return "\n".join(transactions)

    def _add_transaction(self, detail):
        transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {detail}"
        self.data[self.user_id]["transactions"].append(transaction)

# Main function to drive the ATM program
def main():
    data = to_load_data()
    print("Greetings!Welcome to the Python-based ATM service.")
    user_id = input("Provide your User ID to access to your accounut: ")

    atm = Functional_ATM(user_id)

    # If the user ID is new or the user wants to reset their password
    if user_id not in data:
        print("Looks like you're a new user or haven't set a password yet.")
        password = getpass.getpass(": ")  # Secure password input
        print(atm.create_account(password))
        return

    # Securely Set a password for your account 
    password = getpass.getpass("Provide your password to log in. ")  
    if not atm.authenticate(password):
        print("Access denied.Password mismatch.")
        reset = input("Would you like to reset your password?Respond with 'Yes' or 'No' ").strip().lower()
        if reset == "yes":
            new_password = getpass.getpass("Set a new password to proceed: ")
            print(atm.reset_password(new_password))
        else:
            print("Goodbye!")
        return

    while True:
        print("\n *** Select an option ***")
        print("1. Deposit Money into Account")
        print("2. Withdraw Money from Account")
        print("3. Display Amount Balance")
        print("4. Review Transaction History")
        print("5. Exit the ATM")

        choice = input("Choose an option: ")
        if choice == "1":
            amount = float(input("Enter the amount you wish to deposit: "))
            print(atm.deposit(amount))
        elif choice == "2":
            amount = float(input("Enter the amount you wish to withdraw: "))
            print(atm.withdraw(amount))
        elif choice == "3":
            print(atm.check_balance())
        elif choice == "4":
            print(atm.transaction_history())
        elif choice == "5":
            print("Thank you for using our ATM service.Have a great day!")
            break
        else:
            print("Invalid selection. Try choosing a valid option.")

if __name__ == "__main__":
    main()
