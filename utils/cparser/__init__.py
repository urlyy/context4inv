
import os
import warnings

from tree_sitter import Language, Parser, Tree, Node
def init_tree(code:str)->tuple[Tree,Language]:
    warnings.simplefilter("ignore", category=FutureWarning) 
    module_dir = os.path.dirname(os.path.abspath(__file__))
    so_file = os.path.join(module_dir,'build/my-languages.so')
    Language.build_library(
        so_file,
        [
            os.path.join(module_dir,'vendor/tree-sitter-c') ,
        ]
    )
    C_LANGUAGE = Language(so_file, 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)
    tree = parser.parse(bytes(code, "utf-8"))
    return tree,C_LANGUAGE