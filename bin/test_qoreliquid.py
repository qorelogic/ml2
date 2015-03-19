# sudo pip install pytest
# sudo pip install nose
from nose.tools import *
from qoreliquid import *
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
    """normalizeme x.
    >>> normalizeme([1,2,3,4,5,6,7,8,9])
    [-1.5491933384829668, -1.1618950038622251, -0.7745966692414834, -0.3872983346207417, 0.0, 0.3872983346207417, 0.7745966692414834, 1.1618950038622251, 1.5491933384829668]
    >>> normalizeme([9,8,7,6,5,4,3,2,1])
    [1.5491933384829668, 1.1618950038622251, 0.7745966692414834, 0.3872983346207417, 0.0, -0.3872983346207417, -0.7745966692414834, -1.1618950038622251, -1.5491933384829668]
    >>> normalizeme([-653.79116572766691, 487.20209159506686, -1683.7969343430511, -681.85341778816542, -490.82464027127884, -456.72780286536494, -683.29648054923473, 1079.4960144133083, -1649.1331653998573, 198.97273092263697, 925.72300657354367, 1153.5643080061998, -25.578773696034702, -488.17497026318836, 274.9940977784637, -18.845465630672383, 50.306458115569633, -18.76798478896, -724.01976174478773, 1417.8075719760191])
    [-0.67118147066088807, 0.71002165780889159, -1.9180312489774027, -0.70515158405911715, -0.47390609383318277, -0.43263095202693036, -0.70689845047342359, 1.4270094348355151, -1.876069821246239, 0.3611122386491955, 1.2408630591760705, 1.5166711030130888, 0.089286582632914474, -0.47069859678523834, 0.45313815471656527, 0.097437433748942301, 0.18114770355555607, 0.097531226398708468, -0.75619508130613555, 1.8365447048331092]
    """
    """normalizeme x.
    >>> normalizeme2([1,2,3,4,5,6,7,8,9])
    [-1.5491933384829668, -1.1618950038622251, -0.7745966692414834, -0.3872983346207417, 0.0, 0.3872983346207417, 0.7745966692414834, 1.1618950038622251, 1.5491933384829668]
    >>> normalizeme2([9,8,7,6,5,4,3,2,1])
    [1.5491933384829668, 1.1618950038622251, 0.7745966692414834, 0.3872983346207417, 0.0, -0.3872983346207417, -0.7745966692414834, -1.1618950038622251, -1.5491933384829668]
    >>> normalizeme2([-653.79116572766691, 487.20209159506686, -1683.7969343430511, -681.85341778816542, -490.82464027127884, -456.72780286536494, -683.29648054923473, 1079.4960144133083, -1649.1331653998573, 198.97273092263697, 925.72300657354367, 1153.5643080061998, -25.578773696034702, -488.17497026318836, 274.9940977784637, -18.845465630672383, 50.306458115569633, -18.76798478896, -724.01976174478773, 1417.8075719760191])
    [-0.67118147066088807, 0.71002165780889159, -1.9180312489774027, -0.70515158405911715, -0.47390609383318277, -0.43263095202693036, -0.70689845047342359, 1.4270094348355151, -1.876069821246239, 0.3611122386491955, 1.2408630591760705, 1.5166711030130888, 0.089286582632914474, -0.47069859678523834, 0.45313815471656527, 0.097437433748942301, 0.18114770355555607, 0.097531226398708468, -0.75619508130613555, 1.8365447048331092]
    """
    assertSequenceEqual(normalizeme([1,2,3,4,5,6,7,8,9]), n.array([-1.5491933384829668, -1.1618950038622251, -0.7745966692414834, -0.3872983346207417, 0.0, 0.3872983346207417, 0.7745966692414834, 1.1618950038622251, 1.5491933384829668]))
    assertSequenceEqual(normalizeme([9,8,7,6,5,4,3,2,1]), n.array([1.5491933384829668, 1.1618950038622251, 0.7745966692414834, 0.3872983346207417, 0.0, -0.3872983346207417, -0.7745966692414834, -1.1618950038622251, -1.5491933384829668]))
    assertSequenceEqual(normalizeme([-653.79116572766691, 487.20209159506686, -1683.7969343430511, -681.85341778816542, -490.82464027127884, -456.72780286536494, -683.29648054923473, 1079.4960144133083, -1649.1331653998573, 198.97273092263697, 925.72300657354367, 1153.5643080061998, -25.578773696034702, -488.17497026318836, 274.9940977784637, -18.845465630672383, 50.306458115569633, -18.76798478896, -724.01976174478773, 1417.8075719760191]), n.array([-0.67118147066088807, 0.71002165780889159, -1.9180312489774027, -0.70515158405911715, -0.47390609383318277, -0.43263095202693036, -0.70689845047342359, 1.4270094348355151, -1.876069821246239, 0.3611122386491955, 1.2408630591760705, 1.5166711030130888, 0.089286582632914474, -0.47069859678523834, 0.45313815471656527, 0.097437433748942301, 0.18114770355555607, 0.097531226398708468, -0.75619508130613555, 1.8365447048331092]))
    
    assertDatasetEqual(normalizeme2([1,2,3,4,5,6,7,8,9]), n.array([1,2,3,4,5,6,7,8,9]))
    assertDatasetEqual(normalizeme2([9,8,7,6,5,4,3,2,1]), n.array([1.0, 0.88888888888888884, 0.77777777777777779, 0.66666666666666663, 0.55555555555555558, 0.44444444444444442, 0.33333333333333331, 0.22222222222222221, 0.1111111111111111]))
    assertDatasetEqual(normalizeme2([-653.79116572766691, 487.20209159506686, -1683.7969343430511, -681.85341778816542, -490.82464027127884, -456.72780286536494, -683.29648054923473, 1079.4960144133083, -1649.1331653998573, 198.97273092263697, 925.72300657354367, 1153.5643080061998, -25.578773696034702, -488.17497026318836, 274.9940977784637, -18.845465630672383, 50.306458115569633, -18.76798478896, -724.01976174478773, 1417.8075719760191]), [1.0, -0.7451952812069782, 2.5754354335286744, 1.0429223481924315, 0.75073611575187471, 0.69858362548693775, 1.0451295709826982, -1.6511327637959647, 2.5224157985744253, -0.3043368300964745, -1.4159307361444962, -1.7644232110757987, 0.039123767705801941, 0.74668333843246659, -0.42061458183271166, 0.028824901005961828, -0.076945759980679387, 0.028706390928472259, 1.1074174747206269, -2.1685939582833074])
    assertDatasetEqual(normalizeme2([1423,2342,2343,23441,1235,1236,7123,8123,913]), [1.0, 1.6458186929023191, 1.646521433591005, 16.472944483485595, 0.86788475052705549, 0.86858749121574141, 5.0056219255094874, 5.7083626141953623, 0.64160224877020378])

    assert searchQuandl('non farm') == 20
    
    # test etoro
    df = p.DataFrame([['a','b','c'],['buy','sell','sell'],[1,2,3]], index=['pair', 'bias', 'amount']).transpose()
    assert prepTestDataFrame(polarizePortfolio(df, 'amount', 'amountPol', 'bias')) == ['a', 'buy', 1, 1.0, 'b', 'sell', 2, -2.0, 'c', 'sell', 3, -3.0]
