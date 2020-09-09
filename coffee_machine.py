# Coffee coffee machine

class CoffeeMachine:
    # coffee options and their ingredients
    coffee_options = {
        '1': {'water': 250, 'milk': 0, 'coffee_beans': 16, 'disposable_cups': 1, 'price': 4},
        '2': {'water': 350, 'milk': 75, 'coffee_beans': 20, 'disposable_cups': 1, 'price': 7},
        '3': {'water': 200, 'milk': 100, 'coffee_beans': 12, 'disposable_cups': 1, 'price': 6}
        }

    def __init__(self):
        self.initial = {
            'water': 400,
            'milk': 540,
            'coffee_beans': 120,
            'disposable_cups': 9,
            'money': 550
        }

    def check_ingredients(self, coffee_option):
        if coffee_option == "back":
            return " "
        elif coffee_option in CoffeeMachine.coffee_options:
            option = CoffeeMachine.coffee_options[coffee_option]
            count = 0
            for ingredient, value in sorted(option.items()):
                if ingredient == "price":
                    continue
                elif self.initial[ingredient] < value:
                    return f"Sorry, not enough {ingredient.replace('_', ' ')}"
                else:
                    count += 1
            if count == 4:
                for ingredient, value in sorted(option.items()):
                    if ingredient == "price":
                        self.initial['money'] += option['price']
                    else:
                        self.initial[ingredient] -= option[ingredient]

                return "I have enough resources, making you a coffee!"
        else:
            return "No such option"

    def get_machine_state(self):
        return f"""The coffee machine has:
    {self.initial['water']} ml of water
    {self.initial['milk']} ml of milk
    {self.initial['coffee_beans']} g of coffee beans
    {self.initial['disposable_cups']} of disposable cups
    {self.initial['money']} of money"""

    def process_request(self):
        while True:
            print("Write action (buy, fill, take, remaining, exit):")
            action = input().strip()
            if action == "exit":
                return
            elif action == "remaining":
                print(self.get_machine_state(), end="\n\n")
                continue
            elif action == "buy":
                print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
                coffee = input()
                print(self.check_ingredients(coffee), end="\n\n")
            elif action == "fill":
                print("Write how many ml of water you want to add: ")
                self.initial['water'] += int(input().strip())

                print("Write how many ml of milk you want to add: ")
                self.initial['milk'] += int(input().strip())

                print("Write how many grams of coffee beans you want to add: ")
                self.initial['coffee_beans'] += int(input().strip())

                print("Write how many disposable cups of coffee do you want to add: ")
                self.initial['disposable_cups'] += int(input().strip())
                print()
                continue
            elif action == "take":
                print("I gave you", self.initial['money'], end="\n\n")
                self.initial['money'] = 0
                continue


CoffeeMachine().process_request()
