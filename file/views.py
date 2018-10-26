from typing import Tuple

from django.shortcuts import render
from .forms import UpLoadFileForm
from .models import FileModel
from cmdb_info.models import Pc_Info, Server_Info, Network_Device_Info
from general.models import Location, Device_type, Producter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import codecs
import csv
import os
import datetime
import subprocess
import chardet


# Create your views here.


# 上传文件
@login_required
def upload_file(request, page_type):
    if page_type == 'pc':
        device = Pc_Info
    elif page_type == 'server':
        device = Server_Info
    else:
        device = Network_Device_Info
    if request.method == 'POST':
        form = UpLoadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = FileModel()
            upload_file.file = form.cleaned_data['file']
            upload_file.save()
            if change_code() is True:
                code_result = '转码成功'
            else:
                code_result = '转码失败'
            if check_file(device) is True:
                error = '检查通过'
                if import_file(device) is True:
                    error = '导入成功'
            else:
                error = check_file(device)
            clean_work()
            context = {
                'message': '文件上传成功!',
                'code_result': code_result,
                'error': error,
            }
            return render(request, 'file/upload_success.html', context=context)
    else:
        form = UpLoadFileForm()
        context = {
            'form': form,
            'page_type': page_type,
        }
        return render(request, 'file/file.html', context=context)


# 下载模板
@login_required
def down_template(request, page_type):
    # 生成csv响应头对象response
    response = HttpResponse(content_type='text/csv')
    # 加入编码防止中文乱码
    response.write(codecs.BOM_UTF8)
    # 下载文件到硬盘而不是直接网页打开
    response['Content-Disposition'] = 'attachment; filename="temp_%s.csv"' % page_type
    # 生成csv文件
    writer = csv.writer(response)
    if page_type == 'pc':
        writer.writerow(['SN序列号', '资产编号', 'IP',
                         '责任人', '存放/使用地点', '购买日期',
                         '设备状态', '设备类型', '品牌型号',
                         'CPU', '内存', '硬盘', '备注']
                        )
    elif page_type == 'server':
        writer.writerow(['SN序列号', '资产编号', 'IP',
                         '责任人', '存放/使用地点', '购买日期',
                         '所属环境', '设备状态', '设备类型', '品牌型号',
                         'CPU个数', 'CPU核心数', 'CPU线程数',
                         '内存', '硬盘', '备注']
                        )
    elif page_type == 'network':
        writer.writerow(['SN序列号', '资产编号', 'IP',
                         '责任人', '存放/使用地点', '购买日期',
                         '设备状态', '设备类型', '品牌型号',
                         '端口数', '备注']
                        )

    return response


# 校验文件
## 功能函数

# 改变文件编码
def change_code():
    _, csv_file = get_file_path()
    with open(csv_file, 'rb') as f:
        data = f.read()
    code = str(chardet.detect(data)['encoding'])
    command = "iconv -f %s -t UTF-8 %s -o %s" % (code, csv_file, csv_file)
    p = subprocess.call(command,shell=True)
    if p == 0:
        return True
    else:
        return False
    
# 判断是否为正整数
def is_int(s):
    try:
        x = int(s)
        return isinstance(x, int)
    except ValueError:
        return False


# 验证ip地址
def is_ip(s):
    sep = s.split('.')
    if len(sep) != 4:
        return False
    for i in sep:
        if not is_int(i):
            return False
        elif int(i) > 255:
            return False
    return True


# 验证时间格式
def is_right_date(s):
    dt = datetime.datetime.now()
    sep = s.split('/')
    if len(sep) != 3:
        return False
    for i in sep:
        if not is_int(i):
            return False
    if int(sep[2]) > dt.day:
        if int(sep[1]) > dt.month:
            if int(sep[0]) > dt.year:
                return False
    return True


# 检验数据库信息是否存在
def is_model_data_exist(model, s, x=None):
    if x is None:
        return bool(model.objects.filter(text=s))
    elif x == 'ecar_no':
        return bool(model.objects.filter(ecar_no=s))
    elif x == 'ip':
        return bool(model.objects.filter(ip=s))


def clean_work():
    file_path, csv_file = get_file_path()
    try:
        os.remove(csv_file)
        os.rmdir(file_path)
        return True
    except Exception as e:
        return e


def get_file_path():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    date = str(datetime.date.today())
    # 文件夹路径
    file_path = os.path.join(project_dir, 'media', 'uploadfile', date)
    file_name = os.listdir(file_path)[0]
    # 文件路径
    csv_file = os.path.join(file_path, file_name)
    return (file_path, csv_file)


def check_ip(s):
    if not Pc_Info.objects.filter(ip=s):
        if not Server_Info.objects.filter(ip=s):
            if not Network_Device_Info.objects.filter(ip=s):
                return True
    return False


def create_greneral_data(row):
    if not is_model_data_exist(Location, row['存放/使用地点']):
        l = Location.objects.create(text=row['存放/使用地点'])
    if not is_model_data_exist(Producter, row['品牌型号']):
        p = Producter.objects.create(text=row['品牌型号'])
    if not is_model_data_exist(Device_type, row['设备类型']):
        d = Device_type.objects.create(text=row['设备类型'])

# 固定选项
device_status = ('闲置', '正常使用', '维修', '已报废')
server_envs = ('开发环境', '测试环境', '生产环境',)


# 主功能函数
def check_file(model):
    file_path, csv_file = get_file_path()
    line = 2
    # 读取csv文件并验证数据正确
    try:
        with open(csv_file) as f:
            f_reader = csv.DictReader(f)
            for row in f_reader:
                create_greneral_data(row)
                # 格式验证
                if len(row) == 1:
                    return '格式错误,是否没有分列?'
                elif not row['设备状态'] in device_status:
                    return '设备状态错误.Line:%i' % line
                elif not row['IP'] == '':
                    if not is_ip(row['IP']):
                        return 'IP字段格式错误.Line:%i' % line
                elif not is_right_date(str(row['购买日期'])):
                    return '购买日期格式错误.Line:%i' % line
                elif not row['IP'] == '':
                    if not check_ip(row['IP']):
                        return 'IP已存在.Line:%i' % line
                elif is_model_data_exist(model, row['资产编号'], x='ecar_no'):
                    return '资产编号已存在.Line:%i' % line
                elif model is Server_Info:
                    if not row['所属环境'] in server_envs:
                        return '所属环境错误.Line:%i' % line
                    elif not (is_int(row['CPU核心数']) & is_int(row['CPU线程数']) & is_int(row['CPU个数'])):
                        return 'CPU核心数/线程数/个数不是正整数.Line:%i' % line
                elif model is Network_Device_Info:
                    if not is_int(row['端口数']):
                        return '端口数不是正整数.Line:%i' % line
                elif not model is Network_Device_Info:
                    if not is_int(row['内存']):
                        return '内存的值不是正整数.Line:%i' % line
                    elif not is_int(row['硬盘']):
                        return '硬盘的值不是正整数.Line:%i' % line
                else:
                    line += 1
            return True
    except Exception:
        return '导入失败'


def import_file(model):
    file_path, csv_file = get_file_path()
    with open(csv_file) as f:
        f_reader = csv.DictReader(f)
        for row in f_reader:
            l = Location.objects.get(text=row['存放/使用地点'])
            p = Producter.objects.get(text=row['品牌型号'])
            t = Device_type.objects.get(text=row['设备类型'])
            dt = '-'.join(row['购买日期'].split('/'))
            if model is Pc_Info:
                new = Pc_Info(sn=row['SN序列号'], ecar_no=row['资产编号'], ip=row['IP'], user=row['责任人'], location=l,
                              create_date=dt, status=row['设备状态'], type=t, producter=p, cpu=row['CPU'],
                              mem=int(row['内存']), disk=int(row['硬盘']), remark=row['备注'])
            elif model is Server_Info:
                new = Server_Info(sn=row['SN序列号'], ecar_no=row['资产编号'], ip=row['IP'], user=row['责任人'], location=l,
                                  create_date=dt, env=row['所属环境'], status=row['设备状态'], type=t, producter=p,
                                  cpu_no=int(row['CPU个数']), cpu_core=int(row['CPU核心数']), cpu_thread=int(row['CPU线程数']),
                                  mem=int(row['内存']), disk=int(row['硬盘']), remark=row['备注'])
            elif model is Network_Device_Info:
                new = Network_Device_Info(sn=row['SN序列号'], ecar_no=row['资产编号'], ip=row['IP'], user=row['责任人'],
                                          location=l, create_date=dt, status=row['设备状态'], type=t, producter=p,
                                          port=int(row['端口数']), remark=row['备注'])
            new.save()
        return True


# 导出
@login_required
def export(request, page_type):
    # 生成csv响应头对象response
    response = HttpResponse(content_type='text/csv')
    # 加入编码防止中文乱码
    response.write(codecs.BOM_UTF8)
    # 下载文件到硬盘而不是直接网页打开
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % page_type
    # 生成csv文件
    writer = csv.writer(response)
    if page_type == 'pc':
        writer.writerow(['SN序列号', '资产编号', 'IP',
                         '责任人', '存放/使用地点', '购买日期',
                         '设备状态', '设备类型', '品牌型号',
                         'CPU', '内存', '硬盘', '备注']
                        )
        for obj in Pc_Info.objects.all():
            writer.writerow([obj.sn, obj.ecar_no, obj.ip,
                             obj.user, obj.location, obj.create_date,
                             obj.status, obj.type, obj.producter,
                             obj.cpu, obj.mem, obj.disk, obj.remark]
                            )
    elif page_type == 'server':
        writer.writerow(['SN序列号', '资产编号', 'IP',
                         '责任人', '存放/使用地点', '购买日期',
                         '所属环境', '设备状态', '设备类型', '品牌型号',
                         'CPU个数', 'CPU核心数', 'CPU线程数',
                         '内存', '硬盘', '备注']
                        )
        for obj in Server_Info.objects.all():
            writer.writerow([obj.sn, obj.ecar_no, obj.ip,
                             obj.user, obj.location, obj.create_date,
                             obj.env, obj.status, obj.type, obj.producter,
                             obj.cpu_no, obj.cpu_core, obj.cpu_thread,
                             obj.mem, obj.disk, obj.remark]
                            )
    elif page_type == 'network':
        writer.writerow(['SN序列号', '资产编号', 'IP',
                         '责任人', '存放/使用地点', '购买日期',
                         '设备状态', '设备类型', '品牌型号',
                         '端口数', '备注']
                        )
        for obj in Server_Info.objects.all():
            writer.writerow([obj.sn, obj.ecar_no, obj.ip,
                             obj.user, obj.location, obj.create_date,
                             obj.status, obj.type, obj.producter,
                             obj.port, obj.remark]
                            )
    return response
