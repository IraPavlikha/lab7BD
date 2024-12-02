from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Налаштування бази даних
DATABASE_URL = "sqlite:///banking.db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Моделі
class Client(Base):
    __tablename__ = "clients"
    ClientID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    PhoneNumber = Column(String, nullable=False)
    Address = Column(String, nullable=False)

    accounts = relationship("Account", back_populates="client")

class Account(Base):
    __tablename__ = "accounts"
    AccountID = Column(Integer, primary_key=True, autoincrement=True)
    ClientID = Column(Integer, ForeignKey("clients.ClientID"), nullable=False)
    AccountNumber = Column(String, unique=True, nullable=False)
    AccountType = Column(String, nullable=False)
    Balance = Column(Float, default=0.0)
    Currency = Column(String, nullable=False)

    client = relationship("Client", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    TransactionID = Column(Integer, primary_key=True, autoincrement=True)
    AccountID = Column(Integer, ForeignKey("accounts.AccountID"), nullable=False)
    TransactionType = Column(String, nullable=False)
    Amount = Column(Float, nullable=False)
    Description = Column(String, nullable=True)

    account = relationship("Account", back_populates="transactions")

# Ініціалізація бази даних
Base.metadata.create_all(engine)

# Функції
def add_customer():
    full_name = input("Введіть ім'я та прізвище клієнта: ")
    email = input("Введіть email клієнта: ")
    phone_number = input("Введіть номер телефону клієнта: ")
    address = input("Введіть адресу клієнта: ")

    new_client = Client(FullName=full_name, Email=email, PhoneNumber=phone_number, Address=address)
    session.add(new_client)
    session.commit()
    print(f"Клієнта {full_name} додано успішно!")

def find_customer_by_email():
    email = input("Введіть email для пошуку: ")
    customer = session.query(Client).filter_by(Email=email).first()

    if customer:
        print(f"Клієнт знайдений: {customer.FullName}, Email: {customer.Email}, Телефон: {customer.PhoneNumber}, Адреса: {customer.Address}")
    else:
        print("Клієнт не знайдений!")

def add_account():
    client_id = int(input("Введіть ID клієнта: "))
    account_number = input("Введіть номер рахунку: ")
    account_type = input("Введіть тип рахунку (Current/Savings/Credit): ")
    balance = float(input("Введіть баланс рахунку: "))
    currency = input("Введіть валюту рахунку (наприклад, USD, EUR): ")

    new_account = Account(ClientID=client_id, AccountNumber=account_number, AccountType=account_type, Balance=balance, Currency=currency)
    session.add(new_account)
    session.commit()
    print(f"Рахунок {account_number} додано успішно!")

def update_balance():
    account_id = int(input("Введіть ID рахунку для оновлення балансу: "))
    new_balance = float(input("Введіть новий баланс: "))

    account = session.query(Account).filter_by(AccountID=account_id).first()
    if account:
        account.Balance = new_balance
        session.commit()
        print(f"Баланс рахунку оновлено до {new_balance}.")
    else:
        print("Рахунок не знайдено!")

def add_transaction():
    account_id = int(input("Введіть ID рахунку: "))
    transaction_type = input("Введіть тип транзакції (Deposit/Withdrawal): ")
    amount = float(input("Введіть суму транзакції: "))
    description = input("Введіть опис транзакції: ")

    new_transaction = Transaction(AccountID=account_id, TransactionType=transaction_type, Amount=amount, Description=description)
    session.add(new_transaction)
    session.commit()
    print(f"Транзакція {transaction_type} на суму {amount} додана успішно!")

def delete_customer_by_id():
    client_id = int(input("Введіть ID клієнта для видалення: "))
    customer = session.query(Client).filter_by(ClientID=client_id).first()

    if customer:
        session.delete(customer)
        session.commit()
        print(f"Клієнт з ID {client_id} успішно видалений!")
    else:
        print(f"Клієнт з ID {client_id} не знайдений.")

# Головне меню
def main_menu():
    while True:
        print("\nОберіть опцію:")
        print("1. Додати клієнта")
        print("2. Знайти клієнта за email")
        print("3. Додати рахунок")
        print("4. Оновити баланс рахунку")
        print("5. Додати транзакцію")
        print("6. Видалити клієнта за ID")
        print("7. Вихід")

        choice = input("Введіть номер вибору (1-7): ")

        if choice == '1':
            add_customer()
        elif choice == '2':
            find_customer_by_email()
        elif choice == '3':
            add_account()
        elif choice == '4':
            update_balance()
        elif choice == '5':
            add_transaction()
        elif choice == '6':
            delete_customer_by_id()
        elif choice == '7':
            break
        else:
            print("Невірний вибір, будь ласка, спробуйте знову.")

# Запуск програми
if __name__ == "__main__":
    main_menu()
