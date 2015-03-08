# sudo pip install pytest
# sudo pip install nose
from nose.tools import *
from qore import *
import numpy as n

def assertSequenceEqual(it1, it2):
    # source: http://stackoverflow.com/questions/17779526/python-nameerror-global-name-assertequal-is-not-defined
    #assertEqual(tuple(it1), tuple(it2)) # Python 2.7
    assert_equals(tuple(it1), tuple(it2))

def assertDatasetEqual(it1, it2):
    print type(it1)
    it1 =  it1.transpose().get_values()[0]
    print list(it1)
    print list(it2)
    #raise
    #print type(it2)
    assert_equals(tuple(it1), tuple(it2))
    #.transpose().get_values()

def test_answer():
    ''
    #assert debug('test', 9) == "test"
    #assert fetchURL('http://www.google.com') == "test"
    #assert lynxDump2('http://www.google.com') == "test"
    #assert mkdir_p('/tmp/testdir123') == "test"
    assert isRange([1, 2, 3, 4, 3, 2, 9, 3, 1, 1]) == False
    assert isRange([1, 2, 3, 4])                   == True
    assert isRange([1, 2, 3, 4, 5,6,7,8,9,10,11])  == True
    assert isRange([1, 2, 3, 4, 6, 7, 9, 10, 11])  == False
    assertSequenceEqual(isRange([1, 2, 3, 4, 3, 2, 9, 3, 1, 1], rangeHasMissingIntegers=True), [1, 2, 3, 4, 0, 0, 0, 0, 9])
    assertSequenceEqual(isRange([1, 2, 4, 3, 2, 9, 11, 1],      rangeHasMissingIntegers=True), [1, 2, 3, 4, 0, 0, 0, 0, 9, 0, 11])
    assertSequenceEqual(isRange([1, 2, 4, 3, 2, 9, 11, 1],      rangeHasMissingIntegers=True), [1, 2, 3, 4, 0, 0, 0, 0, 9, 0, 11])
    
    assertSequenceEqual(isRange([1, 2, 3, 4],                   rangeHasMissingIntegers=True), [1, 2, 3, 4])
    assertSequenceEqual(isRange([1, 2, 4, 3, 2, 9, 11, 1],      rangeHasMissingIntegers=True), [1, 2, 3, 4, 0, 0, 0, 0, 9, 0, 11])
    assertSequenceEqual(isRange([1, 2, 3, 4, 3, 2, 9, 3, 1, 1], rangeHasMissingIntegers=True), [1, 2, 3, 4, 0, 0, 0, 0, 9])
    assertSequenceEqual(isRange([1,2,4,6,8,9],                  rangeHasMissingIntegers=True), [1, 2, 0, 4, 0, 6, 0, 8, 9])
