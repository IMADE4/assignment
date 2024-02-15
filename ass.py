class Bank:
    def __init__(self):
        self.customers = {}  

    def authenticate_customer(self, card_number: str, pin: str) -> bool:
        if card_number in self.customers:
            return self.customers[card_number]['pin'] == pin
        return False

    def check_balance(self, card_number: str) -> float:
        return self.customers.get(card_number, {}).get('balance', 0.0)

    def deposit_funds(self, card_number: str, amount: float) -> None:
        if card_number in self.customers:
            self.customers[card_number]['balance'] += amount

    def withdraw_cash(self, card_number: str, amount: float) -> bool:
        if card_number in self.customers:
            if self.customers[card_number]['balance'] >= amount:
                self.customers[card_number]['balance'] -= amount
                return True
        return False

class ATM:
    def __init__(self, bank: Bank):
        self.bank = bank

    def check_balance(self, card_number: str) -> float:
        return self.bank.check_balance(card_number)

    def deposit_funds(self, card_number: str, amount: float) -> None:
        self.bank.deposit_funds(card_number, amount)

    def withdraw_cash(self, card_number: str, pin: str, amount: float) -> bool:
        if self.bank.authenticate_customer(card_number, pin):
            return self.bank.withdraw_cash(card_number, amount)
        return False

class Customer:
    def __init__(self, card_number: str, pin: str):
        self.card_number = card_number
        self.pin = pin

    def enter_pin(self) -> str:
        return input("Enter your PIN: ")

    def choose_transaction_type(self) -> str:
        return input("Enter 'w' to withdraw or 'd' to deposit: ").lower()

    def choose_amount(self) -> float:
        return float(input("Enter the amount: "))

class Technician:
    def service_atm(self, atm: ATM) -> None:
        print("ATM service in progress...")
        print("ATM service completed.")

def write_balance_to_file(card_number: str, message: str) -> None:
    with open(f"{card_number}_balance.txt", "w") as file:
        file.write(message)

if __name__ == "__main__":
    bank = Bank()
    bank.customers = {
        "1234567890": {"pin": "5678", "balance": 1000.00}
    }
    atm = ATM(bank)
    customer = Customer("1234567890", "5678")
    technician = Technician()

    
    entered_pin = customer.enter_pin()
    if atm.withdraw_cash(customer.card_number, entered_pin, 0.00):
        transaction_type = customer.choose_transaction_type()
        if transaction_type == 'w':
            withdrawal_amount = customer.choose_amount()
            print("Customer checking balance...")
            print("Balance:", atm.check_balance(customer.card_number))

            print("Customer withdrawing cash...")
            if atm.withdraw_cash(customer.card_number, entered_pin, withdrawal_amount):
                print("Withdrawal of $%.2f successful." % withdrawal_amount)
                updated_balance = atm.check_balance(customer.card_number)
                print("Balance after withdrawal:", updated_balance)
                write_balance_to_file(customer.card_number, str(updated_balance))
            else:
                print("Withdrawal failed due to insufficient funds.")
        elif transaction_type == 'd':
            deposit_amount = customer.choose_amount()
            print("Customer depositing cash...")
            atm.deposit_funds(customer.card_number, deposit_amount)
            print("Deposit of $%.2f successful." % deposit_amount)
            updated_balance = atm.check_balance(customer.card_number)
            print("Balance after deposit:", updated_balance)
            write_balance_to_file(customer.card_number, str(updated_balance))
        else:
            print("Invalid transaction type.")
    else:
        print("PIN is incorrect.")
        write_balance_to_file(customer.card_number, "PIN is incorrect.")

    
    if atm.withdraw_cash(customer.card_number, entered_pin, 0.00):
        technician.service_atm(atm)
