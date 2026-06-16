import re
try:
    from .parser import fol_to_z3
    from .ext_handler import replace_old, replace_old_for_solve
except:
    from parser import fol_to_z3
    from ext_handler import replace_old, replace_old_for_solve

from z3 import (
    IntSort,
    ArraySort,
)

def __get_sort(typ:tuple):
    type_name = typ[0]
    if type_name == "int":
        return IntSort()
    if type_name == "array":
        return ArraySort(IntSort(), __get_sort(typ[1]))