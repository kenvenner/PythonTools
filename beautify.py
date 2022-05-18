import pprint
from attrdict import AttrDict
print('''
python -i beautify.py - should be how you started this program

then:

    1. set the variable:  eg.  out=<paste>
    2. display the variable:  eg. pp(out)

''')

def pp(out):
    pp1 = pprint.PrettyPrinter(indent=4)
    pp1.pprint(out)
