import tkinter as tk
from tkinter import messagebox
import requests
import cv2
from pyzbar import pyzbar
import threading

# Function to scan QR code
def scan_qr_code(entry):
    def run_scanner():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            decoded_objects = pyzbar.decode(frame)
            for obj in decoded_objects:
                atm_card_number = obj.data.decode("utf-8")
                entry.delete(0, tk.END)
                entry.insert(0, atm_card_number)
                cap.release()
                cv2.destroyAllWindows()
                return
            cv2.imshow("Scan QR Code", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    thread = threading.Thread(target=run_scanner)
    thread.start()

# Create the main application window
root = tk.Tk()
root.title("MINI Bank ATM")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight() - 400))  # Set full size without covering the taskbar

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
        atm_card_number = balance_card_number_entry.get()
        pin = balance_pin_entry.get()
        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&pin={pin}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success: Available Balance is {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

def money_transfer_on_submit():
    try:
        atm_card_number = transfer_card_number_entry.get()
        account_no = account_number_entry.get()
        amount = transfer_amount_entry.get()
        pin = transfer_pin_entry.get()
        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&account_no={account_no}&amount={amount}&pin={pin}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success: {response_data.get('message', '')}", bg="green")
            res_label.config(text=f"Transfer amount was {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

def withdraw_money_on_submit():
    try:
        atm_card_number = card_number_entry.get()
        amount = amount_entry.get()
        pin = pin_entry.get()
        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&amount={amount}&pin={pin}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success: {response_data.get('message', '')}", bg="green")
            res_label.config(text=f"Withdraw amount is {balance_str}", bg="green")
        else:
            result_label.config(text=f"Failed: {response_data.get('message', '')}", bg="red")
    except Exception as e:
        result_label.config(text=f"Error: {e}", bg="red")
    show_frame(result_frame)

def withdraw_money_ByOtp_on_submit():
    try:
        atm_card_number = otp_card_number_entry.get()
        otp = otp_entry.get()
        url = f"http://127.0.0.1:8000/api/atm_transaction/?atm_card_number={atm_card_number}&otp={otp}"
        response = requests.get(url)
        response_data = response.json()

        if response_data.get('success'):
            balance = response_data.get('balance')
            balance_str = str(balance) if balance is not None else 'N/A'
            result_label.config(text=f"Success: {response_data.get('message', '')}", bg="green")
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
    button = tk.Button(options_frame, text=text, font=('Helvetica', 14), width=20, height=2, command=lambda f=frame: show_frame(f))
    button.grid(row=i // 2, column=i % 2, padx=20, pady=20, sticky='nsew')

# Add Exit and Home buttons
exit_button = tk.Button(root, text="Exit", font=('Helvetica', 14), width=10, height=2, command=exit_app)
exit_button.place(relx=0.95, rely=0.05, anchor='ne')

home_button = tk.Button(root, text="Home", font=('Helvetica', 14), width=10, height=2, command=lambda: show_frame(welcome_frame))
home_button.place(relx=0.05, rely=0.05, anchor='nw')

# Withdraw Frame
for i in range(6):
    withdraw_frame.rowconfigure(i, weight=1)
for j in range(2):
    withdraw_frame.columnconfigure(j, weight=1)

tk.Label(withdraw_frame, text="Card Number", font=('Helvetica', 14)).grid(row=8, column=8, pady=20, sticky='e')
card_number_entry = tk.Entry(withdraw_frame, font=('Helvetica', 14), width=25)
card_number_entry.grid(row=8, column=13, pady=10)

scan_qr_button = tk.Button(withdraw_frame, text="Scan QR Code", font=('Helvetica', 14), command=lambda: scan_qr_code(card_number_entry))
scan_qr_button.grid(row=9, column=12, columnspan=2, pady=10)

tk.Label(withdraw_frame, text="Amount", font=('Helvetica', 14)).grid(row=11, column=8, pady=20, sticky='e')
amount_entry = tk.Entry(withdraw_frame, font=('Helvetica', 14), width=25)
amount_entry.grid(row=11, column=13, pady=10)

tk.Label(withdraw_frame, text="PIN", font=('Helvetica', 14)).grid(row=13, column=8, pady=20, sticky='e')
pin_entry = tk.Entry(withdraw_frame, show="*", font=('Helvetica', 14), width=25)
pin_entry.grid(row=13, column=13, pady=10)

withdraw_button = tk.Button(withdraw_frame, text="Submit", font=('Helvetica', 14), width=20, height=2, command=withdraw_money_on_submit)
withdraw_button.grid(row=14, column=13, columnspan=2, pady=20)

# Withdraw by OTP Frame
for i in range(6):
    withdraw_otp_frame.rowconfigure(i, weight=1)
for j in range(2):
    withdraw_otp_frame.columnconfigure(j, weight=1)

tk.Label(withdraw_otp_frame, text="Card Number", font=('Helvetica', 14)).grid(row=8, column=8, pady=20, sticky='e')
otp_card_number_entry = tk.Entry(withdraw_otp_frame, font=('Helvetica', 14), width=25)
otp_card_number_entry.grid(row=8, column=13, pady=10)

scan_qr_button = tk.Button(withdraw_otp_frame, text="Scan QR Code", font=('Helvetica', 14), command=lambda: scan_qr_code(otp_card_number_entry))
scan_qr_button.grid(row=9, column=12, columnspan=2, pady=10)

tk.Label(withdraw_otp_frame, text="OTP", font=('Helvetica', 14)).grid(row=11, column=8, pady=20, sticky='e')
otp_entry = tk.Entry(withdraw_otp_frame, font=('Helvetica', 14), width=25)
otp_entry.grid(row=11, column=13, pady=10)

withdraw_by_otp_button = tk.Button(withdraw_otp_frame, text="Submit", font=('Helvetica', 14), width=20, height=2, command=withdraw_money_ByOtp_on_submit)
withdraw_by_otp_button.grid(row=13, column=13, columnspan=2, pady=20)

# Transfer Frame
for i in range(6):
    transfer_frame.rowconfigure(i, weight=1)
for j in range(2):
    transfer_frame.columnconfigure(j, weight=1)

tk.Label(transfer_frame, text="Card Number", font=('Helvetica', 14)).grid(row=8, column=8, pady=20, sticky='e')
transfer_card_number_entry = tk.Entry(transfer_frame, font=('Helvetica', 14), width=25)
transfer_card_number_entry.grid(row=8, column=13, pady=10)

scan_qr_button = tk.Button(transfer_frame, text="Scan QR Code", font=('Helvetica', 14), command=lambda: scan_qr_code(transfer_card_number_entry))
scan_qr_button.grid(row=9, column=12, columnspan=2, pady=10)

tk.Label(transfer_frame, text="Account Number", font=('Helvetica', 14)).grid(row=11, column=8, pady=20, sticky='e')
account_number_entry = tk.Entry(transfer_frame, font=('Helvetica', 14), width=25)
account_number_entry.grid(row=11, column=13, pady=10)

tk.Label(transfer_frame, text="Amount", font=('Helvetica', 14)).grid(row=13, column=8, pady=20, sticky='e')
transfer_amount_entry = tk.Entry(transfer_frame, font=('Helvetica', 14), width=25)
transfer_amount_entry.grid(row=13, column=13, pady=10)

tk.Label(transfer_frame, text="PIN", font=('Helvetica', 14)).grid(row=15, column=8, pady=20, sticky='e')
transfer_pin_entry = tk.Entry(transfer_frame, show="*", font=('Helvetica', 14), width=25)
transfer_pin_entry.grid(row=15, column=13, pady=10)

transfer_button = tk.Button(transfer_frame, text="Submit", font=('Helvetica', 14), width=20, height=2, command=money_transfer_on_submit)
transfer_button.grid(row=17, column=13, columnspan=2, pady=20)

# Check Balance Frame
for i in range(6):
    check_balance_frame.rowconfigure(i, weight=1)
for j in range(2):
    check_balance_frame.columnconfigure(j, weight=1)

tk.Label(check_balance_frame, text="Card Number", font=('Helvetica', 14)).grid(row=8, column=8, pady=20, sticky='e')
balance_card_number_entry = tk.Entry(check_balance_frame, font=('Helvetica', 14), width=25)
balance_card_number_entry.grid(row=8, column=13, pady=10)

scan_qr_button = tk.Button(check_balance_frame, text="Scan QR Code", font=('Helvetica', 14), command=lambda: scan_qr_code(balance_card_number_entry))
scan_qr_button.grid(row=9, column=12, columnspan=2, pady=10)

tk.Label(check_balance_frame, text="PIN", font=('Helvetica', 14)).grid(row=11, column=8, pady=20, sticky='e')
balance_pin_entry = tk.Entry(check_balance_frame, show="*", font=('Helvetica', 14), width=25)
balance_pin_entry.grid(row=11, column=13, pady=10)

check_balance_button = tk.Button(check_balance_frame, text="Submit", font=('Helvetica', 14), width=20, height=2, command=check_balance_on_submit)
check_balance_button.grid(row=13, column=13, columnspan=2, pady=20)

# Result Frame




res = tk.Label(result_frame, text="", font=('Helvetica', 20))
res.grid(row=6, column=13, pady=20)
result_label = tk.Label(result_frame, text="", font=('Helvetica', 20))
result_label.grid(row=8, column=13, pady=20)
res_label = tk.Label(result_frame, text="", font=('Helvetica', 20))
res_label.grid(row=10, column=13, pady=20)

# Add back button to all frames
for frame in (options_frame, withdraw_frame, withdraw_otp_frame, transfer_frame, check_balance_frame, result_frame):
    back_button = tk.Button(frame, text="Back", font=('Helvetica', 14), width=10, height=2, command=lambda f=options_frame: show_frame(f))
    back_button.grid(row=20, column=2, pady=10)

# Show the welcome frame initially
for frame in (welcome_frame, options_frame, withdraw_frame, withdraw_otp_frame, transfer_frame, check_balance_frame, result_frame):
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(welcome_frame)

# Run the application
root.mainloop()
