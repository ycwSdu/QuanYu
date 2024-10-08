import torch
import torch.nn.functional as F
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.utils.data as Data
import numpy as np
import time

torch.manual_seed(1)  # reproducible


class cnn(nn.Module):
    def __init__(self, class_):
        super(cnn, self).__init__()

        self.conv1 = nn.Conv2d(1, 8, 3, 1, 1)
        self.max_pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(8, 16, 3, 1, 1)
        self.hidden1 = nn.Linear(16 * 1 * 150, 20 * 150)
        self.hidden2 = nn.Linear(20 * 150, 500)
        self.out = nn.Linear(500, class_)

    def forward(self, x):
        in_size = x.size(0)
        x = self.conv1(x)
        x = F.dropout(F.relu(x))
        x = self.max_pool1(x)
        x = self.conv2(x)
        x = F.dropout(F.relu(x))
        x = x.view(in_size, -1)
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))
        x = self.out(x)
        return x


def CNN(class_):
    model = cnn(class_)
    model.load_state_dict(torch.load('QuanYu/models/cnn_net_epoch_40.pkl'))
    return model


def query(model, data):
    # data = torch.Tensor(data)
    each = data.unsqueeze(0)
    with torch.no_grad():
        out = model(each)
    # out = net(each)
    prediction = torch.max(out, 1)[1].cpu()
    pred_y = prediction.data.numpy()
    return pred_y


def main():
    net = CNN(15)
    print(net)
    Xp = []
    print('data loading')
    for i in range(15):
        with open('D:/DATA/okdata/okdata/'+str(i) + '.csv') as f:
            data = f.readlines()
            for each in data[6000:]:
                each = each[:-1].split(',')
                x = [float(i) for i in each]
                x = torch.Tensor([x, x])
                Xp.append(np.array(torch.cat((x,), ).unsqueeze(dim=0)))

    Xp = torch.Tensor(Xp).type(torch.FloatTensor)
    ok = 0
    ll = len(Xp)
    print('successfully')
    a = time.time()
    for t, each in enumerate(Xp[:10]):
        print(query(net, each))



# main()

#main()

