from pyxtal import pyxtal
from pyxtal.XRD import Similarity
import chemparse
import re
import numpy as np
import spglib

def find_formula(path = "./BaTiO3_mp-5777_computed.vasp"):
    box = []
    with open(path, "r") as f:
        file = f.readlines()
        box.append(file)
    symbol = box[0][5].strip().split()
    number = box[0][6].strip().split()
    formula = str()
    for i in range(len(symbol)):
        #print(i)
        #print(symbol[i],number[i])
        formula = formula+symbol[i]+number[i]

    return formula

def find_sym(path="./POSCAR"):

    symbol_map = {"H":1,"He":2,    "Li":3,    "Be":4,    "B":5,    "C":6,    "N":7,    "O":8,    "F":9,    "Ne":10,    "Na":11,    "Mg":12,    "Al":13,    "Si":14,
        "P":15,    "S":16,    "Cl":17,    "Ar":18,    "K":19,    "Ca":20,    "Sc":21,    "Ti":22,    "V":23,    "Cr":24,    "Mn":25,    "Fe":26,    "Co":27,    "Ni":28,    "Cu":29,    "Zn":30,
        "Ga":31,    "Ge":32,    "As":33,    "Se":34,    "Br":35,    "Kr":36,    "Rb":37,    "Sr":38,    "Y":39,    "Zr":40,    "Nb":41,    "Mo":42,    "Tc":43,    "Ru":44,    "Rh":45,    "Pd":46,
        "Ag":47,    "Cd":48,    "In":49,    "Sn":50,    "Sb":51,    "Te":52,    "I":53,    "Xe":54,    "Cs":55,    "Ba":56,    "La":57,    "Ce":58,    "Pr":59,    "Nd":60,    "Pm":61,    "Sm":62,
        "Eu":63,    "Gd":64,    "Tb":65,    "Dy":66,    "Ho":67,    "Er":68,    "Tm":69,    "Yb":70,    "Lu":71,    "Hf":72,    "Ta":73,    "W":74,    "Re":75,    "Os":76,    "Ir":77,    "Pt":78,
        "Au":79,    "Hg":80,    "Tl":81,    "Pb":82,    "Bi":83,    "Po":84,    "At":85,    "Rn":86,    "Fr":87,    "Ra":88,    "Ac":89,    "Th":90,    "Pa":91,    "U":92,    "Np":93,    "Pu":94,
        "Am":95,    "Cm":96,    "Bk":97,    "Cf":98,    "Es":99,    "Fm":100,    "Md":101,    "No":102,    "Lr":103,    "Rf":104,    "Db":105,    "Sg":106,
        "Bh":107,    "Hs":108,    "Mt":109,    "Ds":110, "Rg":111,"Cn":112, "Uut":113,"Uuq":114,"Uup":115,"Uuh":116,"Uus":117,"Uuo":118,}

    for st in [path]:
        try:
            with open(st, "r") as f:
                file = f.readlines()
        except FileNotFoundError:
            #print("Not find %s"%st)
            continue    

        lists = []
        for a in [2, 3, 4]:
            row = []
            for b in file[a].split():
                row.append(float(b))
            lists.append(row)
        lattice = np.array(lists) * float(file[1])

        num = 0
        numbers = []
        atmtyp = file[5].strip().split()
        elenu = file[6].split()
        numbers = []
        for ine,a in enumerate(elenu):
            for i in range(int(a)):
                numbers.append(symbol_map.get(atmtyp[ine]))
            num = num+int(a)
            #numbers.append(int(a)) 

        positions = []
        for a in range(8,8+num):
            row = []
            for b in file[a].split():
                row.append(float(b))
            positions.append(row)

        cell = (lattice, positions, numbers)

        #magmoms = [m_1, m_2, ...]
        #cell = (lattice, positions, numbers, magmoms)

        spgobj = spglib.get_symmetry_dataset(cell, symprec=1e-5, hall_number=0)
        #print(st)
        #print(spgobj.get("international"))
        #print(spglib.get_spacegroup_type(spgobj.get("hall_number")).get("schoenflies") + "\n")


    
    return spgobj.get("international")


def find_xrd(path1="BaTiO3_mp-5777_computed.cif",path2="BaTiO3_mp-5986_computed.cif"):
    xtal1 = pyxtal()
    xtal2 = pyxtal()
    #xtal1.from_seed("POSCAR"+".vasp")
    xtal1.from_seed("BaTiO3_mp-5777_computed.cif")
    xrd1 = xtal1.get_XRD(thetas=[0, 180])
    p1 = xrd1.get_profile()
    #xtal2.from_seed("POSCAR2"+".vasp")
    xtal2.from_seed("BaTiO3_mp-5986_computed.cif")
    xrd2 = xtal2.get_XRD(thetas=[0, 180])
    p2 = xrd2.get_profile()
    s= Similarity(p1, p2, x_range=[0,180])
    #s.show()
    s = str(Similarity(p1, p2, x_range=[0,60]))
    kk = re.compile(r'is(.*)')
    res = kk.findall(s)
    res = np.array(res,dtype="float")
    res = float(res)
    return res

def go_rd(path1="./BaTiO3_mp-5777_computed.vasp",path2="./BaTiO3_mp-5986_computed.vasp"):
    """
    flag 来表征是不是一样的，初始值为0
    如果falg输出0表示不是一样的，输出1表示结构无差异
    """
    flag = 0
    chem_df1 =chemparse.parse_formula(find_formula(path=path1))
    chem_df2 =chemparse.parse_formula(find_formula(path=path2))
    if chem_df1 == chem_df2:
        flag = 1
        if find_sym(path=path1) == find_sym(path=path2):
            flag = 1
            if find_xrd(path1=path1,path2=path2)>0.95:
                flag = 1
            else:
                flag = 0
        else:
            flag = 0
    else:
        flag = 0
    return flag
