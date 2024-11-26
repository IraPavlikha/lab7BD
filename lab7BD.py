import sqlite3
from datetime import datetime

# Підключення до бази даних
connection = sqlite3.connect('banking.db')
cursor = connection.cursor()

# Функція для вставки нового клієнта
def add_customer():
    full_name = input("Введіть ім'я та прізвище клієнта: ")
    email = input("Введіть email клієнта: ")
    phone_number = input("Введіть номер телефону клієнта: ")
    address = input("Введіть адресу клієнта: ")

    # Вставка нового клієнта без вказування ClientID
    cursor.execute('''
        INSERT INTO Clients (FullName, Email, PhoneNumber, Address)
        VALUES (?, ?, ?, ?)
    ''', (full_name, email, phone_number, address))

    connection.commit()
    print(f"Клієнта {full_name} додано успішно!")

# Функція для пошуку клієнта за email
def find_customer_by_email():
    email = input("Введіть email для пошуку: ")
    cursor.execute('''
        SELECT * FROM Clients WHERE Email = ?
    ''', (email,))
    customer = cursor.fetchone()

    if customer:
        print(f"Клієнт знайдений: {customer[1]}, Email: {customer[2]}, Телефон: {customer[3]}, Адреса: {customer[4]}")
    else:
        print("Клієнт не знайдений!")

# Функція для додавання нового рахунку
def add_account():
    client_id = int(input("Введіть ID клієнта: "))
    account_number = input("Введіть номер рахунку: ")
    account_type = input("Введіть тип рахунку (Current/Savings/Credit): ")
    balance = float(input("Введіть баланс рахунку: "))
    currency = input("Введіть валюту рахунку (наприклад, USD, EUR): ")

    cursor.execute('''
        INSERT INTO Accounts (ClientID, AccountNumber, AccountType, Balance, Currency)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_id, account_number, account_type, balance, currency))

    connection.commit()
    print(f"Рахунок {account_number} додано успішно!")

# Функція для оновлення балансу рахунку
def update_balance():
    account_id = int(input("Введіть ID рахунку для оновлення балансу: "))
    new_balance = float(input("Введіть новий баланс: "))
    
    cursor.execute('''
        UPDATE Accounts SET Balance = ? WHERE AccountID = ?
    ''', (new_balance, account_id))
    
    connection.commit()
    print(f"Баланс рахунку оновлено до {new_balance}.")

# Функція для додавання транзакції
def add_transaction():
    account_id = int(input("Введіть ID рахунку: "))
    transaction_type = input("Введіть тип транзакції (Deposit/Withdrawal): ")
    amount = float(input("Введіть суму транзакції: "))
    description = input("Введіть опис транзакції: ")

    cursor.execute('''
        INSERT INTO Transactions (AccountID, TransactionType, Amount, Description)
        VALUES (?, ?, ?, ?)
    ''', (account_id, transaction_type, amount, description))

    connection.commit()
    print(f"Транзакція {transaction_type} на суму {amount} додана успішно!")

# Функція для видалення транзакції
def delete_transaction():
    transaction_id = int(input("Введіть ID транзакції для видалення: "))
    
    cursor.execute('''
        DELETE FROM Transactions WHERE TransactionID = ?
    ''', (transaction_id,))
    
    connection.commit()
    print(f"Транзакцію {transaction_id} видалено успішно!")
    
# Функція для видалення клієнта за ClientID
def delete_customer_by_id():
    client_id = int(input("Введіть ID клієнта для видалення: "))

    # Виконання SQL запиту для видалення клієнта
    cursor.execute('''
        DELETE FROM Clients WHERE ClientID = ?
    ''', (client_id,))

    connection.commit()

    if cursor.rowcount > 0:
        print(f"Клієнт з ID {client_id} успішно видалений!")
    else:
        print(f"Клієнт з ID {client_id} не знайдений.")

# Функція для основного меню
def main_menu():
    while True:
        print("\nОберіть опцію:")
        print("1. Додати клієнта")
        print("2. Знайти клієнта за email")
        print("3. Додати рахунок")
        print("4. Оновити баланс рахунку")
        print("5. Додати транзакцію")
        print("6. Видалити транзакцію")
        print("7. Видалити клієнта за ID")  # Додано нову опцію
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
        elif choice == '7':  # Обробка вибору для видалення клієнта
            delete_customer_by_id()
        elif choice == '8':
            break
        else:
            print("Невірний вибір, будь ласка, спробуйте знову.")

# Запуск основного меню
if __name__ == "__main__":
    main_menu()

    # Закриття з'єднання з базою даних
    connection.close()
