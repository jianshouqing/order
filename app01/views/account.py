from django.http import JsonResponse
from django.shortcuts import render,redirect
from app01.forms.account import LoginForm,SmsLoginForm,SendSmsForm
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html',{'form':form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {'form': form})

    data_dict = form.cleaned_data
    role = data_dict.pop('role')
    if role == '1':
        user_object = models.Administrator.objects.filter(**data_dict).filter(active=1).first()
    else:
        user_object = models.Customer.objects.filter(**data_dict).filter(active=1).first()

    if not user_object:
        form.add_error('username','用户名或密码错误')
        return render(request, 'login.html', {'form': form})

    mapping = {'1':'ADMIN','2':'CUSTOMER'}
    request.session[settings.NB_SESSION_KEY] = {
        'role': mapping[role],
        'id':user_object.id,
        'name':user_object.username,
    }
    return redirect(settings.HOME_URL)

def sms_login(request):
    if request.method == 'GET':
        form = SmsLoginForm()
        return render(request, 'sms_login.html', {'form': form})

    # 格式校验（手机号和验证码）
    # 判断验证码是否正确，通过手机号获取redis的验证码判断
    form = SmsLoginForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'status': False, 'msg': form.errors})

    # 在数据库读取用户信息+保存session
    role = form.cleaned_data['role']
    mobile = form.cleaned_data['mobile']
    if role == '1':
        user_object = models.Administrator.objects.filter(mobile=mobile).filter(active=1).first()
    else:
        user_object = models.Customer.objects.filter(mobile=mobile).filter(active=1).first()

    if not user_object:
        return JsonResponse({'status': False, 'msg': {'mobile':['手机号不存在']}})

    mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
    request.session[settings.NB_SESSION_KEY] = {
        'role': mapping[role],
        'id': user_object.id,
        'name': user_object.username,
    }
    return JsonResponse({'status': True, 'msg': 'ok','data':'/home'})


@csrf_exempt
def send_sms(request):
    # 校验手机号格式
    form = SendSmsForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({'status':False,'msg':form.errors})
    return JsonResponse({'status':True,'msg':'ok'})