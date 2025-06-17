from game import Game

def get_user_menu_choice() : 

    try : 
        choice = input("What do you want to do : 1.Play a new game  2.Show scores  q.Quit")
        if choice in ('1', '2', "q") : 
            if choice == '1' : 
                return 1
            elif choice == '2' : 
                return 2
            else : 
                return "q"
        else : 
            print("Enter a value between 1, 2 or 3 ")
    except ValueError : 
        print("Enter a correct value")


def print_results(results) : 

    print(f"these are the results of your games : {results}")
    print("Thank you for playing !!!")


def main() : 

    results = {
        "win" : 0,
        "loss" : 0, 
        "draw"  : 0
        }

    while True : 
        choice = get_user_menu_choice()
        if choice == None : 
            continue
    
        elif choice == 1 : 

            game = Game()
            result = game.play()
            results[result] +=1
        
        elif choice == 2 :
            print_results(results)
        
        elif choice == "q" : 
            break


