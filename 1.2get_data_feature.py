import pandas as pd
from featurebox.featurizers.atom import mapper
from featurebox.featurizers.state.statistics import WeightedAverage
from pymatgen.core import Structure
features = {}
raw_data = pd.read_csv("kim_raw_data.csv")
raw_data.columns
raw_data.index
data = raw_data.values
structures = raw_data["structure"].values
structures = [Structure.from_dict(eval(i)) for i in structures]
# structure
f1 = {"density":[i.density for i in structures]}
f2 = {"volume":[i.volume for i in structures]}
f3 = {"ntypesp":[i.ntypesp for i in structures]}
f4 = {"space_group_number":[i.get_space_group_info()[1] for i in structures]}
#
# lattice
f5 = {"lattice_wigner_seitz":[i._lattice.get_wigner_seitz_cell() for i in structures]}
f6 = {"lattice_lengths":[i._lattice.lengths for i in structures]}
f7 = {"lattice_angles":[i._lattice.angles for i in structures]}
f8 = {"lattice_brillouion":[i._lattice.get_brillouin_zone() for i in structures]}

# composition_origin
f9 = {"com_weight":[si.composition.weight for si in structures]}
f10 = {"com":[si.composition.to_reduced_dict for si in structures]}
f11 = {"com_number":[si.composition.to_reduced_dict.values() for si in structures]}
f12 = {"com_average_electroneg":[si.composition.average_electroneg for si in structures]}
f13 = {"com_num_atoms":[si.composition.num_atoms for si in structures]}
f14 = {"com_total_electrons":[si.composition.total_electrons for si in structures]}

# atom
f15 = {"atom_a":[i.as_dataframe()["a"] for i in structures]}
f16 = {"atom_b":[i.as_dataframe()["b"] for i in structures]}
f17 = {"atom_c":[i.as_dataframe()["c"] for i in structures]}
f18 = {"atom_x":[i.as_dataframe()["x"] for i in structures]}
f19 = {"atom_y":[i.as_dataframe()["y"] for i in structures]}
f20 = {"atom_z":[i.as_dataframe()["z"] for i in structures]}
f21 = {"atom_Species":[i.as_dataframe()["Species"] for i in structures]}

d3 = {}
[d3.update(i) for i in [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,
                        f16,f17,f18,f19,f20,f21]]
d3 = pd.DataFrame(d3)

# composition_weight

func_map = ["atomic_radius","atomic_mass", "Z", "X", "number", "max_oxidation_state", "min_oxidation_state",
    "row", "group", "atomic_radius_calculated", "van_der_waals_radius", "mendeleev_no", "molar_volume",
    "boiling_point", "melting_point", "critical_temperature", "density_of_solid", "average_ionic_radius",
    "average_cationic_radius", "average_anionic_radius"]

appm = mapper.AtomPymatgenPropMap(prop_name=func_map)
wa = WeightedAverage(appm, n_jobs=6, return_type="df")
wa.set_feature_labels(func_map)
d1 = wa.fit_transform(f10["com"])

dd = pd.concat((d1, d3), axis=1)
dd.to_csv("data.csv") ## 41种特征

# # 第二部分，针对材料A，B，C位置分别展开。

# # Featurebox是一个开放的python库，集成了一套全面的材料信息学机器学习工具，旨在快速和轻松地生成、筛选、使用材料特征。


key = raw_data["Atom types"]
value = raw_data["Number of each atom"]

key0 = []
value0 = []
for i, j in zip(key, value):
    key0.append(i.split())
    value0.append(j.split())

d = [dict(zip(k, [int(i) for i in v])) for k, v in zip(key0, value0)]
A = []
B = []
X = []

for m in d:
    seq = list(m.items())
    A.append(dict(seq[:-2]))
    B.append(dict([seq[-2]]))
    X.append(dict([seq[-1]]))

# 原子/元素特征可以通过调取元素周期表数据获取

# A sites
from featurebox.featurizers.atom import mapper
from featurebox.featurizers.state.statistics import MaxPooling, WeightedAverage
appm = mapper.AtomTableMap(tablename="ele_table_norm.csv")
wa = MaxPooling(appm, n_jobs=6, return_type="df")
wa.set_feature_labels([f"max_A_{i}" for i in appm.feature_labels])
dA_max = wa.fit_transform(A)

# A sites
wa = WeightedAverage(appm, n_jobs=6, return_type="df")
wa.set_feature_labels([f"ave_A_{i}" for i in appm.feature_labels])
dA_ave = wa.fit_transform(A)

# B sites
from featurebox.featurizers.atom import mapper
from featurebox.featurizers.state.statistics import WeightedAverage
appm = mapper.AtomTableMap(tablename="ele_table_norm.csv")
wa = WeightedAverage(appm, n_jobs=6, return_type="df")
wa.set_feature_labels([f"single_B_{i}" for i in appm.feature_labels])
dB = wa.fit_transform(B)

# C sites
wa = WeightedAverage(appm, n_jobs=6, return_type="df")
wa.set_feature_labels([f"single_C_{i}" for i in appm.feature_labels])
dX = wa.fit_transform(X)

data2 = pd.concat([dA_ave, dA_max, dB, dX], axis=1)
# data2.to_csv("data2.csv")

d_all = pd.concat((dd, data2), axis=1)
d_all = pd.concat((d_all, raw_data), axis=1)


d_all.to_csv("data_all.csv") 288



