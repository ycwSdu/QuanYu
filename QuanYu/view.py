from django.http import HttpResponse
import os
import time
from django.shortcuts import render

from . import solve

adminLoginStatus = False
userData = []
resultDataGlobal = None
nowUser = None


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def loadUserNow(userId):
    user = {'name': '', 'age': '', 'sex': '', 'id': '', 'tel': '', 'addr': '', 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
    with open('QuanYu/datas/userall.data', encoding='utf-8') as f:
        data = f.readlines()
    for each in data:
        each = each[:-1].split(',')
        if each[3] == userId:
            # 郑新园, 19, 女, 370481200102213841, 19106412646, 山东省滕州市
            user['name'] = each[0]
            user['age'] = each[1]
            user['sex'] = each[2]
            user['id'] = each[3]
            user['tel'] = each[4]
            user['addr'] = each[5]
            break
    return user


def userIllSave(userId, inData):
    userId = 'id' + userId + '.data'
    path = 'QuanYu/datas/user_ill/'
    allFiles = os.listdir(path)
    if userId in allFiles:
        with open(path + userId, 'r', encoding='gbk') as f:
            data = f.readline()
            data = eval(data)
            # print(data.keys())
            data['ill'].append(inData)
        with open(path + userId, 'w', encoding='gbk') as f:
            f.write(str(data))


def xinDianSolve(request):
    global resultDataGlobal, nowUser
    if request.method == "POST":
        userId = request.POST['beiZhu']
        # print(userId)
        myFile1 = request.FILES.get("inputFile1", None)
        if not myFile1:
            return HttpResponse("no files")
        myFile2 = request.FILES.get("inputFile2", None)
        if not myFile2:
            return HttpResponse("files not enough")
        file = open('upLoadData/'+myFile1.name, 'wb+')
        for chunk in myFile1.chunks():
            file.write(chunk)
        file = open('upLoadData/'+myFile2.name, 'wb+')
        for chunk in myFile2.chunks():
            file.write(chunk)
        file.close()
        #resultData = solve.solve(myFile1.name)
        nowUser = loadUserNow(userId)
        resultData = solve.solve(myFile1.name, nowUser)
        resultDataGlobal = resultData
        userIllSave(userId, resultDataGlobal['report'])
        return render(request, 'test.html', resultData)
    else:
        return HttpResponse("not get ")


def show(request):
    return render(request, 'submit.html')
    # return HttpResponse("Hello")


def runoob(request):
    context = {}
    a = int(input("输入草莓的数量："))
    context['caomei_val'] = a

    return render(request, 'runoob.html', context)


def hello(request):
    return HttpResponse("Hello")


def loadUser():
    global userData
    userData = []
    with open(r'QuanYu/datas/userall.data', encoding='utf-8') as f:
        data = f.readlines()
    for each in data:
        # 刘凯,21,男,370911199900008888,19861403695,山东省济南市长清大学城
        each = each[:-1].split(',')
        print(each)
        if len(each) < 6:
            break
        userData.append({'name': each[0], 'age': each[1], 'sex': each[2], 'id': each[3], 'tel': each[4], 'addr': each[5]})


def upload(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files")
        file = open(myFile.name, 'wb+')
        for chunk in myFile.chunks():
            file.write(chunk)
        file.close()
        return HttpResponse("upload over")
    else:
        return HttpResponse("not get ")


def adminLogin(request):
    global adminLoginStatus, userData
    if adminLoginStatus is True:
        return render(request, 'admin2.html')
    else:
        if request.method == "POST":
            userId = request.POST['userId']
            userPw = request.POST['passWd']
            if userId == 'admin' and userPw == 'admin':
                adminLoginStatus = True
                loadUser()
                data = {'users': userData}
                print(data)
                return render(request, 'admin2.html', data)
            else:
                return HttpResponse("Login Error")
        else:
            return HttpResponse("Login Error")


def login(request):
    global adminLoginStatus, userData
    if adminLoginStatus is True:
        loadUser()
        data = {'users': userData}
        print(data)
        return render(request, 'admin2.html', data)
    else:
        return render(request, 'login.html')


def adminQuit(request):
    global adminLoginStatus
    adminLoginStatus = False
    return render(request, 'index.html')


def userRegister(request):
    with open('QuanYu/datas/userall.data', 'a', encoding='utf-8') as f:
        # 刘凯,21,男,370911199900008888,19861403695,山东省济南市长清大学城
        # print("用户：",request.POST['name']+','+request.POST['age']+','+request.POST['sex']+','+request.POST['id']+request.POST['tel']+','+request.POST['addr'])
        f.write(request.POST['name']+','+request.POST['age']+','+request.POST['sex']+','+request.POST['id']+','+request.POST['tel']+','+request.POST['addr']+'\n')
    data = {'id': request.POST['id'], 'ill': []}
    with open('QuanYu/datas/user_ill/'+'id'+request.POST['id']+'.data', 'w') as f:
        f.write(str(data))
    return render(request, 'index.html')


def details(request):
    global resultDataGlobal, nowUser

    # resultDataGlobal['userdata'] = nowUser
    return render(request, 'detiles.html', resultDataGlobal)


def showUserData(request):
    id = 'id'+request.GET['id']+'.data'
    path = 'QuanYu/datas/user_ill/'
    with open(path+id, 'r', encoding='gbk') as f:
        data = eval(f.readline())
    return render(request, 'showUserData.html', data)


def delUserData(request):
    id = request.GET['id']
    idData = 'id'+ id +'.data'
    os.remove('QuanYu/datas/user_ill/'+idData)
    with open('QuanYu/datas/userall.data', encoding='utf-8') as f:
        data = f.readlines()
    with open('QuanYu/datas/userall.data', 'w', encoding='utf-8') as f:
        for each in data:
            a = each.split(',')
            if a[3] == id:
                continue
            else:
                f.write(each)
    return render(request, 'admin2.html')
