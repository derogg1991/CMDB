from django.db import models
from django.utils import timezone
from general.models import Device_type, Producter, Internet_Ip, Location

# Create your models here.

device_status = (
    ('闲置', '闲置'),
    ('正常使用', '正常使用'),
    ('维修', '维修'),
    ('已报废', '已报废'),
)

server_envs = (
    ('开发环境', '开发环境'),
    ('测试环境', '测试环境'),
    ('生产环境', '生产环境'),
)


class Pc_Info(models.Model):
    # 基本信息
    sn = models.CharField('SN序列号', max_length=200)
    ecar_no = models.CharField('资产编号', max_length=100, unique=True, blank=True)
    ip = models.GenericIPAddressField('IP', protocol='ipv4', blank=True, null=True, unique=True)
    user = models.CharField('责任人', max_length=100, blank=True)
    create_date = models.DateField('购买日期')
    modi_time = models.DateTimeField('变动时间', default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='存放/使用地点')
    status = models.CharField('设备状态', max_length=100, choices=device_status, default='正常使用')
    old_status = models.CharField(max_length=100, blank=True)
    # 详细信息
    producter = models.ForeignKey(Producter, on_delete=models.CASCADE, verbose_name='品牌型号')
    type = models.ForeignKey(Device_type, on_delete=models.CASCADE, verbose_name='设备类型')
    cpu = models.CharField('CPU', max_length=200)
    mem = models.IntegerField('内存(G)')
    disk = models.IntegerField('硬盘(G)')
    remark = models.TextField('备注/维修更改记录', blank=True)

    class Meta:
        verbose_name = '电脑资产详情'
        verbose_name_plural = '电脑资产详情'

    def __str__(self):
        return str(self.ecar_no)


class Server_Info(models.Model):
    # 基本信息
    sn = models.CharField('序列号', max_length=200)
    ecar_no = models.CharField('资产编号', max_length=200, blank=True, unique=True)
    ip = models.GenericIPAddressField('IP', protocol='ipv4', blank=True, null=True, unique=True)
    user = models.CharField('责任人', max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='存放/使用地点')
    create_date = models.DateField('购买日期')
    modi_time = models.DateTimeField('变动时间', default=timezone.now)
    status = models.CharField('设备状态', max_length=100, choices=device_status, default='正常使用')
    # 详细信息
    env = models.CharField('所属环境', choices=server_envs, max_length=400, default='开发环境')
    cpu_core = models.IntegerField('CPU核心数/个')
    cpu_thread = models.IntegerField('CPU线程数/个')
    cpu_no = models.IntegerField('CPU个数', default=1)
    mem = models.IntegerField('内存(G)')
    disk = models.IntegerField('磁盘(G)')
    remark = models.TextField('备注/涉及项目', blank=True)
    type = models.ForeignKey(Device_type, on_delete=models.CASCADE, verbose_name='设备类型')
    producter = models.ForeignKey(Producter, on_delete=models.CASCADE, verbose_name='品牌型号')

    class Meta:
        verbose_name = '线下服务器资产详情'
        verbose_name_plural = '线下服务器资产详情'


class Network_Device_Info(models.Model):
    # 基本信息
    sn = models.CharField('序列号', max_length=200)
    ecar_no = models.CharField('资产编号', max_length=200, blank=True)
    ip = models.GenericIPAddressField('管理IP', protocol='ipv4', blank=True, null=True, unique=True)
    user = models.CharField('责任人', max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='存放/使用地点')
    create_date = models.DateField('购买日期')
    modi_time = models.DateTimeField('变动时间', default=timezone.now)
    status = models.CharField('设备状态', max_length=100, choices=device_status, default='正常使用')
    # 详细信息
    producter = models.ForeignKey(Producter, on_delete=models.CASCADE, verbose_name='品牌型号')
    type = models.ForeignKey(Device_type, on_delete=models.CASCADE, verbose_name='设备类型')
    port = models.IntegerField('端口数')
    remark = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '网络设备详情'
        verbose_name_plural = '网络设备详情'


class Nat_Info(models.Model):
    internet_ip = models.ForeignKey(Internet_Ip, on_delete=models.CASCADE, verbose_name='外网ip')
    out_port = models.CharField('外网端口', max_length=50, unique=True)
    intranet_ip = models.GenericIPAddressField('内网ip', protocol='ipv4')
    in_port = models.CharField('内网端口', max_length=50)
    domain = models.CharField('域名', max_length=100, blank=True)
    user = models.CharField('责任人', max_length=100)
    remark = models.CharField('备注/应用', max_length=400)

    def __str__(self):
        return str(self.internet_ip) + ':' + str(self.out_port)

    class Meta:
        verbose_name = 'NAT映射'
        verbose_name_plural = 'NAT映射'


