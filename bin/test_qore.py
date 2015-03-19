# sudo pip install pytest
# sudo pip install nose
from nose.tools import *
from qore import *
import numpy as n
import pandas as p

def test_answer():
    ''
    #assert debug('test', 9) == "test"
    #assert fetchURL('http://www.google.com') == "test"
    #assert lynxDump2('http://www.google.com') == "test"
    #assert mkdir_p('/tmp/testdir123') == "test"
    df = p.DataFrame([['a','b','c'],['buy','sell','sell'],[1,2,3]], index=['pair', 'bias', 'amount']).transpose()
    assert prepTestDataFrame(df) == ['a', 'buy', 1, 'b', 'sell', 2, 'c', 'sell', 3]
