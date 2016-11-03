
import pandas as p
import numpy as n
from qorequant import QoreQuant

cc = [0.5, 1, 50, 200.0/15, 2000.0/15, 2500.0/15, 50, 500, 1000, 2400, 5000]
qq = QoreQuant(oandaInit=False, statWingInit=False)
print qq.calcCapitalRequirements(cc)
#print calcCapital(5000)
