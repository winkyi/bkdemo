# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from common.mymako import render_mako_context
from models import Member,Group,Job
import json
from django.http import  HttpResponse
from django.db import transaction


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def helloworld(request):
    return render_mako_context(request,'/home_application/helloworld.html')


def work(request):

    alluser = Member.get_all_members(request.COOKIES.get('bk_token',''))
    print "alluser:%s" % alluser
    print "cookies:%s" % request.COOKIES
    print "current_user:%s" % request.user
    return render_mako_context(request,'/home_application/work.html')



#主页
def index(request,**kwargs):
    login_user = request.user
    kwargs["login_user"] = login_user
    return render_mako_context(request,'/home_application/index.html',kwargs)



#新增会议
def meeting_add(request,**kwargs):
    all_members = Member.get_all_members(request.COOKIES.get('bk_token'))
    kwargs["members"] = all_members
    login_user = request.user
    kwargs["login_user"] = login_user
    return render_mako_context(request,'/home_application/meetingadd.html',kwargs)



#会议内容提交
def meeting_save(request,**kwargs):
    login_user = request.user
    kwargs["login_user"] = login_user
    if (request.method == 'POST'):
        group_name = request.POST["group_name"]
        hostess = request.POST["hostess"]
        recorder = request.POST["recorder"]
        join_member = request.POST.getlist("join_member")
        group_addr = request.POST["group_addr"]
        group_context = request.POST["group_context"]
        data = json.dumps({"group_name":group_name,"hostess":hostess,"recorder":recorder,"join_member":join_member,"group_addr":group_addr,"group_context":group_context})
        Group.add_group(data)
        return render_mako_context(request,'/home_application/meetingsave.html',kwargs)



#获取所有会议
def get_meeting(request,**kwargs):
    all_group = Group.objects.all()
    kwargs["groups"] = all_group
    login_user = request.user
    kwargs["login_user"] = login_user
    return render_mako_context(request,'/home_application/getmeeting.html',kwargs)

#查看单个会议内容
def view_meeting(request,**kwargs):
    gid = request.GET.get("gid")
    group = Group.objects.get(id=gid)
    kwargs["groups"] = group
    login_user = request.user
    kwargs["login_user"] = login_user
    return render_mako_context(request,'/home_application/viewmeeting.html',kwargs)



#工作内容新增页面
def job_add(request,**kwargs):
    gid = request.GET.get("gid")
    kwargs["gid"] = gid
    login_user = request.user
    kwargs["login_user"] = login_user
    return render_mako_context(request,'/home_application/jobadd.html',kwargs)



#工作内容新增
def job_save(request,**kwargs):
    login_user = request.user
    kwargs["login_user"] = login_user
    if (request.method == 'POST'):
        tswk_group_context = request.POST["tswk_group_context"]
        tswk_execution = request.POST["tswk_execution"]
        tswk_remark = request.POST["tswk_remark"]

        nex_group_context = request.POST["nex_group_context"]
        nex_remark = request.POST["nex_remark"]

        gid = request.GET.get("gid")
        try:
            with transaction.atomic():
                lu_obj = Member.objects.get(username=login_user)
                tswk = Job(job_item=tswk_group_context,status=tswk_execution,remark=tswk_remark,follow_member_id=lu_obj.id)
                tswk.save()

                nex = Job(job_item=nex_group_context,remark=nex_remark,follow_member_id=lu_obj.id)
                nex.save()

                #获取会议
                group = Group.objects.get(id=gid)
                group.tswk_job.add(tswk)
                group.nexwk_job.add(nex)
        except Exception as e:
            print "add group fail error is : %s" % e

        all_group = Group.objects.all()
        kwargs["groups"] = all_group
        return render_mako_context(request,'/home_application/getmeeting.html',kwargs)

def test1(request):
    return render_mako_context(request,'/home_application/test1.html')