from django.db import models

# Create your models here.
#House infomations model
class Houseinfo(models.Model):
    addtime = models.CharField(max_length=20, blank=True, null=True)
    updatetime = models.CharField(max_length=20, blank=True, null=True)
    communityid = models.CharField(max_length=50, blank=True, null=True)
    buildingnumber = models.CharField(max_length=10, blank=True, null=True)
    totalfloors = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    housetype = models.CharField(max_length=10, blank=True, null=True)
    orientation = models.CharField(max_length=10, blank=True, null=True)
    decoration = models.CharField(max_length=10, blank=True, null=True)
    additional = models.IntegerField(blank=True, null=True)
    gardenarea = models.FloatField(blank=True, null=True)
    loftarea = models.FloatField(blank=True, null=True)
    terracearea = models.FloatField(blank=True, null=True)
    basementarea = models.FloatField(blank=True, null=True)
    averageprice = models.FloatField(blank=True, null=True)
    totalprice = models.FloatField(blank=True, null=True)
    describe = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    turnovertime = models.CharField(max_length=50, blank=True, null=True)
    scoreflag = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'houseinfo'


#Community infomations model
class Communityinfo(models.Model):
    openid = models.CharField(max_length=200, blank=True, null=True)
    flag=models.IntegerField(blank=True, null=True)
    addtime = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    alias = models.CharField(max_length=200, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    uses = models.CharField(max_length=20, blank=True, null=True)
    buildingyear = models.CharField(max_length=20, blank=True, null=True)
    developer = models.CharField(max_length=20, blank=True, null=True)
    buildingtype = models.CharField(max_length=20, blank=True, null=True)
    landarea = models.FloatField(blank=True, null=True)
    structureareasum = models.FloatField(blank=True, null=True)
    housingsum = models.IntegerField(blank=True, null=True)
    buildingsum = models.IntegerField(blank=True, null=True)
    managecompany = models.CharField(max_length=100, blank=True, null=True)
    greenratio = models.CharField(max_length=10, blank=True, null=True)
    plotratio = models.CharField(max_length=10, blank=True, null=True)
    managefee = models.FloatField(blank=True, null=True)
    watersupply = models.CharField(max_length=50, blank=True, null=True)
    heatsupply = models.CharField(max_length=50, blank=True, null=True)
    busstation = models.CharField(max_length=200, blank=True, null=True)
    subway = models.CharField(max_length=200, blank=True, null=True)
    kindergarten = models.CharField(max_length=200, blank=True, null=True)
    school = models.CharField(max_length=200, blank=True, null=True)
    shopping = models.CharField(max_length=200, blank=True, null=True)
    hospital = models.CharField(max_length=200, blank=True, null=True)
    park = models.CharField(max_length=200, blank=True, null=True)
    bank = models.CharField(max_length=200, blank=True, null=True)
    entertainment = models.CharField(max_length=200, blank=True, null=True)
    updatetime = models.CharField(max_length=20, blank=True, null=True)
    groundtime = models.CharField(max_length=20, blank=True, null=True)
    undertime = models.CharField(max_length=20, blank=True, null=True)
    describe = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    scoreflag = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'communityinfo'

#user score statu record
#gains_reson is type 1  type 2  infoid is community_id or house_id
class UserGains(models.Model):
    openid = models.CharField(max_length=200, blank=True, null=True)
    infoid=models.CharField(max_length=50, blank=True, null=True)
    scorer=models.CharField(max_length=50, blank=True, null=True)
    operate = models.CharField(max_length=200, blank=True, null=True)
    gains_datetime = models.CharField(max_length=50, blank=True, null=True)
    others = models.CharField(max_length=50, blank=True, null=True)
    gains_reson = models.CharField(max_length=80, blank=True, null=True)
    gains_value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_gains'

class GainsSum(models.Model):
    id = models.IntegerField(primary_key=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    money = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'gains_sum'

