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

from django.db import models
from account.models import BkUser
from tools import get_all_user
import django.utils.timezone as timezone
import json

"""
用户信息
"""
class Member(models.Model):
    user = models.ForeignKey(BkUser,blank=True,null=True)
    username = models.CharField(u"用户名登录名",max_length=128)
    fullname = models.CharField(u"用户姓名",max_length=128)

    isActive = models.BooleanField(u"是否激活",default=True)

    class Meta:
        verbose_name = u"用户表"
        verbose_name_plural = u"用户表"

    def __unicode__(self):
        return self.username

    @classmethod
    def get_all_members(cls,bk_token):
        data = get_all_user(bk_token)
        if data['data']:
            for u in data['data']:
                Member.get_or_crate_member_by_username(u["bk_username"],u["chname"])
            members = Member.objects.filter(isActive=True)
            return members
        else:
            return []

    #通过用户名获取或者新增一个用户
    @classmethod
    def get_or_crate_member_by_username(cls,username,chname):
        member = Member.get_member_by_username(username)
        if not isinstance(member,Member):
            #创建用户
            member = Member(username=username,fullname=chname)
            member.save()
        return member


    #通过用户名获取一个用户
    @classmethod
    def get_member_by_username(cls,username):
        try:
            member= cls.objects.get(username=username,isActive=True)
        except Exception as e:
            member = None
        return member


"""
工作总结
"""
class Job(models.Model):
    job_item = models.CharField(verbose_name=u"工作事项",max_length=300)
    follow_member = models.ForeignKey(Member,verbose_name=u'跟进人',related_name="job_as_member")
    job_status =  ((0, u'已完成'),(1, u'部分完成'),(2, u'未完成'),)
    status = models.IntegerField(verbose_name=u"完成情况",choices=job_status,default=2)
    remark = models.CharField(verbose_name=u"备注",max_length=300)

    class Meta:
        verbose_name = u"会议组表"
        verbose_name_plural = u"会议组表"

    def __unicode__(self):
        return self.job_item


"""
会议组
"""
class Group(models.Model):
    group_name = models.CharField(u"名称",max_length=300)
    hostess = models.ForeignKey(Member,verbose_name=u"主持人",blank=True,null=True,related_name="group_as_hostess")
    recorder = models.ForeignKey(Member,verbose_name=u"记录人",blank=True,null=True,related_name="group_as_recorder")
    join_member = models.ManyToManyField(Member,verbose_name=u"参会人员",blank=True,null=True,related_name="group_as_join")
    addr = models.CharField(verbose_name=u"会议地点",max_length=300)
    create_time = models.DateTimeField(u"会议创建时间",default=timezone.now())
    group_context = models.CharField(verbose_name=u"会议内容",max_length=300)
    tswk_job = models.ManyToManyField(Job,verbose_name=u"本周工作总结",blank=True,null=True,related_name="group_as_tswk")
    nexwk_job = models.ManyToManyField(Job,verbose_name=u"下周工作总结",blank=True,null=True,related_name="group_as_nexwk")

    class Meta:
        verbose_name = u"会议组表"
        verbose_name_plural = u"会议组表"


    def __unicode__(self):
        return self.group_name


    """
    新增会议信息
    """
    @classmethod
    def add_group(self,data):
        print "data is %s" % data
        try:
            data_dic = json.loads(data)
            g_obj = Group(group_name=data_dic['group_name'],addr=data_dic['group_addr'],group_context=data_dic['group_context'])
            hostess = Member.objects.get(username=data_dic['hostess'])
            recorder = Member.objects.get(username=data_dic['recorder'])
            g_obj.save()
            g_obj.hostess = hostess
            g_obj.recorder = recorder
            join_member = data_dic['join_member']
            g_obj.join_member.add(*join_member)
            g_obj.save()
        except Exception as e:
            print 'add group metting faild,error is %s' % e


