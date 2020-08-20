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
            print("1. Balance", "2. Log out", "0. Exit", sep = "\n")
            menu_pick = int(input())
            if menu_pick == 0:
                exit_app()
            elif menu_pick == 1:
                c.execute("SELECT * FROM card WHERE number=?", (card_input,))
                balance = c.fetchone()
                print(balance)
                print(" \n", "Balance: ", balance, " \n")
                continue
            elif menu_pick == 2:
                print("", "You have successfully logged out!", "", sep = "\n")
                menu_nli()
            else:
                print("", "Please choose the number of existing operation.", "", sep = "\n")

def exit_app():
    conn.close()
    print("\nBye!")
    sys.exit()

def account_creator(): #account generation
    iin = "400000" #predefined iin
    account_identifier = ""
    while (len(account_identifier)) < 9: #generating unique account identifying number
        number = str(random.randint(0, 9))
        account_identifier += number
    ccg = iin + account_identifier #calculating checksum using luhn algorithm
    ccg = [int(i) for i in ccg]
    for i in range(0, 15, 2):
        ccg[i] *= 2
    for i in range(0, 15):
        if ccg[i] > 9:
            ccg[i] -= 9
    checksum = str(sum(ccg) * 9)
    checksum = str(int(checksum[len(checksum)-1]))
    card_number = iin + account_identifier + checksum #generated card number
    card_pin = str(random.randint(1000, 9999)) #generated pin
    balance = 0
    c.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (None, card_number, card_pin, balance)) #adding account data to DB
    conn.commit()
    print("", "Your card has been created", "Your card number:", card_number, "Your card PIN:", card_pin, "", sep = "\n")

def login(): #login to account
    print("", "Enter your card number:", sep = "\n")
    card_input = input()
    c.execute("""SELECT number FROM card WHERE number=?""", (card_input,))
    card_check = c.fetchone()
    print("Enter your PIN:")
    pin_input = input()
    c.execute("""SELECT pin FROM card WHERE number = ?""", (card_input,))
    pin_check = c.fetchone()
    if card_check == None:
        print("", "Wrong card number or PIN!", "", sep = "\n") #card not in DB -> login failed
    else: 
        if pin_input in pin_check:
            print("", "You have successfully logged in!", "", sep = "\n") #correct card and pin numbers -> login successful
            menu_li(card_input)
        elif pin_input != pin_check:
            print("", "Wrong card number or PIN!", "", sep = "\n") #wrong pin -> login failed

table_creation()
menu_nli()
