import random
import sqlite3
import textwrap


class Bank:
    # Luhn algorithm
    def create_checksum(self, card_number: str):
        nums = list(card_number)
        mult_odd_2 = [int(num) * 2 if i % 2 == 0 else int(num) for i, num in enumerate(nums)]
        subtract_9 = [num - 9 if num > 9 else num for num in mult_odd_2]
        total = sum(subtract_9)
        return 0 if total % 10 == 0 else 10 - total % 10

    def create_card(self):
        card_number = '400000' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
        card_number += str(self.create_checksum(card_number))
        card_pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return card_number, card_pin

    def create_account(self, conn, cur, card_number, card_pin):
        cur.execute(f"""
                    INSERT INTO card (number, pin)
                    VALUES ({card_number}, {card_pin})
                    ;
                    """)
        conn.commit()
        print("Your card has been created")
        print("Your card number:", card_number, sep="\n")
        print("Your card PIN:", card_pin, sep="\n", end="\n\n")

    def get_account(self, cur, number, pin):
        cur.execute(f"""
                    SELECT number, balance
                    FROM card
                    WHERE number = {number} AND pin = {pin}
                    ;
                    """)
        return cur.fetchone()

    def update_balance(self, conn, cur, account, amount):
        cur.execute(f"""
                    UPDATE card
                    SET balance = {account[-1] + amount}
                    WHERE number = {account[0]}
                    ;
                    """)
        conn.commit()

    def start(self):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
            );
        """)
        conn.commit()
        while True:
            print(textwrap.dedent("""
                1. Create an account
                2. Log into account
                0. Exit
                """))
            option = input()
            print()

            # Exit
            if option == '0':
                conn.close()
                print("Bye!")
                break

            # Create account
            elif option == '1':
                # card_number, card_pin = self.create_card()
                self.create_account(conn, cur, *self.create_card())

            # Log into account
            elif option == '2':
                print("Enter your card number:")           
                card = input()
                print("Enter your PIN:")
                pin = input()
                print()
                user_account = self.get_account(cur, card, pin)
                if not user_account:
                    print("Wrong card number or PIN!")
                    continue
                else:
                    print("You have successfully logged in!", end="\n\n")
                    while True:
                        print(textwrap.dedent("""
                            1. Balance
                            2. Add income
                            3. Do transfer
                            4. Close account
                            5. Log out
                            0. Exit
                            """))
                        option = input()
                        print()

                        # Balance
                        if option == "1":
                            acc = self.get_account(cur, card, pin)
                            print(f"Balance: {acc[-1]}", end="\n\n")
                            continue

                        # Add income
                        elif option == "2":
                            print("Enter income: ")
                            income = input()
                            deposit_acc = self.get_account(cur, card, pin)
                            new_balance = deposit_acc[-1] + int(income)
                            cur.execute(f"""
                                        UPDATE card
                                        SET balance = {new_balance}
                                        WHERE number = {deposit_acc[0]}
                                        ;
                                        """)
                            conn.commit()
                            print("Income was added!")
                            continue

                        # Transfer
                        elif option == "3":
                            sender = self.get_account(cur, card, pin)
                            print("Transfer")
                            print("Enter card number: ")
                            receiver = input()
                            cur.execute(f"""
                                        SELECT number, balance
                                        FROM card
                                        WHERE number = {receiver}
                                        ;
                                        """)
                            receiver_account = cur.fetchone()

                            # Luhn algorithm verification
                            if int(receiver[-1]) != self.create_checksum(receiver[:-1]):
                                print("Probably you made a mistake in the card number."
                                      " Please try again!", end="\n\n")
                                continue

                            elif not receiver_account:
                                print("Such a card does not exist.", end="\n\n")
                                continue
                            elif receiver_account[0] == sender[0]:
                                print("You can't transfer money to the same account!", end="\n\n")
                                continue
                            else:
                                print("Enter how much money you want to transfer: ")
                                deposit = int(input())
                                if sender[-1] < deposit:
                                    print("Not enough money!", end="\n\n")
                                    continue
                                else:
                                    # Update receiver's account balance
                                    self.update_balance(conn, cur, receiver_account, deposit)

                                    # Update sender's account balance
                                    self.update_balance(conn, cur, sender, -deposit)

                                    print("Success!", end="\n\n")
                                    continue
                        elif option == "4":
                            cur.execute(f"""
                                        DELETE FROM card
                                        WHERE number == {user_account[0]}
                                        ;
                                        """)
                            conn.commit()
                            print("The account has been closed!", end="\n\n")
                            break
                        elif option == "5":
                            print(f"You have successfully logged out!", end="\n\n")
                            break
                        else:
                            conn.close()
                            print("Bye!")
                            return


Bank().start()
