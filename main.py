import numpy as np
import math
from Configuration import Mechanism
from Analysis import State


# mechanism configuration input
lab = float(input("输入LAB"))
lbc = float(input("输入LBC"))
lcd = float(input("输入LCD"))
lde = lhm = lan = float(input("输入LDE=LHM=LAN"))
lef = float(input("输入LEF"))
ldg = lek = float(input("输入LDG=LEK"))
lag = lnk = float(input("输入LAG=LNK"))
lah = lnm = float(input("输入LAH=LNM"))
beta1 = beta2 = float(input("输入角度HAG和MNK（角度制）"))
beta3 = float(input("输入EF与水平夹角（角度制）"))

# trajectory formula input
print("轨迹方程选项，角度从小到大填")
print("1. 3-4-5")
print("2. 4-5-6-7")
interval_lst = []
formula_lst = []
h_lst = []
beta_lst = []
j = 0
while j != 360:
    i = float(input("输入左区间"))
    j = float(input("输入右区间"))
    if i > j:
        print("错误区间")
        continue
    formula = int(input("选择轨迹方程"))
    h = float(input("输入参数h"))
    beta = float(input("输入参数beta1"))
    h_lst.append(h)
    beta_lst.append(beta)
    interval_lst.append((i, j))
    formula_lst.append(formula)


# acquire the list of enpoints tuple
def get_endpoints(interval_lst, formula_lst, h_lst, beta_lst):
    endpoint_lst = []
    for index in range(0, len(interval_lst)):
        for theta in [round(num,1) for num in np.arange(interval_lst[index][0], interval_lst[index][1] + 0.5, 0.5)]:
            if formula_lst[index] == 1:
                s = h_lst[index] * (10 * pow(theta/beta_lst[index], 3) - 15 * pow(theta/beta_lst[index], 4) + 6 * pow(theta/beta_lst[index], 5))
            else:
                s = h_lst[index] * (35 * pow(theta/beta_lst[index], 4) - 84 * pow(theta/beta_lst[index], 5) + 70 * pow(theta/beta_lst[index], 6) - 20 * pow(theta/beta_lst[index], 7))
            endpoint_lst.append((s * math.cos(theta), s * math.sin(theta)))
    return endpoint_lst

# prepare for analysis
mech = Mechanism(lab, lbc, lcd, lde, lhm, lan, lef, ldg, lek, lag, lnk, lah, lnm, beta1, beta2, beta3)
endpoints = get_endpoints(interval_lst, formula_lst, h_lst, beta_lst)

state_lst = []
for endpoint in endpoints:
    state = State(mech, endpoint[0], endpoint[1])
