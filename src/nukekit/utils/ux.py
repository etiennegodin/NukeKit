from typing import Literal, get_args, get_origin, Any

return_type = Literal['bool', 'str']

def add_question_mark(question:str)->str:
    if not question.endswith('?'):
        question += '?'
    return question

def format_options_list(options:Any):
    if get_origin(options) is Literal:
        options = list(get_args(options))
    return options

def user_input_choice(question:str, options:list = ['y','n'], type:return_type = 'bool')-> bool | str:
    correct = False
    question = add_question_mark(question)
    options = format_options_list(options)

    while not correct:
        user_input_choice = input(f"{question} {[o for o in options]} ")
        if user_input_choice in options:
            correct = True
        else:
            print("\033[1A\033[K", end="") 

    if type == 'bool':
        return user_input_choice == 'y'
    return user_input_choice
