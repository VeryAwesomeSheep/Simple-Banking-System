import sys, sqlite3, random

conn = sqlite3.connect('card.db')
c = conn.cursor()

def table_creation():
    c.execute('''CREATE TABLE IF NOT EXISTS card
         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         number TEXT NOT NULL,
         pin TEXT NOT NULL,
         balance INTEGER DEFAULT 0)''')
    conn.commit()

def welcome():
    print("", "Welcome to Very Awesome Bank!", "", sep = "\n")

def menu_nli(): #menu for not logged in users
    while True:
        print("1. Create an account", "2. Log into account", "0. Exit", sep = "\n")
        menu_pick = int(input())
        if menu_pick == 0:
            exit_app()
        elif menu_pick == 1:
            account_creator()
        elif menu_pick == 2:
            login()
        else:
            print("", "Please choose the number of existing operation.", "", sep = "\n")

def menu_li(card_input): #menu for logged in users
        while True:
            print("1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit", sep = "\n")
            menu_pick = int(input())
            if menu_pick == 0:
                exit_app()
            elif menu_pick == 1:
                balance(card_input)
                continue
            elif menu_pick == 2:
                add_income(card_input)
                continue
            elif menu_pick == 3:
                transfer(card_input)
                continue
            elif menu_pick == 4:
                close_account(card_input)
                continue
            elif menu_pick == 5:
                print("", "You have successfully logged out!", "", sep = "\n")
                menu_nli()
            else:
                print("", "Please choose the number of existing operation.", "", sep = "\n")

def login(): #login to account
    print("", "Enter your card number:", sep = "\n")
    card_input = input()
    c.execute("SELECT number FROM card WHERE number=?", (card_input,))
    card_check = c.fetchone()
    print("Enter your PIN:")
    pin_input = input()
    c.execute("SELECT pin FROM card WHERE number = ?", (card_input,))
    pin_check = c.fetchone()
    if card_check == None:
        print("", "Wrong card number or PIN!", "", sep = "\n") #card not in DB -> login failed
    else: 
        if pin_input in pin_check:
            print("", "You have successfully logged in!", "", sep = "\n") #correct card and pin numbers -> login successful
            menu_li(card_input)
        elif pin_input != pin_check:
            print("", "Wrong card number or PIN!", "", sep = "\n") #wrong pin -> login failed

def exit_app():
    conn.close()
    print("\nBye!")
    sys.exit()

def balance(card_input): #check balance
    c.execute("SELECT balance FROM card WHERE number=?", (card_input,))
    balance = c.fetchone()
    print(" \n", "Balance:", balance[0], " \n")

def close_account(card_input): #delete account from database
    c.execute("DELETE FROM card WHERE number=?", (card_input,))
    conn.commit()
    print("", "The account has been closed!", "", sep = "\n")
    menu_nli()

def add_income(card_input): #add money to account
    print("", "Enter income:", sep = "\n")
    amount = int(input())
    c.execute("UPDATE card SET balance=balance+? WHERE number=?", (amount, card_input,))
    conn.commit()
    print("Income was added!", "", sep = "\n")

def transfer(card_input): #money transfer between accounts
    c.execute("SELECT balance FROM card WHERE number=?", (card_input,))
    balance = c.fetchone()
    print("", "Transfer", "Enter card number:", sep = "\n")
    destination_card = input()
    checksum = luhn_validation(destination_card)
    if destination_card[15] == checksum:
        c.execute("SELECT number FROM card WHERE number=?", (destination_card,))
        destination_check = c.fetchone()
        if destination_check == None:
            print("Such a card does not exist.", "", sep = "\n")
        else:
            print("Enter how much money you want to transfer:")
            amount = int(input())
            if amount <= balance[0]:
                c.execute("UPDATE card SET balance=balance-? WHERE number=?", (amount, card_input,))
                c.execute("UPDATE card SET balance=balance+? WHERE number=?", (amount, destination_card,))
                conn.commit()
                print("Success!", "", sep = "\n")
            else:
                print("Not enough money!", "", sep = "\n")    
    else:
        print("Probably you made mistake in the card number. Please try again!", "", sep = "\n")

def account_creator(): #account generation
    iin = "400000" #predefined iin
    account_identifier = ""
    while (len(account_identifier)) < 9: #generating unique account identifying number
        number = str(random.randint(0, 9))
        account_identifier += number
    an = iin + account_identifier #calculating checksum using luhn algorithm
    checksum = luhn_checksum_generation(an)
    card_number = an + checksum #generated card number
    card_pin = str(random.randint(1000, 9999)) #generated pin
    balance = 0
    c.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (None, card_number, card_pin, balance)) #adding account data to DB
    conn.commit()
    print("", "Your card has been created", "Your card number:", card_number, "Your card PIN:", card_pin, "", sep = "\n")

def luhn_checksum_generation(an):
    an = [int(i) for i in an]
    for i in range(0, 15, 2):
        an[i] *= 2
    for i in range(0, 15):
        if an[i] > 9:
            an[i] -= 9
    checksum = str(sum(an) * 9)
    checksum = str(int(checksum[len(checksum)-1]))
    return checksum

def luhn_validation(destination_card):
    lv = destination_card[:-1]
    lv = [int(i) for i in lv]
    for i in range(0, 15, 2):
        lv[i] *= 2
    for i in range(0, 15):
        if lv[i] > 9:
            lv[i] -= 9
    checksum = str(sum(lv) * 9)
    checksum = str(int(checksum[len(checksum)-1]))
    return checksum
    
table_creation()
welcome()
menu_nli()
