from .solve2 import CNN
from .solve2 import load_MIT_Data
import torch
import numpy as np

from .solve2 import ReportSet


def dataToTensor(data):
    Xp = []
    for x in data:
        x = torch.Tensor([x, x])
        Xp.append(np.array(torch.cat((x,), ).unsqueeze(dim=0)))
    Xp = torch.Tensor(Xp).type(torch.FloatTensor)
    return Xp


def solve(fileName, user):
    # print(user)
    fileName = fileName[:-4]
    data, data1, data2, R_location, sc, daolian = load_MIT_Data.load(fileName)
    dataX1 = []
    dataX2 = []
    for each in data:
        for i in each:
            dataX1.append(i)
    for each in data2:
        for i in each:
            dataX2.append(i - 1)
    cnn = CNN.CNN(15)
    data3 = data
    data = dataToTensor(data)
    Lab = ["正常波动", "左束支传导阻滞", "右束支传导阻滞", "异常房性早搏",
           "室性早搏", "心室融合心跳", "交界性早搏", "房性早搏", "交界性逸搏",
           "起搏心跳", "孤立的类QRS伪迹", "注释", "频率变化", "动脉血压阻塞", "起搏融合心跳"]
    illDict = {}
    all_ill = []
    x_len = 0
    for i, each in enumerate(data):
        a = Lab[CNN.query(cnn, each)]
        if illDict.get(a) is None:
            illDict[a] = 1
        else:
            illDict[a] += 1
        d1, d2 = [], []
        if a != '正常波动':
            for j in range(max(0, i-4), min(len(data), i+5)):
                for k in data3[j]:
                    d1.append(k)
                for k2 in data2[j]:
                    d2.append(k2-1)
            if x_len == 0:
                x_len = len(d1)
            all_ill.append({'name': a, 'data1': d1, 'data2': d2, })
            # print('长度：', len(d1), len(d2))

    ###
    a = 0
    illsc = []
    for each in illDict.keys():
        illsc.append([each, illDict[each]])
        a += illDict[each]
    sc.append(a / len(R_location))
    illdict = ReportSet.createSc(illsc, sc, daolian, ["admin", "admin"], [user['name'], user['id'], user['sex'], user['age']])
    repo = ReportSet.createReport(illdict)
    ###
    print('最新的：', repo)
    ill_names = []
    ill_nums = []
    result = {}
    for each in illDict:
        if each == '正常波动':
            continue
        ill_names.append(each)
        ill_nums.append(illDict[each])

    result['total'] = len(data)
    result['zc_num'] = illDict['正常波动']
    result['yc_num'] = result['total'] - result['zc_num']
    result['ill_names'] = ill_names
    result['ill_nums'] = ill_nums
    result['all_ill'] = all_ill
    result['report'] = {'user': user, 'data': repo}
    illDict.pop('正常波动')
    result['ill_dict'] = illDict
    result['x_r'] = [i for i in range(x_len)]
    return result
