import random

class Game: 
    def __init__(self):
        self.rps = ["rock", "paper", "scissors", "spock", "lizard"]
        self.rand = ""
        self.answer = ""
    
    def makeItRandom(self):
        self.rand = random.choice(self.rps)
    
    def letsCheck(self):
        if self.answer == self.rand:
            print("Its a Tie! Go again.")  
            
        elif self.answer == "rock":
            if self.rand == "scissors":
                print("Rock crushes Scissors") 
            elif self.rand == "paper": 
                print("Paper covers Rock")
            elif self.rand == "lizard":
                print("Rock crushes Lizard")
            elif self.rand == "spock":
                print("Spock melts rock")    
                       
        elif self.answer == "paper":
            if self.rand == "rock":
                print("Paper covers Rock")
            elif self.rand == "scissors":
                print("Scissors cuts Paper")
            elif self.rand == "lizard":
                print("Lizard eats paper")
            elif self.rand == "spock":
                print("The truth disproves Spock")
                
        elif self.answer == "scissors":
            if self.rand == "paper":
                print("Scissors cuts Paper")
            elif self.rand == "rock":
                print("Rock crushes Scissors")
            elif self.rand == "lizard":
                print("Scissors stab lizard")
            elif self.rand == "spock":
                print("do you think scissors can hurt spock?")            
        
        elif self.answer == "lizard":
            if self.rand == "paper":
                print("Lizard eats Paper")
            elif self.rand == "rock":
                print("Rock Smashes Lizard")
            elif self.rand == "Scissors":
                print("Scissors Stab Lizard")
            elif self.rand == "spock":
                print("Lizard Poisons Spock")
        
        elif self.answer == "spock":
            if self.rand == "paper":
                print("The truth disproves Spock")
            elif self.rand == "rock":
                print("Spock Destroys Rock")
            elif self.rand == "scissors":
                print("do you think scissors can hurt spock?")
            elif self.rand == "lizard":
                print("Lizard Poisons Spock")
        
        
def main():
    g = Game()
    
    while g.answer != "q":
        print()
        g.makeItRandom()
        answer1 = input("Pick one: rock, paper, scissors, lizard, spock:  ")
        g.answer = answer1
        print(g.answer)
        g.letsCheck()
        








if __name__ == "__main__":
    main()