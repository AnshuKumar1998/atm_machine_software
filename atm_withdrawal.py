import tkinter as tk
from tkinter import messagebox
import requests


# Create the main application window
root = tk.Tk()
root.title("MINI Bank ATM")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight() - 40))  # Set full size without covering the taskbar
root.attributes("-fullscreen", True)

# Create a frame for each page
welcome_frame = tk.Frame(root, bg='light blue')
options_frame = tk.Frame(root)
withdraw_frame = tk.Frame(root)
withdraw_otp_frame = tk.Frame(root)
transfer_frame = tk.Frame(root)
check_balance_frame = tk.Frame(root)
result_frame = tk.Frame(root)

# Function to switch between frames
def show_frame(frame):
    frame.tkraise()

# Function to handle API requests

def check_balance_on_submit():
    try:
        #atm_card_number = balance_card_number_entry.get()
        atm_card_number = 4526324512632541
        #pin = balance_pin_entry.get()
        pin = 4152
        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&pin={pin}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success: Avaliable Balance is {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

def money_transfer_on_submit():
    try:
        #atm_card_number = transfer_card_number_entry.get()
        atm_card_number = 4526324512632541
        account_no = 77041374
        pin = 4152
        amount = 200
        #account_no = account_number_entry.get()
        #amount = transfer_amount_entry.get()
        #pin = balance_pin_entry.get()
        url =  f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&account_no={account_no}&amount={amount}&pin={pin}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success : {response_data.get('message', '')}", bg="green")
            res_label.config(text=f"Transfer amount was {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

def withdraw_money_on_submit():
    try:
        #atm_card_number = card_number_entry.get()
        atm_card_number = 4526324512632541
        #amount = amount_entry.get()
        #pin = pin_entry.get()
        amount = 50
        pin = 4152

        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&amount={amount}&pin={pin}"
        response = requests.get(url)
        response_data = response.json()


        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success : {response_data.get('message', '')}", bg="green")
            res_label.config(text=f"Withdraw amount is {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

def withdraw_money_ByOtp_on_submit():
    try:
        #atm_card_number = otp_card_number_entry.get()
        atm_card_number = 4526324512632541
        otp = "60XV87"
        #otp = otp_entry.get()
        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&otp={otp}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success : {response_data.get('message', '')}", bg="green")
            res_label.config(text=f"Withdraw Money is {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")

    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

# Exit button function
def exit_app():
    root.quit()

# Welcome Frame
welcome_label = tk.Label(welcome_frame, text="Welcome, In MINI Bank", bg='light blue', font=('Helvetica', 50))
welcome_label.pack(expand=True)
welcome_frame.bind("<Button-1>", lambda e: show_frame(options_frame))

# Options Frame
options = [
    ("Money Transfer", transfer_frame),
    ("Withdraw Money", withdraw_frame),
    ("Withdraw by OTP", withdraw_otp_frame),
    ("Check Balance", check_balance_frame)
]

for i, (text, frame) in enumerate(options):
    button = tk.Button(options_frame, text=text, font=('Helvetica', 18), command=lambda f=frame: show_frame(f))
    button.grid(row=i // 2, column=i % 2, padx=20, pady=20, sticky='nsew')

# Add Exit and Home buttons
exit_button = tk.Button(root, text="Exit", font=('Helvetica', 18), command=exit_app)
exit_button.place(relx=0.95, rely=0.05, anchor='ne')

home_button = tk.Button(root, text="Home", font=('Helvetica', 18), command=lambda: show_frame(welcome_frame))
home_button.place(relx=0.05, rely=0.05, anchor='nw')

# Withdraw Frame
tk.Label(withdraw_frame, text="Card Number", font=('Helvetica', 18)).pack(side='top', pady=20)
card_number_entry = tk.Entry(withdraw_frame, font=('Helvetica', 18))
card_number_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(withdraw_frame, text="Amount", font=('Helvetica', 18)).pack(side='top', pady=20)
amount_entry = tk.Entry(withdraw_frame, font=('Helvetica', 18))
amount_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(withdraw_frame, text="PIN", font=('Helvetica', 18)).pack(side='top', pady=20)
pin_entry = tk.Entry(withdraw_frame, show="*", font=('Helvetica', 18))
pin_entry.pack(side='top', pady=10, fill='x', padx=20)

withdraw_button = tk.Button(withdraw_frame, text="Submit", font=('Helvetica', 18), command=withdraw_money_on_submit)
withdraw_button.pack(side='top', pady=20)

# Withdraw by OTP Frame
tk.Label(withdraw_otp_frame, text="Card Number", font=('Helvetica', 18)).pack(side='top', pady=20)
otp_card_number_entry = tk.Entry(withdraw_otp_frame, font=('Helvetica', 18))
otp_card_number_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(withdraw_otp_frame, text="OTP", font=('Helvetica', 18)).pack(side='top', pady=20)
otp_entry = tk.Entry(withdraw_otp_frame, font=('Helvetica', 18))
otp_entry.pack(side='top', pady=10, fill='x', padx=20)

otp_button = tk.Button(withdraw_otp_frame, text="Submit", font=('Helvetica', 18), command=withdraw_money_ByOtp_on_submit)
otp_button.pack(side='top', pady=20)

# Transfer Frame
tk.Label(transfer_frame, text="Card Number", font=('Helvetica', 18)).pack(side='top', pady=20)
transfer_card_number_entry = tk.Entry(transfer_frame, font=('Helvetica', 18))
transfer_card_number_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(transfer_frame, text="Account Number", font=('Helvetica', 18)).pack(side='top', pady=20)
account_number_entry = tk.Entry(transfer_frame, font=('Helvetica', 18))
account_number_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(transfer_frame, text="Amount", font=('Helvetica', 18)).pack(side='top', pady=20)
transfer_amount_entry = tk.Entry(transfer_frame, font=('Helvetica', 18))
transfer_amount_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(transfer_frame, text="PIN", font=('Helvetica', 18)).pack(side='top', pady=20)
transfer_pin_entry = tk.Entry(transfer_frame, show="*", font=('Helvetica', 18))
transfer_pin_entry.pack(side='top', pady=10, fill='x', padx=20)

transfer_button = tk.Button(transfer_frame, text="Submit", font=('Helvetica', 18), command=money_transfer_on_submit)
transfer_button.pack(side='top', pady=20)

# Check Balance Frame
tk.Label(check_balance_frame, text="Card Number", font=('Helvetica', 18)).pack(side='top', pady=20)
balance_card_number_entry = tk.Entry(check_balance_frame, font=('Helvetica', 18))
balance_card_number_entry.pack(side='top', pady=10, fill='x', padx=20)

tk.Label(check_balance_frame, text="PIN", font=('Helvetica', 18)).pack(side='top', pady=20)
balance_pin_entry = tk.Entry(check_balance_frame, show="*", font=('Helvetica', 18))
balance_pin_entry.pack(side='top', pady=10, fill='x', padx=20)

balance_button = tk.Button(check_balance_frame, text="Submit", font=('Helvetica', 18), command=check_balance_on_submit)
balance_button.pack(side='top', pady=20)

# Result Frame
result_label = tk.Label(result_frame, text="", font=('Helvetica', 32))
result_label.pack(expand=True)
res_label = tk.Label(result_frame, text="", font=('Helvetica', 32))
res_label.pack(expand=True)
result_button = tk.Button(result_frame, text="Back to Home", font=('Helvetica', 18), command=lambda: show_frame(welcome_frame))
result_button.pack(side='bottom', pady=20)

# Add back buttons
back_buttons = [
    tk.Button(withdraw_frame, text="Back", font=('Helvetica', 18), command=lambda: show_frame(options_frame)),
    tk.Button(withdraw_otp_frame, text="Back", font=('Helvetica', 18), command=lambda: show_frame(options_frame)),
    tk.Button(transfer_frame, text="Back", font=('Helvetica', 18), command=lambda: show_frame(options_frame)),
    tk.Button(check_balance_frame, text="Back", font=('Helvetica', 18), command=lambda: show_frame(options_frame)),
]

for button in back_buttons:
    button.pack(side='top', pady=10)

# Set the frames to the same size
for frame in (welcome_frame, options_frame, withdraw_frame, withdraw_otp_frame, transfer_frame, check_balance_frame, result_frame):
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(welcome_frame)

root.mainloop()
