from django.db import models

# Create your models here.

# 品牌型号
class Producter(models.Model):
    text = models.CharField('品牌型号', max_length=400)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = '品牌型号'


# 设备类型
class Device_type(models.Model):
    text = models.CharField('设备类型', max_length=400)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = '设备类型'


# 存放/使用地点
class Location(models.Model):
    text = models.CharField('存放地点', max_length=400)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = '使用/存放地点'


# 外网IP
class Internet_Ip(models.Model):
    ip = models.GenericIPAddressField('公网IP', protocol='ipv4', blank=True, null=True, unique=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name_plural = '外网IP'


# 内网ip网段
class Intranet_Ip(models.Model):
    ip = models.IntegerField('网段')

    def produce_free_ip(self):
        from cmdb_info.models import Pc_Info, Server_Info, Network_Device_Info
        temp = list(range(1, 255))
        ip_list = []
        for i in temp:
            ip = '192.168.' + str(self.ip) + '.' + str(i)
            if not (set(Pc_Info.objects.filter(ip=ip)) or set(Server_Info.objects.filter(ip=ip)) or set(Network_Device_Info.objects.filter(ip=ip))):
                ip_list.append(ip)
        content = [len(ip_list),ip_list[:10]]
        return content



    def __str__(self):
        return str(self.ip)


    class Meta:
        verbose_name_plural = '网段'

