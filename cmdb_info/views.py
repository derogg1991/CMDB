from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Pc_Info, Server_Info, Network_Device_Info
from general.models import Internet_Ip
from django.contrib.auth.decorators import login_required
#
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.cvm.v20170312 import cvm_client, models
import json


def index(request):
    return render(request, 'cmdb_info/index.html')


def info(request):
    if 'pc' in request.path:
        devices = Pc_Info.objects.all()
        page_type = 'pc'
    elif 'server' in request.path:
        devices = Server_Info.objects.all()
        page_type = 'server'
    elif 'network' in request.path:
        devices = Network_Device_Info.objects.all()
        page_type = 'network'
    context = {
        'devices': devices,
        'page_type': page_type,
    }
    return render(request, 'cmdb_info/info.html', context=context)


def detail(request, page_type, pk):
    # 分类判断
    if page_type == 'pc':
        device = Pc_Info.objects.get(pk=pk)
    elif page_type == 'server':
        device = Server_Info.objects.get(pk=pk)
    elif page_type == 'network':
        device = Network_Device_Info.objects.get(pk=pk)
    context = {
        'page_type': page_type,
        'device': device,
    }
    return render(request, 'cmdb_info/detail.html', context=context)


@login_required
def cloud(request):
    # 注意保密
    sId = 'Your_ID'
    sKey = 'Your_Key'

    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
        cred = credential.Credential(sId, sKey)
        # 实例化要请求产品的client对象
        client = cvm_client.CvmClient(cred, "ap-guangzhou")
        # 实例化一个请求对象
        req = models.DescribeInstancesRequest()
        # 传入参数
        req.Limit = 100
        # 通过client对象调用想要访问的接口，需要传入请求对象
        resp = client.DescribeInstances(req).to_json_string()
        servers = json.loads(resp)['InstanceSet']
    except TencentCloudSDKException as err:
        print(err)

    context = {
        'servers': servers,
    }
    return render(request, 'cmdb_info/cloud.html', context=context)


# 报废
@login_required
def scrap(request, page_type, pk):
    # 分类判断
    if page_type == 'pc':
        device = Pc_Info.objects.get(pk=pk)
    elif page_type == 'server':
        device = Server_Info.objects.get(pk=pk)
    elif page_type == 'network':
        device = Network_Device_Info.objects.get(pk=pk)
    # 保存旧值
    device.old_status = device.status
    device.status = '已报废'
    device.save()
    return HttpResponseRedirect(reverse('cmdb_info:%s_info' % page_type))


@login_required
def callback(request, page_type, pk):
    # 分类判断
    if page_type == 'pc':
        device = Pc_Info.objects.get(pk=pk)
    elif page_type == 'server':
        device = Server_Info.objects.get(pk=pk)
    elif page_type == 'network':
        device = Network_Device_Info.objects.get(pk=pk)
    # 取出旧值
    device.status = device.old_status
    device.save()
    return HttpResponseRedirect(reverse('cmdb_info:%s_info' % page_type))


def to_admin(request):
    return HttpResponseRedirect('admin/')


@login_required
def nat_list(request):
    ips = Internet_Ip.objects.all()
    context = {
        "ips": ips,
    }
    return render(request, 'cmdb_info/nats.html', context=context)
