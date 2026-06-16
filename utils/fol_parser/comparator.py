from collections import defaultdict
try:
    from .parser import fol_to_z3, BinOp, BooleanLiteral, Exists, ForAll, Identifier, Number, ArraySelect, NotOp
except:
    from parser import fol_to_z3, BinOp, BooleanLiteral, Exists, ForAll, Identifier, Number, ArraySelect, NotOp

if __name__ == "__main__":
    ast1, _ = fol_to_z3("∀_a ( (_a >= 0 && _a < i) => max >= a[_a] )")
    ast2, _ = fol_to_z3("∀_a((0 <= _a && _a < i) => max >= a[_a])")
    print(ast1==ast2)