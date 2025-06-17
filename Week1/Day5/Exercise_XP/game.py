import random 

class Game:

    def get_user_item(self) :

       while True : 

           try :
               value = int(input("Enter a value between 1.rock  2.paper  3.scissors : ")) 
               if value in (1,2,3) :
                   if value == 1 : 
                      return "rock"
                   elif value == 2 : 
                      return "paper"
                   else : 
                      return "scissors"
               else : 
                   print("Enter a value between 1, 2 or 3")
           except ValueError :
               print("Enter an integer please.")

    def get_computer_item(self) : 

        item = ["rock", "paper", "scissors"] 
        return random.choice(item)
    
    def get_game_result(self, user_item, computer_item) : 

        if user_item == computer_item : 
            return "draw"
        elif (user_item == "rock" and computer_item == "scissors" or
              user_item == "paper" and computer_item == "rock" or
              user_item == "scissors" and computer_item == "paper") : 
            return "win"
        else : 
            return "loss"

    def play(self) :

        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)
        print(f"you selected {user_item}. The computer selected {computer_item}. You {result}.")
        return result


        