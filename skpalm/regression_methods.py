def noz(P, Y, y, m, c, o, plm):
    """
    This is equivalent to Draper-Stoneman, as when there is no Z
    Y remains unchanged.
    """
    Mr = P @ plm.X[y][m][c][o]
    return Mr, Y

def noz3d(P, Y, y, m, c, o, plm):
    """
    This is equivalent to Draper-Stoneman, as when there is no Z
    Y remains unchanged.
    """
    Mr = P @ plm.X[y][m][c][o]
    return Mr, Y

def nozm(P, Y, y, m, c, o, plm, ikeep):
    """
    This is equivalent to Draper-Stoneman, as when there is no Z
    Y remains unchanged.
    """
    Mr = P @ plm.X[y][m][c][o]
    return Mr, Y

def exact(P, Y, y, m, c, o, plm):
    """
    The "exact" method, in which the coefficients for
    the nuisance are known.
    """
    Mr = P @ plm.X[y][m][c][o]
    return Mr, Y

def exact3d(P, Y, y, m, c, o, plm):
    """
    This is equivalent to Draper-Stoneman, as when there is no Z
    Y remains unchanged.
    """
    Mr = P @ plm.X[y][m][c][o]
    return Mr, Y

def exactm(P, Y, y, m, c, o, plm, ikeep):
    """
    The "exact" method, in which the coefficients for
    the nuisance are known.
    """
    Mr = P @ plm.X[y][m][c][o]
    return Mr, Y