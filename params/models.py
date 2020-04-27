from django.db import models

# Create your models here.

class ExcelFile(models.Model):
    filename = models.CharField(max_length=512)
    excelfile = models.FileField(upload_to = 'excels')

    def __str__(self):
        return self.filename


class InputParams(models.Model):
    model_type = models.CharField(u'模式', max_length=512)
    max_bat = models.FloatField(u'电池最大容量')
    cur_bat = models.FloatField(u'电池当前电量')
    charge_bat = models.FloatField(u'电池充电电量')
    run_bat = models.FloatField(u'电池放电电量')
    a_laden = models.TimeField(u'充电开始时间')
    e_laden = models.TimeField(u'充电结束')
    a_entladen = models.TimeField(u'放电开始')
    e_entladen = models.TimeField(u'放电结束')
    percent_power = models.FloatField(u'供电百分比', default=100)
    netzentlastang = models.FloatField(u'缓解变量', default=100)

    def __str__(self):
        return self.model_type


