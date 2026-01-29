from typing import Literal, get_args
import ast

class MyObject():
    classes = Literal['yo','ya']


obj = MyObject()

my_list = ast.literal_eval(obj.classes)
print(my_list)