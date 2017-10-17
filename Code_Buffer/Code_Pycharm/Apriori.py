# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '17/10/2017 21:50'

from itertools import combinations
import pandas as pd

trans = pd.read_table('output.txt', header=None, index_col=0)


def apriori(trans, support=0.01, minlen=1):
    ts = pd.get_dummies(trans.unstack().dropna()).groupby(level=1).sum()

    collen, rowlen = ts.shape

    # -------------Max leng (not used)
    # tssum=ts.sum(axis=1)
    # maxlen=int(tssum.loc[tssum.idxmax()])


    pattern = []
    for cnum in range(minlen, rowlen + 1):
        for cols in combinations(ts, cnum):
            patsup = ts[list(cols)].all(axis=1).sum()
            patsup = float(patsup) / collen
            pattern.append([",".join(cols), patsup])
    sdf = pd.DataFrame(pattern, columns=["Pattern", "Support"])
    results = sdf[sdf.Support >= support]

    return results
