#!/usr/bin/env python
# coding=utf8

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../..")

from sample_config import MNSSampleConfig
from mns.mns_common import *
from mns.account import Account
from mns.subscription import *

if len(sys.argv) < 3:
    print("Please specify endpoint. e.g. python subscribe_queue_endpoint.py cn-hanghzou MySampleSubQueue")
    sys.exit(1)
region = sys.argv[1]
queue_name = sys.argv[2]

# 从sample.cfg中读取基本配置信息
# WARNING： Please do not hard code your accessId and accesskey in next line.(more information: https://yq.aliyun.com/articles/55947)
accessKeyId, accessKeySecret, endpoint, token = MNSSampleConfig.load_config()
account_id = endpoint.split("/")[2].split(".")[0]
queue_endpoint = TopicHelper.generate_queue_endpoint(region, account_id, queue_name)

# 初始化 my_account, my_topic, my_sub
my_account = Account(endpoint, accessKeyId, accessKeySecret, token)
topic_name = sys.argv[3] if len(sys.argv) > 3 else "MySampleTopic"
my_topic = my_account.get_topic(topic_name)

sub_name = sys.argv[4] if len(sys.argv) > 4 else "MySampleTopic-Sub"
my_sub = my_topic.get_subscription(sub_name)

# 创建订阅, 具体属性请参考mns/subscription.py中的SubscriptionMeta结构
sub_meta = SubscriptionMeta(queue_endpoint, notify_content_format=SubscriptionNotifyContentFormat.SIMPLIFIED)
try:
    topic_url = my_sub.subscribe(sub_meta)
    print("Create Subscription Succeed! TopicName: %s SubName: %s Endpoint: %s\n" % (topic_name, sub_name, queue_endpoint))
except MNSExceptionBase as e:
    if e.type == "TopicNotExist":
        print("Topic not exist, please create topic.")
        sys.exit(0)
    elif e.type == "SubscriptionAlreadyExist":
        print("Subscription already exist, please unsubscribe or use it directly.")
        sys.exit(0)
    print("Create Subscription Fail! Exception:%s\n" % e)
