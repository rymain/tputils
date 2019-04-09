import codecs
import os
import pickle
import random
import re
import string
import time

import numpy as np


def json_load(filename):
    import json
    with open(filename, "r") as f:
        return json.load(f)


def json_dump(d, filename):
    import json
    with open(filename, "w") as f:
        json.dump(d, f)


def pickle_load(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def pickle_dump(d, filename):
    with open(filename, "wb") as f:
        pickle.dump(d, f)


def csv_dump(rows, filename, append=False, delimiter=";"):
    import csv
    open_param = 'a' if append else 'w'
    with open(filename, open_param) as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quotechar=str('"'), quoting=csv.QUOTE_MINIMAL)
        rows = [list(row) for row in rows]  # Like copy, but converts inner tuples to lists
        writer.writerows(rows)


def csv_load(filename, delimiter=";", n=-1, skip_header=False):
    import csv
    rows = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=str('"'), quoting=csv.QUOTE_MINIMAL)

        if skip_header:
            next(reader)

        for row in reader:

            if 0 <= n <= len(rows):
                break

            rows.append(row)

    return rows


def txt_dump(rows, filename, append=False, add_new_line=True):
    open_param = 'a' if append else 'w'
    if add_new_line:
        rows = [row + "\n" for row in rows]
    with codecs.open(filename, open_param, encoding="utf-8") as f:
        f.writelines(rows)


def txt_load(filename, n=-1, strip_new_line=True):
    with codecs.open(filename, "r", encoding="utf-8") as f:

        rows = []
        for row in f:
            if strip_new_line:
                row = row.rstrip("\n")
            rows.append(row)

            if 0 <= n <= len(rows):
                break

        return rows


def make_sure_path_exists(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exception:
        import errno
        if exception.errno != errno.EEXIST:
            raise


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        import errno
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def print_info(var, name="var", output=False):
    """
    Print variable information.
    :type var: any
    :type name: str
    :return:
    """
    if isinstance(var, np.ndarray):
        out = "{}: type:{}, shape:{}, dtype:{}".format(name, type(var), var.shape, var.dtype)
    elif isinstance(var, list) or isinstance(var, tuple):
        out = "{}: type:{}, len:{}, type[0]:{}".format(name, type(var), len(var), type(var[0]) if len(var) > 0 else "")
    else:
        out = "{}: val:{}, type:{}".format(name, var, type(var))
    if output:
        return out
    else:
        print(out)


def strip_extension(filename):
    arr = filename.split(".")
    if len(arr) == 1:
        return arr[0]
    return ".".join(arr[:-1])


def extension(filename):
    arr = filename.split(".")
    return arr[-1]


def tokenize(s):
    return list(filter(None, re.split("[,._ \-!?:\(\)|@/=]+", s)))


def dir_path(file):
    """
    Get the path to a dir where file is located.
    Use der_path(__file__) to get dir where source file is located.
    :param str file:
    :return:
    """
    return os.path.dirname(os.path.abspath(file))


def undefaultdict(d):
    return {k: v for k, v in d.items()}


VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


def generate_word(length):
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


class Timer:

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.duration = self.end - self.start
