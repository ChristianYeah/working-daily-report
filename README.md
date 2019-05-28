# 中文
菜鸡写代码 越写越菜


目前只支持腾讯企业邮箱，其他邮箱如果使用SSL认证也是可以发送的


修改```config.py```中的配置（腾讯企业邮箱开启客户端密码的话请使用客户端密码）


```config.py```中的```BITCHING```参数设为```False```则不附带鸡汤文


只能抽取目录当前分支的git记录, ```config.AUTHOR_EMAIL```必须与你提交时的email地址匹配


如果你是一杯茶一包烟一行代码敲一天，请执行时带上--previous参数，默认随机取1-3条


以下仅对抽取之前的提交有效:


如果你每天都敲一行代码请带上-n 5,6,7 随机取1-n条之前的提交


或者你想强制每个项目一定的数量, 请带上 -f 5,4,3 表示三个项目各取5,4,3条


如果你上班中途出去嫖娼了也想记录下来 请带上参数-t 嫖娼,不给钱（逗号分隔）


mongo集合格式
qiangdeyipi: 保存鸡汤，使用字段message


qiangdeerpi: 工作内容，使用字段message, platform


修改```config.py```中的```WORKING_PLATFORM_NAMES```以及```WORKING_DIRS```
例:
```python
WORKING_PLATFORM_NAMES = {
    "API": "后台api接口",
}
WORKING_DIRS = {
    "API": '/path/to/api',
}

# mongo 工作内容
# db.qiangdeerpi.insert_one({"message": "API接口开发", "platform": "API"})
# db.qiangdeerpi.insert_one({"message": "API接口BUG修复", "platform": "API"})
# etc.

# mongo 鸡汤
# db.qiangdeyipi.insert_one({"message": "鲁迅曾经说过，日报这个东西可有可无"})
# db.qiangdeyipi.insert_one({"message": "子曾经曰过，cogito ergo sum"})
# db.qiangdeyipi.insert_one({"message": "Trump says，I'm a fuck head and HUAWEI is the fucker"})
# etc.
```

# 其他自己问或者自己试

python: 3.6, 2.7没测过

# English
I don't give the shit.