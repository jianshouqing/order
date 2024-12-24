from django.db import models

# 抽象类
class ActiveBaseModel(models.Model):
    active = models.SmallIntegerField(verbose_name='状态',default=1,choices=((1,'激活'),(0,'删除')))
    class Meta:
        abstract = True

# Create your models here.
class Administrator(ActiveBaseModel):
    username = models.CharField(verbose_name='用户名',max_length=32,db_index=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    mobile = models.CharField(verbose_name='手机号',max_length=11,db_index=True)
    create_date = models.DateTimeField(verbose_name='创建日期',auto_now_add=True)

class Level(ActiveBaseModel):

    title = models.CharField(verbose_name='标题',max_length=32)
    percent = models.IntegerField(verbose_name='折扣',help_text='0-100百分比')

    def __str__(self):
        return self.title

class Customer(ActiveBaseModel):
    username = models.CharField(verbose_name='用户名',max_length=32,db_index=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    mobile = models.CharField(verbose_name='手机号',max_length=11,db_index=True)
    balance = models.DecimalField(verbose_name='账户余额',default=0,max_digits=10,decimal_places=2)
    level = models.ForeignKey(verbose_name='级别',to='Level',on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    creator = models.ForeignKey(verbose_name='创建者',to='Administrator',on_delete=models.CASCADE)

class PricePolicy(models.Model):
    count =models.IntegerField(verbose_name='数量')
    price =models.DecimalField(verbose_name='价格',default=0,max_digits=10,decimal_places=2)