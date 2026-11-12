print("expense calculator using csv files")

def say(message:str, err:bool =False)->None:
    if err:
        print(f"Error-------{message}-----!")
    else:
        print(message)

a = 4+5
b = 4+3

say(f"error in {a}",err = True)
say(f"{b}",err = False)
say(f"{b}")


