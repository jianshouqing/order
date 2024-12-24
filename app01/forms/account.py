from django import forms
from app01.utils.encrypt import md5_string
from django.core.validators import RegexValidator
from django_redis import get_redis_connection
from django.core.exceptions import ValidationError
from app01 import models
import random
from app01.utils.hl_sms import send_sms
from app01.utils.bootstrap import BootStrapForm


class LoginForm(BootStrapForm,forms.Form):
    exclude_field_list = []
    role = forms.ChoiceField(
        label = '角色',
        required = True,
        choices=(('2','客户'),('1','管理员')),
        widget = forms.Select,
    )
    username = forms.CharField(
        label = '用户名',
        required = True,
        widget= forms.TextInput,
    )
    password = forms.CharField(
        label = '密码',
        required = True,
        widget = forms.PasswordInput(render_value=True),
    )

    def clean_password(self):
        old = self.cleaned_data['password']
        return md5_string(old)


class SmsLoginForm(BootStrapForm,forms.Form):
    exclude_field_list = []
    role = forms.ChoiceField(
        label = '角色',
        required = True,
        choices=(('2','客户'),('1','管理员')),
        widget = forms.Select,
    )

    mobile = forms.CharField(
        label = '手机号',
        required = True,
    )
    code = forms.CharField(
        label = '验证码',
        validators=[RegexValidator(r'^[0-9]{4}$', '验证码格式错误'), ],
    )

    def clean_code(self):
        mobile = self.cleaned_data['mobile']
        code = self.cleaned_data['code']
        conn = get_redis_connection('default')
        cache_code = conn.get(mobile)
        if not cache_code:
            raise ValidationError('未发送或已失效')
        if code !=cache_code.decode('utf-8'):
            raise ValidationError('验证码错误')
        # 验证码校验成功后，删除redis中的验证码，防止验证码多次使用
        conn.delete(mobile)
        return code


class SendSmsForm(forms.Form):
    role = forms.ChoiceField(
        label='角色',
        required=True,
        choices=(('2', '客户'), ('1', '管理员')),
    )
    mobile = forms.CharField(
        label = '手机号',
        widget=forms.TextInput,
        validators= [RegexValidator(r'^1[3588]\d{9}$','手机格式错误'),],
        required=True
    )

    def clean_mobile(self):
        old = self.cleaned_data['mobile']
        role = self.cleaned_data['role']
        if role == '1':
            exists = models.Administrator.objects.filter(mobile=old).filter(active=1).exists()
        else:
            exists = models.Customer.objects.filter(mobile=old).filter(active=1).exists()

        if not exists:
            raise ValidationError('手机号不存在')

        # 生成随机验证码+发送短信
        sms_code = str(random.randint(1000,9999))
        print(sms_code)
        is_ok = send_sms(old,sms_code)
        if not is_ok:
            raise ValidationError('短信发送失败')

        # 短信验证码写入redis+超时时间
        conn = get_redis_connection('default')
        conn.set(old,sms_code,ex=5*60)
        return old