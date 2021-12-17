import numpy as np
import os


def miscread(filename, **kwargs):
    useniiclass = True
    tmppath = "/tmp"
    X = {"filename": filename}
    _, file_extension = os.path.splitext(X["filename"])
    if file_extension in ["txt", "csv"]:
        X.data = np.loadtxt(filename)
    elif file_extension in ["npy", "npz"]:
        X.data = np.load(filename)
    elif file_extension in ["mat", "con", "fts", "grp"]:
        # TODO
        raise NotImplementedError
    elif file_extension == "gz":
        # TODO
        raise NotImplementedError
    elif file_extension in ["nii", "hdr", "img"]:
        # TODO
        raise NotImplementedError
    elif file_extension in ["dpv", "dpf", "dpx"]:
        # TODO
        raise NotImplementedError
    elif file_extension == "srf":
        # TODO
        raise NotImplementedError
    elif file_extension == "obj":
        # TODO
        raise NotImplementedError
    elif file_extension == "mz3":
        # TODO
        raise NotImplementedError
    elif file_extension in [
        "area",
        "avg_curv",
        "crv",
        "curv",
        "h",
        "k",
        "jacobian_white",
        "mid",
        "sulc",
        "thickness",
        "volume",
        "gwc",
    ]:
        # TODO
        raise NotImplementedError
    elif file_extension in [
        "inflated",
        "nofix",
        "orig",
        "pial",
        "smoothwm",
        "sphere",
        "reg",
        "white",
        "white_reg",
    ]:
        # TODO
        raise NotImplementedError
    elif file_extension in ["mgh", "mgz"]:
        # TODO
        raise NotImplementedError
    elif file_extension == "annot":
        # TODO
        raise NotImplementedError
    elif file_extension == "gii":
        # TODO
        raise NotImplementedError
    return X
