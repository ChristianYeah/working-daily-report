"""
MONGO设置
"""
# mongo url
MONGO_URL = "mongodb://localhost:27017/admin"
# 使用replicaset
MONGO_USE_REPLICASET = True
# replicaset名
MONGO_REPLICA_SET = "mgset-123456"
MONGO_DB = "admin"

# git 用户邮箱
AUTHOR_EMAIL = "git@123.com"
# 企业邮箱smtp地址
SMTP_HOST = "smtp.exmail.qq.com"
# 企业邮箱smtp端口
SMTP_PORT = 465
# 名字
NAME = "老实人"
# 部门
DEPARTMENT = "部门"
# 职位
POSITION = "码农"
# 发件人
MAIL_FROM = "abc@123.com"
# 发件人密码
MAIL_PASS = "mima"
# 收件人
MAIL_TO = "ceo@123.com"

BITCHING = True

WORKING_PLATFORMS_NAMES = {
    "API": "后台接口",
}
WORKING_DIRS = {
    "API": '/path/to/api/dir',
}