import json
import math
from django.db.models import Q
from django.shortcuts import render
from . import models
from django.views import View
from django.shortcuts import redirect
from carweb.models import Username,Carname,CarData,SaleData
from django.core.paginator import Paginator
from django.http.request import QueryDict

# Create your views here.

#起始页
class IndexView(View):
    def get(self,request):
        return render(request,'start.html')


#登录-跳转
def login1(request):
    return render(request,'login.html')


#登录-处理
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        #检查是否符合
        if username.strip() and password:
            user = Username.objects.get(user_name=username)
            try:
                pass
            except:
                message = '用户不存在！'
                return render(request, 'login.html', {'message': message})
            if user.user_password == password:
                print(username, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', {'message': message})
        else:
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')


#主页
def index(request):
    pass
    return render(request,'index.html')


#关于我们
def userroom(request):
    return render(request,'userroom.html')


#车型一览
def carshow(request,num=1):
    carnamelst=Carname.objects.all().order_by('id')
    num=int(num)
    #分页功能
    pager=Paginator(carnamelst,8)
    pagenum=pager.page(num)
    begin = (num - int(math.ceil(10.0 / 2)))
    if begin < 1:
        begin = 1
    end = begin + 9
    if end > pager.num_pages:
        end = pager.num_pages
    if end <= 10:
        begin = 1
    else:
        begin = end - 9
    pagelist = range(begin, end + 1)

    return render(request, 'carshow.html',{'carnamelst':pagenum,'pagelist':pagelist,'cnum':num})


#车辆详情
def cardetails(request,carid):
    #数据表的转换
    carid =int(carid)
    cars=Carname.objects.get(id=carid)
    carclass=cars.class_id
    carname=cars.car_name

    #最近四个月销量排行
    carsale=SaleData.objects.filter(class_id=carclass).order_by('-sale_date')[:4]

    #各项参数展示
    truecar=CarData.objects.filter(car_class=carclass)
    truetr=CarData.objects.filter(car_class=carclass).values('tr').order_by('tr').distinct()
    truetrty=CarData.objects.filter(car_class=carclass).values('gearbox_type').order_by('gearbox_type').distinct()
    truecomp = CarData.objects.filter(car_class=carclass).values('compartment').order_by('compartment').distinct()
    truedis = CarData.objects.filter(car_class=carclass).values('displacement').order_by('displacement').distinct()
    truenewenergy = CarData.objects.filter(car_class=carclass).values('newenergy').order_by('newenergy').distinct()
    truemvp = CarData.objects.filter(car_class=carclass).values('mvp').order_by('mvp').distinct()
    trueluxurious = CarData.objects.filter(car_class=carclass).values('luxurious').order_by('luxurious').distinct()
    truepower = CarData.objects.filter(car_class=carclass).values('power').order_by('power').distinct()
    truecylinder = CarData.objects.filter(car_class=carclass).values('cylinder').order_by('cylinder').distinct()
    trueengine = CarData.objects.filter(car_class=carclass).values('engine').order_by('engine').distinct()
    truecar_len = CarData.objects.filter(car_class=carclass).values('car_len').order_by('car_len').distinct()
    truecar_width = CarData.objects.filter(car_class=carclass).values('car_width').order_by('car_width').distinct()
    truetotal_quality = CarData.objects.filter(car_class=carclass).values('total_quality').order_by('total_quality').distinct()
    trueequipment_quality = CarData.objects.filter(car_class=carclass).values('equipment_quality').order_by('equipment_quality').distinct()
    truewheelbase = CarData.objects.filter(car_class=carclass).values('wheelbase').order_by('wheelbase').distinct()
    truefront_track = CarData.objects.filter(car_class=carclass).values('front_track').order_by('front_track').distinct()
    truerear_track = CarData.objects.filter(car_class=carclass).values('rear_track').order_by('rear_track').distinct()

    return render(request,'cardetails.html',{'carsale':carsale,'carname':carname,'truerear_track':truerear_track,'truefront_track':truefront_track,'truewheelbase':truewheelbase,'trueequipment_quality':trueequipment_quality,'truecar_width':truecar_width,'truecar_len':truecar_len,'trueengine':trueengine,'truecylinder':truecylinder,'truepower':truepower,'trueluxurious':trueluxurious,'truemvp':truemvp,'truenewenergy':truenewenergy,'truedis':truedis,'truetotal_quality':truetotal_quality,'truecar':truecar,'truetr':truetr,'truecomp':truecomp,'truetrty':truetrty})


#预测-跳转
def predict1(request):
    return render(request,'predict.html')


#预测-处理
def predict(request):
    """预测"""

    carclass = request.POST.get('carclass')
    ranliao = request.POST.get('ranliao')
    qudong = request.POST.get('qudong')
    jiage = request.POST.get('jiage')
    gaodu = request.POST.get('gaodu')
    zaike = request.POST.get('zaike')
    paifang = request.POST.get('paifang')
    zengya = request.POST.get('zengya')
    car = Carname.objects.get(class_id=carclass)
    if carclass and ranliao and qudong and jiage and gaodu and zaike and paifang and zengya:

        # 136-194行代码为金雪锋编写
        # !/usr/bin/env python3
        # -*- coding: utf-8 -*-
        # @Time   : 2021/1/9 16:54
        # @Author : Jin Xuefeng
        # @File   : predict.py
        import numpy as np
        from keras.models import load_model
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        from keras import backend as K
        K.clear_session()

        # 1. 输入特征
        date_pre = [201711]
        class_pre = int(carclass)    # 281301  # 车型
        fuel_pre = int(ranliao)      # 1  # 燃料类型1-4整数
        driven_pre = int(qudong)     # 1  # 驱动形式1-3整数
        combination_pre = [float(jiage), int(gaodu), int(zaike), int(paifang), int(zengya)]  # 价格、车高、额定载客、排放标准、是否增压

        # 2. 读取onehot编码字典、均值和标准差、模型信息
        f = open('carweb/data/onehot_dict.txt', 'r')
        onehot_dict = eval(f.read())
        date_dict = onehot_dict['date']
        class_dict = onehot_dict['classes']
        fuel_dict = onehot_dict['fuel']
        driven_dict = onehot_dict['driven']
        es = np.load('carweb/data/epsilon_sigma.npy')
        epsilon, sigma = es[0], es[1]
        model = load_model('carweb/data/model.h5')
        # print(model)

        # 3. 检查非法输入
        date_pre = np.array(date_pre)
        if class_pre not in class_dict.keys():
            raise ValueError('车型输入不合法')
        if fuel_pre not in fuel_dict.keys():
            raise ValueError('燃料类型输入不合法')
        if driven_pre not in driven_dict.keys():
            raise ValueError('驱动类型输入不合法')

        # 4. 对输入特征预处理
        # date_pre = date_dict.keys[-len-1:-1]     # 现在onehot编码截止201711
        date_pre = [date_dict[x] for x in date_pre-1]  # 列表解析，5*75   len(date_pre)
        # print(date_pre)
        num = len(date_pre)
        class_pre = class_dict[class_pre]
        class_pre = np.tile(class_pre, num).reshape(num, len(class_pre))
        fuel_pre = fuel_dict[fuel_pre]
        fuel_pre = np.tile(fuel_pre, num).reshape(num, len(fuel_pre))
        driven_pre = driven_dict[driven_pre]
        driven_pre = np.tile(driven_pre, num).reshape(num, len(driven_pre))
        combination_pre = (np.array(combination_pre) - epsilon) / sigma
        combination_pre = np.tile(combination_pre, num).reshape(num, len(combination_pre))

        # 5. 预测
        res = model.predict(x=[date_pre, class_pre, fuel_pre, driven_pre, combination_pre], verbose=0)
        res = np.expm1(res)  # 反平滑处理
        res = np.clip(res, 0, 2260 + 2000)  # 数据最大值为2260
        res = int(np.round(res))
        # res = res.reshape(1, )
        print('\n预测结果：', res)

        # carnum=int(zengya)+int(paifang)+int(carclass)+int(ranliao)+int(qudong)+int(jiage)+int(gaodu)+int(zaike)
        return render(request, 'predict.html', {'car':car,'carnum': res,'jiage1':jiage,'class1':carclass,'qudong1':qudong, 'ranliao1':ranliao,'gaodu1':gaodu,'zaike1':zaike,'paifang1':paifang,'zengya1':zengya})
    else:
        print('输入为空')
    return render(request,'predict.html')


#热门车型
def popularcar(request):

    #查找数据表里最近几月
    popdate= SaleData.objects.values('sale_date').order_by('-sale_date').first()
    popdate1=popdate.values()
    popdate2=list(popdate1)
    popdate3=popdate2[0]

    #排行前四的车辆
    popcar=SaleData.objects.filter(sale_date=popdate3).values('class_id').order_by('-sale_num')[:4]
    # print(popcar)
    #获取车型id具体数字
    car1id=popcar[0]['class_id']
    car2id = popcar[1]['class_id']
    car3id = popcar[2]['class_id']
    car4id = popcar[3]['class_id']


    #四辆推荐车型的具体信息
    car1info = Carname.objects.filter(class_id=car1id).first()
    car2info = Carname.objects.filter(class_id=car2id).first()
    car3info = Carname.objects.filter(class_id=car3id).first()
    car4info = Carname.objects.filter(class_id=car4id).first()
    #print(car1info)
    # print(' ')

    return render(request,'popularcar.html',{'car1info':car1info,'car2info':car2info,'car3info':car3info,'car4info':car4info})


#销量排行
def sale(request):
    saledate = '201201'

    if request.method == "POST":
        saledate = request.POST.get('saledate')

    datelst=SaleData.objects.all().values('sale_date').distinct()
    saleinfo=SaleData.objects.filter(sale_date=saledate).values('sale_num').order_by('-sale_num')[:8]
    saleclass=SaleData.objects.filter(sale_date=saledate).values('class_id').order_by('-sale_num')[:8]

    #转换成list
    #saleclass1 = list(SaleData.objects.filter(sale_date=saledate).values_list('class_id',flat=True))

    #获取排行榜汽车id
    salelst1 = []
    for sale in saleclass:
        salelst1.append(sale)
    salelst2 = []
    for item in salelst1:
        for key in item:
            salelst2.append(item[key])

    #读取排行榜汽车名字,地址
    namelst = []
    urllst = []
    for i in range(8):
        classid = Carname.objects.filter(class_id=salelst2[i]).values('car_name').first()
        classidv = classid.values()
        classidvv = list(classidv)[0]
        namelst.append(classidvv)
    for i in range(8):
        classid1 = Carname.objects.filter(class_id=salelst2[i])
        classidv1 = classid1.values()
        classidvv1 = list(classidv1)[0]
        urllst.append(classidvv1)

    return render(request,'sale.html',{'saleinfo':saleinfo,'datelst':datelst,'namelst':namelst,'urllst':urllst})

