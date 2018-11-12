from django.db import models
import datetime
from django.utils import  timezone
# Create your models here.
#user_approve table
class UserApprove(models.Model):
    iduser_approve = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    user_approvecol = models.CharField(max_length=45, blank=True, null=True)
    user_approvecol1 = models.CharField(max_length=45, blank=True, null=True)
    user_approvecol2 = models.CharField(max_length=45, blank=True, null=True)
    datetimes = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_approve'
#user_info table
class UserInfo(models.Model):
    iduser_info = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    user_name = models.CharField(max_length=45, blank=True, null=True)
    user_age = models.IntegerField(blank=True, null=True)
    user_phone = models.CharField(max_length=45, blank=True, null=True)
    user_sex = models.IntegerField(blank=True, null=True)
    user_infocol1 = models.CharField(max_length=45, blank=True, null=True)
    user_infocol2 = models.CharField(max_length=45, blank=True, null=True)
    user_infocol3 = models.CharField(max_length=45, blank=True, null=True)
    user_infocol4 = models.CharField(max_length=300, blank=True, null=True)
    user_infocol = models.CharField(max_length=45, blank=True, null=True)
    user_create_time = models.CharField(max_length=45, blank=True, null=True)
    worktype = models.CharField(max_length=45, blank=True, null=True)
    workcompany = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'
#user_statu view
class UserInfoStatu(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.CharField(max_length=200, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    datetimes = models.CharField(max_length=60, blank=True, null=True)
    approvetimes=models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    createtime = models.CharField(max_length=45, blank=True, null=True)
    worktype = models.CharField(max_length=45, blank=True, null=True)
    workcompany = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'user_statu'

class CollectFormid(models.Model):
    idcollect_formid = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    formid = models.CharField(max_length=200, blank=True, null=True)
    frombtn = models.CharField(max_length=45, blank=True, null=True)
    datetime = models.CharField(max_length=100, blank=True, null=True)
    other1 = models.CharField(max_length=45, blank=True, null=True)
    other2 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collect_formid'


