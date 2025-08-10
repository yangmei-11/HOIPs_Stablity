import os
import re
from pymatgen.io.cif import CifParser, CifFile
from pymatgen.io.vasp.inputs import Poscar
from tqdm import tqdm
import pandas as pd

def read_comment(path):
    """读取cif里的额外信息。"""
    f = open(path)
    lins = f.readlines()
    f.close()
    ls = [re.findall(r"#.*$", i) for i in lins]
    ls = [re.sub("# ", "", i[0]) for i in ls if i]

    ls = [re.split(":", i) for i in ls if i]

    data = {}
    for k, v in ls:
        v = re.sub("^ *", "", v)
        try:
            v = float(v)
        except (TypeError, SyntaxError, NameError, ValueError):
            pass

        data.update({k: v})
    return data

def read_data(f,fmt="cif",note=True):
    """读取单个cif信息。"""
    if fmt =="cif":
        f = CifFile.from_file(f)
        cif = CifParser.from_string(f.orig_string)
        structure = cif.get_structures()[0] # 每个cif为单个结构
    elif fmt =="poscar":
        f = Poscar.from_file(f)
        structure = f.structure
    else:
        raise NotImplementedError

    if note:
        data = read_comment(pa)
    else:
        data = {}

    data["structure"] = structure.as_dict()
    name = structure.formula
    data["name"] = name
    return data


# 读取每个文件路径
path = r"."
path = os.path.join(path, "cif_merge")
files = os.listdir(path)

# 读取每个信息
datas = []
for k, i in tqdm(enumerate(files)):
    if ".py" in str(i):
        continue
    pa = os.path.join(path, i)
    data = read_data(pa, fmt="cif", note=True)
    datas.append(data)


datas = pd.DataFrame(datas)
datas.to_csv("kim_raw_data.csv")
