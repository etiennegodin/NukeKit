


def var_user_input(question:str, options:list = ['y','n']):
    correct = False
    while not correct:
        user_input = input()
        

def bool_user_input(question:str):
    correct = False
    options = ['y', 'n']

    while not correct:
        user_input = input(question)
        if user_input in options:
            correct = True

    if user_input == 'y':
        return True
    else:
        return False