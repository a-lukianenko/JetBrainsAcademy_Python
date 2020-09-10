# Write your code here
import random


class RockPaperScissors:
    def __init__(self):
        self.rating = 0

    def less_more(self, options: list, player: str) -> tuple:
        idx = options.index(player)
        length = int((len(options) - 1) / 2)
        diff = len(options[idx + 1:]) - length
        if diff == 0:
            more = options[idx + 1:]
            less = options[:idx]
        elif diff < 0:
            more = options[idx + 1:] + options[:abs(diff)]
            less = options[idx - length:idx]
        else:
            more = options[idx + 1:(idx + 1 + length)]
            less = options[:idx] + options[-diff:]
        return more, less
    
    def start(self):
        print("Enter your name: ", end="")
        name = input()
        print("Hello,", name)
        with open("rating.txt", "r+", encoding="utf-8") as rating_file:
            ratings = rating_file.readlines()
            for rating in ratings:
                self.rating = int(rating.split(" ")[1]) if name in rating else self.rating
        options = input().split(',')
        if len(options) == 1:
            options = ['paper', 'scissors', 'rock']
        print("Okay, let's start")
        while True:
            player = input().strip()
            if player == "!exit":
                print("Bye!")
                break
            elif player == "!rating":
                print("Your rating:", self.rating)
                continue
            elif player in options:
                computer = random.choice(options)
                if player == computer:
                    self.rating += 50
                    print(f"There is a draw {player}")
                    continue
                else:
                    more, less = self.less_more(options, player)
                    if computer in less:
                        self.rating += 100
                        print(f"Well done. The computer chose {computer} and failed")
                        continue
                    else:
                        print(f"Sorry, but the computer chose {computer}")
                        continue
            else:
                print("Invalid input")
                continue


RockPaperScissors().start()
