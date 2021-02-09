from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from .models import Employee,SRV,SIV,Items
from datetime import datetime

import json

def getDate(datestr):
    datestr = datestr.split('T')[0]
    d1 = datetime.strptime(datestr,'%Y-%m-%d')
    return d1

def index(request):
    return render(request, 'index.html')


def createEmployee(emp_data):
    emp = Employee(
        emp_no = emp_data["emp_no"],
        name = emp_data["name"],
        designation = emp_data["designation"],
        department = emp_data["department"]
    )
    emp.save()
    return emp

def addEmployee(request):
    #implement try catch
    emp_data = json.loads(request.body.decode('utf-8'))
    emp = Employee(
        emp_no = emp_data["emp_no"],
        name = emp_data["name"],
        designation = emp_data["designation"],
        department = emp_data["department"]
    )
    emp.save()
    return JsonResponse({'result':'success'})

def getEmployees(request):
    emp_data = list(Employee.objects.values())
    return JsonResponse(emp_data, safe=False)

def createSIV(request):
    siv_data = json.loads(request.body.decode('utf-8'))
    srv = SRV.objects.filter(id = siv_data["srv_id"])[0]
    siv = SIV(
        issued_reason = siv_data["issued_reason"],
        issued_to = createEmployee(siv_data["issued_to"]),
        srv_id = srv
    )
    siv.save()
    return HttpResponse("Hello, world. You're at the polls index.")

def createSRV(request):
    srv_data = json.loads(request.body.decode('utf-8'))
    srv = SRV(
        mode_of_receipt = srv_data["mode_of_receipt"],
        name_supplier = srv_data["name_supplier"],
        indent_ref_no = srv_data["indent_ref_no"],
        indent_date = getDate(srv_data["indent_date"]),
        inspected_by = createEmployee(srv_data["inspected_by"]),
        inspected_countersigned_by = createEmployee(srv_data["inspected_countersigned_by"]),
        received_by = createEmployee(srv_data["received_by"]),
        received_countersigned_by = createEmployee(srv_data["received_countersigned_by"])
    )
    srv.save()
    for item_data in srv_data["items"]:
        item = Items(
            description = item_data["description"],
            received_qty = item_data["received_qty"],
            rejected_qty = item_data["rejected_qty"],
            unit_rate = item_data["unit_rate"],
            srv_id = srv
        )
        item.save()
    return JsonResponse({'result':'success'})

def createsrvsiv(request):
    try:
        srvsiv_data = json.loads(request.body.decode('utf-8'))
        srv = addSRV(srvsiv_data["srvdetails"])
        siv = addSIV(srvsiv_data["sivdetails"],srv)
        return JsonResponse({'id':srv.id,'result':'success'})
    except Exception as ex:
        return JsonResponse({'result':'success'})

def addSIV(siv_data,srv):
    #srv = SRV.objects.filter(id = siv_data["srv_id"])[0]
    siv = SIV(
        issued_reason = siv_data["issued_reason"],
        issued_to = Employee.objects.filter(id = siv_data["issued_to"]["id"])[0],
        srv_id = srv
    )
    siv.save()
    return siv

def addSRV(srv_data):
    srv = SRV(
        mode_of_receipt = srv_data["mode_of_receipt"],
        name_supplier = srv_data["name_supplier"],
        indent_ref_no = srv_data["indent_ref_no"],
        indent_department = srv_data["indent_department"],
        remarks = srv_data["remarks"],
        indent_date = getDate(srv_data["indent_date"]),
        srvsiv_date = getDate(srv_data["srvsiv_date"]),
        inspected_by = Employee.objects.filter(id = srv_data["inspected_by"]["id"])[0],
        inspected_countersigned_by = Employee.objects.filter(id = srv_data["inspected_countersigned_by"]["id"])[0],
        received_by = Employee.objects.filter(id = srv_data["received_by"]["id"])[0],
        received_countersigned_by = Employee.objects.filter(id = srv_data["received_countersigned_by"]["id"])[0]
    )
    srv.save()
    for item_data in srv_data["items"]:
        item = Items(
            description = item_data["description"],
            received_qty = item_data["received_qty"],
            rejected_qty = item_data["rejected_qty"],
            unit_rate = item_data["unit_rate"],
            srv_id = srv
        )
        item.save()
    return srv

def getSRVID(srv_id):
    srv_data = list(SRV.objects.filter(id=srv_id).values())
    srv_data = srv_data[0]
    srv_data["inspected_by"] = getEmployee(srv_data["inspected_by_id"])
    srv_data["inspected_countersigned_by"] = getEmployee(srv_data["inspected_by_id"])
    srv_data["received_by"] = getEmployee(srv_data["inspected_by_id"])
    srv_data["received_countersigned_by"] = getEmployee(srv_data["inspected_by_id"])
    srv_data['items'] = getItems(srv_data['id'])
    return JsonResponse(srv_data, safe=False)




def getsrvs(request):
    #Need to redesign as data becomes more
    srv_data = list(SRV.objects.select_related().values())
    srvsiv_data = []
    for srv in srv_data:
        srvsiv = {
            'srvdetails': '',
            'sivdetails': '',
            'srvid': ''
        }
        srv["inspected_by"] = getEmployee(srv["inspected_by_id"])
        srv["inspected_countersigned_by"] = getEmployee(srv["inspected_countersigned_by_id"])
        srv["received_by"] = getEmployee(srv["received_by_id"])
        srv["received_countersigned_by"] = getEmployee(srv["received_countersigned_by_id"])
        srv['items'] = getItems(srv['id'])
        srvsiv['srvdetails'] = srv
        srvsiv['sivdetails'] = getSIV(srv['id'])
        srvsiv['sivdetails']['issued_to'] = getEmployee(srvsiv['sivdetails']['issued_to_id'])
        srvsiv['srvid'] = srv['id']
        srvsiv_data.append(srvsiv)
    return JsonResponse(srvsiv_data, safe=False)

def getEmployee(emp_id):
    emp = Employee.objects.filter(id = emp_id)
    emp = list(emp.values())
    return emp[0]

def getItems(item_srv_id):
    items = Items.objects.filter(srv_id=item_srv_id)
    items = list(items.values())
    return items

def getSIV(srv_id):
    siv = SIV.objects.filter(srv_id=srv_id)
    siv = list(siv.values())
    return siv[0]
# Create your views here.
