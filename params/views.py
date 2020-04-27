from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from batteryserver.settings import MEDIA_ROOT

from .models import ExcelFile, InputParams
from django.db import models

from .dataproc import procData, procBtn, btnList, currentParamSetModel, last_bat, except_bat, polor_dict, last_alt_dict, l_last_dict, kap_alt_dict, procPWMOutput

import os
import time


# Create your views here.


current_model = 'modelA'
current_excel = ''



# User.objects.get(user_name=user_name); get查询结果转换为JSON
def model2json(data):
    data.__dict__.pop("_state")
    rData = data.__dict__
    return rData

# User.objects.filter(pwd=pwd); filter结果集转换为JSON
def model2jsonArr(data):
    rData = []
    for p in data:
        p.__dict__.pop("_state") # 需要除去，否则不能json化
        rData.append(p.__dict__) # 注意，实际是个json拼接的过程，不能直接添加对象
    return rData


def mainPage(request):

    global currentParamSetModel
    if request.POST.get('model'):
        currentParamSetModel = request.POST['model']
        print(currentParamSetModel)
        obj = InputParams.objects.filter(model_type=currentParamSetModel)
        obj_params = model2jsonArr(obj)[0]
        return JsonResponse(obj_params)

    elif request.POST.get('max_bat') and request.POST.get('cur_bat') and request.POST.get('charge_bat') and request.POST.get('run_bat'):
        max_b = request.POST.get('max_bat')
        cur_b = request.POST.get('cur_bat')
        charge_b = request.POST.get('charge_bat')
        run_b = request.POST.get('run_bat')
        a_l = request.POST.get('a_laden')
        e_l = request.POST.get('e_laden')
        a_e = request.POST.get('a_entladen')
        e_e = request.POST.get('e_entladen')
        p_p = request.POST.get('percent_power')
        net = request.POST.get('netzentlastang')

        print(request.POST)

        InputParams.objects.filter(model_type=currentParamSetModel).update(max_bat = max_b, cur_bat = cur_b, charge_bat = charge_b, run_bat = run_b, a_laden=a_l, e_laden=e_l, a_entladen = a_e, e_entladen = e_e, percent_power = p_p, netzentlastang = net)

        print(InputParams(model_type = current_model))
        return HttpResponse('Param Save OK')


    # 检查表是不是存在，不存在就创建
    modelList = ["modelA", "modelB", "modelC", "modelD", "modelE", "modelF"]
    for model in modelList:
        obj = InputParams.objects.filter(model_type = model)
        if len(obj) == 0:
            obj = InputParams(model_type = model, max_bat = 0.0, cur_bat = 0.0, charge_bat = 0.0, run_bat = 0.0, a_laden = '00:00', e_laden = '00:00', a_entladen = '00:00', e_entladen = '00:00', percent_power = 100, netzentlastang = 100)
            obj.save()

    obj = InputParams.objects.filter(model_type = currentParamSetModel)
    obj_params = {"obj_params": obj[0]}
    print(obj_params['obj_params'].model_type)
    return render(request, 'main.html', obj_params)


def chartPage(request):

    global current_excel
    global current_model
    global btnList
    global last_bat
    global except_bat
    global polor_dict
    global kap_alt_dict
    global last_alt_dict
    global l_last_dict

    excels = ExcelFile.objects

    if(request.method == 'GET'):
    
        if request.GET.get('func') != None:

            jsonRes = list()
            print(request.GET['func'])

            if request.GET['func'] == 'selectExcelClick':
                if request.GET.get('excelfilename') != None:
                    current_excel = request.GET['excelfilename']
                    jsonRes = procData(current_model, current_excel, current_model)


            if request.GET['func'] == 'modelChanged':
                if request.GET.get('model') != None:
                    current_model = request.GET['model']
                    jsonRes = procData(current_model, current_excel, current_model)

            if request.GET['func'] == 'buttonClick':
                if request.GET.get('btn') != None:
                    btn = request.GET['btn']
                    print(btn)
                    jsonRes = procBtn(btn)

            if request.GET['func'] == 'selectTime':
                if request.GET.get('time') != None:
                    time = request.GET['time']
                    print(time)
                    jsonRes = {'last_battery': last_bat[time], 'except_battery': except_bat[time]}

                
                # print('last_alt:', last_alt_dict[time])
                # print('kap_alt:', kap_alt_dict[time])
                # print('polor:', polor_dict[time])
                # print('l_last:', l_last_dict[time])

                currentParamSetModel = current_model
                procPWMOutput(current_model, time)

                # if last_alt_dict[time] > 0 and kap_alt_dict[time] > 0:
                #     # 此处接通电池给用电器
                #     print('此处接通电池给用电器')
                #     # runCh1()

                #     pass

                # if polor_dict[time] < l_last_dict[time] + last_alt_dict[time]:
                #     # 此处将太阳能通电给电池
                #     print('此处将太阳能通电给电池')
                #     # runCh2()
                #     pass

                # # if polor_dict[time] > l_last_dict[time] + last_alt_dict[time]:
                # #     # 多出的电给电网
                # #     print('多出的电给电网')
                # #     pass

                # if polor_dict[time] > l_last_dict[time] + last_alt_dict[time]:
                #     # 此时太阳能接入电网
                #     print('多出的电给电网')
                #     # runCh3()
                #     pass

            return JsonResponse({'data_array': jsonRes})


    excel_list = {"excels": excels, 'btnList': btnList}
    # if(len(excels.values('filename')) != 0):
    #     current_excel = (excels.values('filename')[0]['filename'])

    return render(request, 'chart.html', excel_list)


def uploadExcel(request):

    if(request.method == 'POST'):
        myFile = request.FILES.get('myfile', None)
        if not myFile:
            return HttpResponse("no file for upload")

        # 检查表格是否已存在，如果存在则禁止
        excels = ExcelFile.objects.filter(filename = myFile.name)
        if(len(excels) != 0):
            return HttpResponse("excel already exist!")

        excelf = open(os.path.join(MEDIA_ROOT + '/excels/'+myFile.name), 'wb+')

        print('file name: ' + myFile.name)
        for chunk in myFile.chunks():
            print('save new chunck')
            excelf.write(chunk)

        excelf.close()

        excelmodel = ExcelFile(filename=myFile.name,
                               excelfile='excels/'+myFile.name)
        excelmodel.save()
    return HttpResponse("ok")
