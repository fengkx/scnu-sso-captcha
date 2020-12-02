import os
from os.path import join

CODE_LEN = 4
CASESENTIVE = False

numbers = '0123456789'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
idict = numbers + uppercase
if CASESENTIVE is True:
    idict += lowercase
DICT_LEN = len(idict)


__dirname = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = join(__dirname, '..','..', 'output', 'model')