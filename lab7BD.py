from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Ініціалізація бази даних та сесії
engine = create_engine('sqlite:///banking.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Моделі для таблиць
class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)

    accounts = relationship("Account", back_populates="client")

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, nullable=False)

    client = relationship("Client", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)

    account = relationship("Account", back_populates="transactions")

# Створення таблиць
Base.metadata.create_all(engine)

# Функції
def add_customer():
    full_name = input("Введіть ім'я та прізвище клієнта: ")
    email = input("Введіть email клієнта: ")
    phone_number = input("Введіть номер телефону клієнта: ")
    address = input("Введіть адресу клієнта: ")

    new_client = Client(full_name=full_name, email=email, phone_number=phone_number, address=address)
    session.add(new_client)
    session.commit()
    print(f"Клієнта {full_name} додано успішно!")

def find_customer_by_email():
    email = input("Введіть email для пошуку: ")
    customer = session.query(Client).filter_by(email=email).first()

    if customer:
        print(f"Клієнт знайдений: {customer.full_name}, Email: {customer.email}, Телефон: {customer.phone_number}, Адреса: {customer.address}")
    else:
        print("Клієнт не знайдений!")

def add_account():
    client_id = int(input("Введіть ID клієнта: "))
    account_number = input("Введіть номер рахунку: ")
    account_type = input("Введіть тип рахунку (Current/Savings/Credit): ")
    balance = float(input("Введіть баланс рахунку: "))
    currency = input("Введіть валюту рахунку (наприклад, USD, EUR): ")

    new_account = Account(client_id=client_id, account_number=account_number, account_type=account_type, balance=balance, currency=currency)
    session.add(new_account)
    session.commit()
    print(f"Рахунок {account_number} додано успішно!")

def update_balance():
    account_id = int(input("Введіть ID рахунку для оновлення балансу: "))
    new_balance = float(input("Введіть новий баланс: "))
    account = session.query(Account).filter_by(id=account_id).first()

    if account:
        account.balance = new_balance
        session.commit()
        print(f"Баланс рахунку оновлено до {new_balance}.")
    else:
        print("Рахунок не знайдено!")

def add_transaction():
    account_id = int(input("Введіть ID рахунку: "))
    transaction_type = input("Введіть тип транзакції (Deposit/Withdrawal): ")
    amount = float(input("Введіть суму транзакції: "))
    description = input("Введіть опис транзакції: ")

    new_transaction = Transaction(account_id=account_id, transaction_type=transaction_type, amount=amount, description=description)
    session.add(new_transaction)
    session.commit()
    print(f"Транзакція {transaction_type} на суму {amount} додана успішно!")

def delete_transaction():
    transaction_id = int(input("Введіть ID транзакції для видалення: "))
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()

    if transaction:
        session.delete(transaction)
        session.commit()
        print(f"Транзакцію {transaction_id} видалено успішно!")
    else:
        print("Транзакція не знайдена!")

def delete_customer_by_id():
    client_id = int(input("Введіть ID клієнта для видалення: "))
    customer = session.query(Client).filter_by(id=client_id).first()

    if customer:
        session.delete(customer)
        session.commit()
        print(f"Клієнта з ID {client_id} успішно видалено!")
    else:
        print("Клієнт не знайдений!")

def main_menu():
    while True:
        print("\nОберіть опцію:")
        print("1. Додати клієнта")
        print("2. Знайти клієнта за email")
        print("3. Додати рахунок")
        print("4. Оновити баланс рахунку")
        print("5. Додати транзакцію")
        print("6. Видалити транзакцію")
        print("7. Видалити клієнта за ID")
        print("8. Вихід")
        
        choice = input("Введіть номер вибору (1-8): ")

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
            delete_transaction()
        elif choice == '7':
            delete_customer_by_id()
        elif choice == '8':
            break
        else:
            print("Невірний вибір, будь ласка, спробуйте знову.")

if __name__ == "__main__":
    main_menu()
