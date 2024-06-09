#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk


# In[2]:


from tkinter import simpledialog, messagebox


# In[3]:


# Class representing an individual account
class Account:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []  # List to store transaction history

    # Method to record a new transaction in the account history
    def record_transaction(self, description):
        self.transactions.append(description)


# In[4]:


# Class to handle the transaction history functionality
class TransactionHistory:
    @staticmethod
    def show_history(account):
        trans = "\n".join(account.transactions)
        messagebox.showinfo("Transaction History", f"Transactions:\n{trans}")


# In[5]:


# Class to handle withdrawal functionality
class Withdraw:
    @staticmethod
    def withdraw_funds(account, amount):
        if account.balance >= amount:
            account.balance -= amount
            account.record_transaction(f"Withdraw ${amount}")
            messagebox.showinfo("Success", f"${amount} has been withdrawn.")
        else:
            messagebox.showerror("Error", "Insufficient funds")


# In[6]:


# Class to handle deposit functionality
class Deposit:
    @staticmethod
    def deposit_funds(account, amount):
        account.balance += amount
        account.record_transaction(f"Deposited ${amount}")
        messagebox.showinfo("Success", f"${amount} has been deposited.")


# In[7]:


class Transfer:
    @staticmethod
    def transfer_funds(src_account, dest_account, amount):
        if src_account.balance >= amount:
            src_account.balance -= amount
            dest_account.balance += amount
            src_account.record_transaction(f"Transferred ${amount} to {dest_account.user_id}")
            dest_account.record_transaction(f"Received ${amount} from {src_account.user_id}")
            messagebox.showinfo("Success", f"Transferred ${amount} to {dest_account.user_id}")
        else:
            messagebox.showerror("Error", "Insufficient funds")


# In[19]:


# Main Tkinter GUI class
class ATMApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM")
        self.master.geometry("400x400")

        # Configure rows and columns for layout
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Initialize some demo accounts
        self.accounts = {
            "Keerthi": Account("Keerthi", "2005", 10000),
            "Harshitha": Account("Harshitha", "2009", 15000)
        }

        self.create_login_window()

    # Method to create login window

    def create_login_window(self):
        title = tk.Label(self.master, text="ATM", font=("Helvetica", 16))
        title.grid(row=0, columnspan=2, pady=20)

        tk.Label(self.master, text="User ID").grid(row=1, column=0, padx=20, pady=10)
        tk.Label(self.master, text="PIN").grid(row=2, column=0, padx=20, pady=10)

        self.e1 = tk.Entry(self.master)
        self.e2 = tk.Entry(self.master, show="*")

        self.e1.grid(row=1, column=1, padx=20, pady=10)
        self.e2.grid(row=2, column=1, padx=20, pady=10)

        tk.Button(self.master, text="Quit", command=self.master.destroy).grid(row=4, columnspan=2, pady=5)

        tk.Button(self.master, text="Login", command=self.login).grid(row=3, columnspan=2, pady=5)

    def login(self):
        user_id = self.e1.get()
        pin = self.e2.get()

        if user_id in self.accounts and self.accounts[user_id].pin == pin:
            self.current_account = self.accounts[user_id]
            messagebox.showinfo("Success", "ATM functionality unlocked.")
            self.show_options()
        else:
            messagebox.showerror("Error", "Invalid User ID or PIN")

    def show_options(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title = tk.Label(self.master, text="ATM", font=("Helvetica", 16))
        title.grid(row=0, columnspan=2, pady=20)
        tk.Label(self.master, text="Balance:").grid(row=1, column=0, padx=20, pady=10)
        self.balance_label = tk.Label(self.master, text="")
        self.balance_label.grid(row=1, column=1, padx=20, pady=10)

        tk.Button(self.master, text="Transactions History", command=lambda: TransactionHistory.show_history(self.current_account)).grid(row=2, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Withdraw", command=self.withdraw_funds_gui).grid(row=3, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Deposit", command=self.deposit_funds_gui).grid(row=4, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Transfer", command=self.transfer_funds_gui).grid(row=5, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Quit", command=self.master.destroy).grid(row=6, columnspan=2, padx=20, pady=5)

    def update_balance_label(self):
        self.balance_label.config(text=f"${self.current_account.balance}")

    def withdraw_funds_gui(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            Withdraw.withdraw_funds(self.current_account, amount)
            self.update_balance_label()  # Update balance label after withdrawal

    def deposit_funds_gui(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            Deposit.deposit_funds(self.current_account, amount)
            self.update_balance_label()  # Update balance label after deposit

    def transfer_funds_gui(self):
        transfer_id = simpledialog.askstring("Transfer", "Enter User ID to transfer to:")
        if transfer_id in self.accounts:
            amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
            if amount is not None:
                Transfer.transfer_funds(self.current_account, self.accounts[transfer_id], amount)
                self.update_balance_label()  # Update balance label after transfer
        else:
            messagebox.showerror("Error", "Invalid User ID")
             

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()


# 

# In[ ]:



