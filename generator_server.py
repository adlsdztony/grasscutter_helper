import json
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import start_server
from pywebio.session import download
# from pywebio import start_server

import pymongo

import bson


data = json.load(open('data.json', encoding='UTF-8'))
Art_main = data['art_main']
Art_sub = data['art_sub']
Art_posi = data['art_posi']
Art = data['art']
Char = data['char']
Weapons = data['weapons']
PASSWORD = data['password']

db = pymongo.MongoClient('localhost', 27017).grasscutter
items = db.items


def key_list(dict):
    return list(dict.keys())


def generate_oid():
    id = bson.objectid.ObjectId()
    return str(id)


def save_as_json(file_name, data):
    with open(file_name, 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def download_as_json(name, jsons):
    str = json.dumps(jsons, ensure_ascii=False, indent=4)
    bytelike = str.encode('utf-8')
    # bytelike = bytes(bytelike, encoding='utf-8')
    download(name, bytelike)
    return


def generate_art_id(art, art_posi):
    return int(str(Art[art]) + '5' + str(Art_posi[art_posi]) + '4')


def generate_art_dict(owner_id, item_id, main, sub):
    art = {
      # "_id": {
      #   "$oid": generate_oid()
      # },
      "ownerId": owner_id,
      "itemId": item_id,
      "count": 1,
      "level": 21,
      "exp": 0,
      "totalExp": 0,
      "promoteLevel": 1,
      "locked": False,
      "refinement": 0,
      "mainPropId": main,
      "appendPropIdList": sub
    }
    return art


def write_or_download(data, name, set='items'):
    confirm = actions('是否直接写入数据库', ['是', '导出数据'])
    if confirm == '是':
        password = input('输入密码')
        if password == PASSWORD:
            db[set].insert_many(data)
            popup('写入成功', content='可以退出此页面', size='normal', implicit_close=True, closable=True)
        else:
            popup('密码错误', content='请重新输入', size='normal', implicit_close=True, closable=True)
    else:
        name = input('请输入文件名：', value=name)
        download_as_json(str(name), data)
        popup('导出成功', content='可以退出此页面', size='normal', implicit_close=True, closable=True)


def art_generator():
    arts_list = []
    uid = input('请输入UID：', type=NUMBER)
    while True:
        art_data = input_group("Art data", [
            select('请选择圣遗物套装：', key_list(Art), name='art'),
            select('请选择圣遗物位置：', key_list(Art_posi), name='art_posi'),
            select('请选择主属性：', key_list(Art_main), name='main'),
            select('请选择副属性1：', key_list(Art_sub), name='sub1'),
            input('请输入副属性1数量：', type=NUMBER, name='count1', value='6'),
            select('请选择副属性2：', key_list(Art_sub), name='sub2'),
            input('请输入副属性2数量：', type=NUMBER, name='count2', value='1'),
            select('请选择副属性3：', key_list(Art_sub), name='sub3'),
            input('请输入副属性3数量：', type=NUMBER, name='count3', value='1'),
            select('请选择副属性4：', key_list(Art_sub), name='sub4'),
            input('请输入副属性4数量：', type=NUMBER, name='count4', value='1')
        ])
        main = Art_main[art_data['main']]
        sub = []
        for i in range(4):
            sub.extend([Art_sub[art_data['sub' + str(i + 1)]]])
        for i in range(4):
            sub.extend([Art_sub[art_data['sub' + str(i + 1)]] for i1 in range(art_data['count' + str(i + 1)]-1)])
        item_id = generate_art_id(art_data['art'], art_data['art_posi'])
        art_dict = generate_art_dict(uid, item_id, main, sub)
        arts_list.append(art_dict)
        state = actions('是否继续', ['是', '结束'])
        if state == '结束':
            write_or_download(arts_list, 'art_list.json')
            return


def art_suit_generator():
    def generate_art_id2(art, art_posi):
        return int(str(Art[art]) + '5' + str(art_posi) + '4')
    arts_list = []
    uid = input('请输入UID：', type=NUMBER)
    while True:
        art_data = input_group("Art data", [
            select('请选择圣遗物套装：', key_list(Art), name='art'),
            select('请选择杯子词条：', key_list(Art_main), name='1'),
            select('请选择时记词条：', key_list(Art_main), name='5', value='攻击力百分比'),
            select('请选择头词条：', key_list(Art_main), name='3', value='暴击伤害'),
            input('请输入无圣遗物的暴击数值：', type=NUMBER, name='cri_rate_without', value='5'),
            input('请输入希望的暴击数值：', type=NUMBER, name='cri_rate', value='100'),
            select('请选择主要副属性：', key_list(Art_sub), name='sub1', value='暴击伤害'),
            select('请选择副属性2：', key_list(Art_sub), name='sub2', value='攻击力百分比'),
            select('请选择副属性3：', key_list(Art_sub), name='sub3', value='元素充能效率'),
            select('请选择副属性4：', key_list(Art_sub), name='sub4', value='元素精通')
        ])
        art_data['2'] = '攻击力'
        art_data['4'] = '生命值'
        exp_cri_rate = int((float(art_data['cri_rate']) - 23.3 - 3.9*4 - float(art_data['cri_rate_without']))/3.9)
        suit = []
        posi_list = ['1', '2', '4', '5']
        sub = [Art_sub[art_data['sub' + str(i + 1)]] for i in range(3) if art_data['sub' + str(i + 1)] != art_data[str(3)]]
        if len(sub) < 3:
            sub.append(Art_sub[art_data['sub' + str(4)]])
        sub.extend([Art_sub['暴击率'] for i in range(6)])
        suit.append(generate_art_dict(uid, generate_art_id2(art_data['art'], '3'), Art_main['暴击伤害'], sub))
        for a in posi_list:
            sub = [Art_sub['暴击率']]
            sub.extend(
                [Art_sub[art_data['sub' + str(i + 1)]] for i in range(3) if art_data['sub' + str(i + 1)] != art_data[str(a)]])
            if len(sub) < 4:
                sub.append(Art_sub[art_data['sub' + str(4)]])
            s = 4
            while s < 9 and exp_cri_rate > 0:
                sub.append(Art_sub['暴击率'])
                s += 1
                exp_cri_rate -= 1
            while s < 9:
                if art_data['sub1'] != art_data[str(a)]:
                    sub.append(Art_sub[art_data['sub1']])
                    s += 1
                else:
                    sub.append(Art_sub[art_data['sub2']])
                    s += 1
            suit.append(generate_art_dict(uid, generate_art_id2(art_data['art'], a), Art_main[art_data[a]], sub))
        confirm = actions('是否选择装备角色', ['是', '否'])
        if confirm == '是':
            role = select('请选择角色：', key_list(Char))
            for art in suit:
                art['equipCharacter'] = Char[role]
        arts_list.extend(suit)
        state = actions('是否继续', ['是', '结束'])
        if state == '结束':
            write_or_download(arts_list, 'art_list.json')
            return


def weapon_generator():
    weapon_data = []
    owner_id = input('请输入UID：', type=NUMBER)
    for key, value in Weapons.items():
        weapon_data.append({
          # "_id": {
          #   "$oid": generate_oid()
          # },
          "ownerId": owner_id,
          "itemId": value,
          "count": 1,
          "level": 90,
          "exp": 0,
          "totalExp": 0,
          "promoteLevel": 6,
          "locked": False,
          "affixes": [
            int('1'+str(value))
          ],
          "refinement": 4,
          "mainPropId": 0
                })
    write_or_download(weapon_data, 'all_weapon.json')
    return


def query_data(set, quary, uid):
    list = []
    for term in db[set].find(quary):
        del term['_id']
        term['ownerId'] = uid
        list.append(term)
    return list


def data_download():
    password = input('输入密码')
    if password != PASSWORD:
        return
    group = input_group("Art data", [
        input('set', name='set'),
        input('query', name='query'),
        input('new UID', name='uid', value='10001')
    ])
    query = eval(group['query'])
    data = query_data(group['set'], query, int(group['uid']))
    write_or_download(data, 'data.json', group['set'])
    return


def index():
    put_link('圣遗物生成器\n', app='圣遗物生成器')
    put_link('圣遗物套装生成器(Beta)\n', app='圣遗物套装生成器')
    put_link('全武器生成器\n', app='全武器生成器')
    put_link('数据下载\n', app='数据下载')


if __name__ == '__main__':
    start_server(
        {'index': index,
         '圣遗物生成器': art_generator,
         '全武器生成器': weapon_generator,
         '圣遗物套装生成器': art_suit_generator,
         '数据下载': data_download},
        debug=True,
        host='0.0.0.0',
        port=8080
    )

# if __name__ == '__main__':
#     start_server(
#         {'index': index,
#          '圣遗物生成器': art_generator,
#          '全武器生成器': weapon_generator,
#          '圣遗物套装生成器': art_suit_generator,
#          '数据下载': data_download},
#         debug=True,
#         auto_open_webbrowser=True,
#         remote_access=True,
#         )
