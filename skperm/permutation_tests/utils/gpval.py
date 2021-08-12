import numpy as np

def gpva(g,df1,df2,twotail):
    if df1>1:
        df2=np.ones_like(g)*df2
    B=(df1*g/df2)/(1+df1*g/df2)
    pass