# sudo pip install pytest
# sudo pip install nose
from nose.tools import *
from qore import *
import numpy as n

def test_answer():
    assert debug('test', 9) == "test"
    #assert fetchURL('http://www.google.com') == "test"
    #assert lynxDump2('http://www.google.com') == "test"
    #assert mkdir_p('/tmp/testdir123') == "test"
