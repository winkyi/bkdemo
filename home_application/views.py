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
from models import Member,Group
import json

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


def index(request):
    return render_mako_context(request,'/home_application/index.html')


def group_add(request,**kwargs):
    all_members = Member.get_all_members(request.COOKIES.get('bk_token'))
    kwargs["members"] = all_members
    print kwargs
    return render_mako_context(request,'/home_application/groupadd.html',kwargs)


def group_save(request):
    if (request.method == 'POST'):
        group_name = request.POST["group_name"]
        hostess = request.POST["hostess"]
        recorder = request.POST["recorder"]
        join_member = request.POST.getlist("join_member")
        group_addr = request.POST["group_addr"]
        group_context = request.POST["group_context"]
        data = json.dumps({"group_name":group_name,"hostess":hostess,"recorder":recorder,"join_member":join_member,"group_addr":group_addr,"group_context":group_context})
        Group.add_group(data)
        return render_mako_context(request,'/home_application/groupsave.html')


def get_groups(request,**kwargs):
    all_group = Group.objects.all()
    kwargs["groups"] = all_group
    return render_mako_context(request,'/home_application/getgroup.html',kwargs)