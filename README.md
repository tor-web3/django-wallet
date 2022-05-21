# 简介

Django 区块链钱包应用

# 应用

```
pip install Django>=4.0.4,<5
# 构建本地数据库
python manage.py migrate
# 创建超级用户
python manage.py createsuperuser
# 加载基础区块链数据
python manage.py loaddata wallet.json
# 创建钱包地址
python manage.py create_deposit_address -u [username or uid]
```