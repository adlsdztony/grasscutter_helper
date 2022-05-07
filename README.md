# grasscutter_helper
artifacts generator/weapons generator with GUI by pywebio
圣遗物/武器自动生成器

# language
chinese only

# 特性
* 可视化界面生成圣遗物，可以指定主副词条
* 一键生成圣遗物套装（5个圣遗物）（仅支持需要堆暴击的角色）
* 一键导入5星与4星全武器（精5 90级）
* 以上操作均可一键导入数据库
* 数据库操作（将角色或物品从一个账号复制到另一个账号）

## 单个圣遗物生成
* 副词条默认最大值 如：暴击率 3.9%
* 词条数总和不应超过9 （虽然超了也没事）
* 副词条不应与主词条相同（虽然也没事）

## 圣遗物套装生成
* 会优先将暴击率堆到设定数值
* 不支持暴击头！选爆伤头就好，反正暴击靠副词条也堆得上去
* 暴击堆满后会优先堆‘主要副词条’
* 可以选择装备角色，但是要注意该角色是否装备圣遗物（没测试过，不知道后果）

## 武器生成
* 输入UID自动生成全武器
* 每种一把，需要多把就多生成几次

## 一键导入数据库
* 最后选是就可以一键导入
* 默认密码为123456，可以在data.json中修改
* 需要重新登录才能生效

## 数据库操作
* 没有看过数据库的最好不要碰

# 运行
* 分为本地版（local）和服务器版（server）
* requirements: pywebio pymongo 服务器版还需要 flask
* 下载对应版本与data.json，放入同一文件夹，双击运行
* server版默认端口为8080
```shell
git clone https://github.com/TZonyhou/grasscutter_helper.git
pip install -r requirements.txt
python generator_local.py
```


# 关于
* 本人高三党，自学的python，所以代码写的不好，轻喷
