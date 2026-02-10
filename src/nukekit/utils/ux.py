from typing import Literal, get_args, get_origin, Any

return_type = Literal["bool", "str"]

def add_question_mark(question:str)->str:
    if not question.endswith("?"):
        question += "?"
    return question

def format_options_list(options:Any):
    if get_origin(options) is Literal:
        options = list(get_args(options))
    return options

def user_input_choice(question:str, options:list[str] = ["y","n"], type:return_type = "bool")-> bool | str:
    """
    Ask user a question with options answers in terminal. Loops until correct answer is given.

    :param question: Question to ask
    :type question: str
    :param options: Options of correct answers. Defaults to y/n
    :type options: list[str]
    :param type: Type of return, either string or bool. Defaults to bool.
    :type type: return_type
    :return: Returns bool if y/n, str from options
    :rtype: bool | str
    """
    correct = False
    question = add_question_mark(question)
    options = format_options_list(options)

    while not correct:
        user_input_choice = input(f"{question} {[o for o in options]} ")
        if user_input_choice in options:
            correct = True
        else:
            print("\033[1A\033[K", end="") 

    if type == "bool":
        return user_input_choice == "y"
    return user_input_choice
