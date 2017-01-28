
import pandas as p
import sys

df = p.read_csv(sys.argv[1])
df['lots'] = df['amount2'] / 100000.0
with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
  print df
