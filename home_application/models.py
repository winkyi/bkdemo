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

"""
用户信息
"""
class Member(models.Model):
    user = models.ForeignKey(BkUser,blank=True,null=True)
    username = models.CharField(u"用户名",max_length=128)

    isActive = models.BooleanField(u"是否激活",default=True)

    class Meta:
        verbose_name = u"用户表"
        verbose_name_plural = u"用户表"

    def __unicode__(self):
        return self.username

    @classmethod
    def get_all_members(cls,bk_token):
        username = []
        data = get_all_user(bk_token)
        if data['data']:
            for u in data['data']:
                username.append(u['username'])
        return username


"""
会议组
"""
class Group(models.Model):
    group_name = models.CharField(u"名称",max_length=300)
    hostess = models.ForeignKey(Member,verbose_name=u"主持人",blank=True,null=True,related_name="group_as_hostess")
    recorder = models.ForeignKey(Member,verbose_name=u"记录人",blank=True,null=True,related_name="group_as_recorder")
    join_member = models.ManyToManyField(Member,verbose_name=u"参会人员",blank=True,null=True,related_name="group_as_join")
    addr = models.CharField(verbose_name=u"会议地点",max_length=300)
    quantumtime = models.CharField(verbose_name=u"时间段",max_length=300)


    class Meta:
        verbose_name = u"会议组表"
        verbose_name_plural = u"会议组表"


    def __unicode__(self):
        return self.group_name



"""
工作总结
"""
class Job(models.Model):
    job_item = models.CharField(verbose_name=u"工作事项",max_length=300)
    follow_member = models.ForeignKey(Member,verbose_name=u'跟进人',related_name="job_as_member")
    status = models.BooleanField(verbose_name=u"当前状态",default=False)
    remark = models.CharField(verbose_name=u"备注",max_length=300)



    class Meta:
        verbose_name = u"会议组表"
        verbose_name_plural = u"会议组表"

    def __unicode__(self):
        return self.job_item

