from typing import Literal, Union, get_args, get_origin, Any
import ast

return_type = Literal['bool', 'str']

def add_question_mark(question:str)->str:
    if not question.endswith('?'):
        question += '?'
    return question

def format_options_list(options:Any):
    if get_origin(options) is Literal:
        options = list(get_args(options))
    
    return options

def user_input(question:str, options:list = ['y','n'], type:return_type = 'bool')-> bool | str:

    question = add_question_mark(question)
    options = format_options_list(options)

    correct = False
    while not correct:
        user_input = input(f"{question} {[f'{str(o)}' for o in options]} ")
        if user_input in options:
            correct = True
        else:
            print("\033[1A\033[K", end="") 

    if type == 'bool':
        return user_input == 'y'
    return user_input