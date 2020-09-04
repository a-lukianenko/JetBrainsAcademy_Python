# Classic console game HANGMAN
import random
from string import ascii_lowercase

print("H A N G M A N", end="\n\n")
LIVES = 8
WORDS = ('python', 'java', 'kotlin', 'javascript')

word = random.choice(WORDS)
hidden_word = "-" * len(word)
tried_letters = set()


while True:
    print('Type "play" to play the game, "exit" to quit: > ', end="\n")
    option = input()
    print()
    if option == 'play':
        while LIVES > 0:
            print(hidden_word)
            if "-" not in hidden_word:
                print("You guessed the word!", "You survived!", sep="\n", end="\n\n")
                break
            else:
                print("Input a letter: ", end="")
                letter = input()
                if len(letter) != 1:
                    print("You should input a single letter", end="\n\n")
                    continue
                elif letter not in ascii_lowercase:
                    print("It is not an ASCII lowercase letter", end="\n\n")
                    continue
                elif letter in word:
                    if letter not in tried_letters:
                        print()
                        tried_letters.add(letter)
                        indices = [i for i, l in enumerate(word) if l == letter]
                        split = list(hidden_word)
                        for i, _ in enumerate(split):
                            if i in indices:
                                split[i] = letter
                        hidden_word = "".join(split)
                        continue
                    else:
                        print("You already typed this letter", end="\n\n")
                        continue
                elif letter not in word:
                    if letter not in tried_letters:
                        LIVES -= 1
                        tried_letters.add(letter)
                        if LIVES == 0:
                            print("No such letter in the word", "You are hanged!", sep="\n", end="\n\n")
                            break
                        else:
                            print("No such letter in the word", end="\n\n")
                            continue
                    else:
                        print("You already typed this letter", end="\n\n")
                        continue
    elif option == "exit":
        break
    else:
        continue
