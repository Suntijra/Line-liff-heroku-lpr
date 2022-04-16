from tabnanny import check
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
import pymongo

myclient = pymongo.MongoClient("mongodb://santi:Santi!12321@157.245.59.56:27018/?authSource=admin&readPreference=primary&directConnection=true&ssl=false")
def check_register(lineID):
    query={
        'Line_Users_ID': lineID
    }
    mycol = myclient['LPR']['register']
    if mycol.find_one(query)==None:
        return True
    else:
        print(mycol.find_one(query))
        print('Line_User_Id : ซำ้าๆๆๆๆๆ')
        return False
def insert_data(lineID,name,license_plate,tel,email):
    mydb = myclient["LPR"]
    mycol = mydb["register"]
    mydict = { 
        "Line_Users_ID": lineID,
        'name': name,
        'license_plate': license_plate,
        'tel': tel,
        'Email':email
    }
    mycol.insert_one(mydict)

def index(request):
    if request.is_ajax():
        print('เป็น Ajax')
        if 'lineID' in request.GET and bool(request.GET['license_plate']) == True and bool(request.GET['name']) == True and bool(request.GET['email'])== True and bool(request.GET['tel'])== True:
            lineID = request.GET['lineID']
            name = request.GET['name']
            license_plate = request.GET['license_plate']
            tel = request.GET['tel']
            email = request.GET['email']
            print('Line user id :', lineID)
            if check_register(lineID):
                insert_data(lineID,name,license_plate,tel,email)
                return JsonResponse({'Status':check_register(lineID)})
            else:
                print('check line id : ',check_register(lineID))
                return JsonResponse({'Status':check_register(lineID)})    
        else:
            return JsonResponse({'Status':'กรุณาเติมข้อความให้ครบทุกช่อง'})
    else:
        print('ไม่ใช่ Ajax')
    return render(request,'index.html',)


from .form import searchForm

def search(request):
    if request.is_ajax():
        print('เป็น ajax')
        if 'search' in request.GET:
            print('มี request search')
            search =request.GET['search']
            print(search)
            return JsonResponse({'search:':search})
        else:
            print('ไม่เป็น ajax')
    form = searchForm(request.GET)
    vars = {
        'form': form
    }
    return render(request,'test.html',vars)


