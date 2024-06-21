from hulk.interpreter import compiler

def hulk_compile():

    f = open('main.hulk')
    p = f.read()
    f.close()

    compiler(p)

hulk_compile()
