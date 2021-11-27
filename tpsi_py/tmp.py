import random
import json
import pickle
import os
from numpy.lib.function_base import append
import pandas as pd
from hashlib import sha256, md5
import numpy as np


def generate_random_bytes(n: int, byteorder='big'):
    if n <= 0:
        raise ValueError(f"illegal n: {n}")
    randi = random.SystemRandom().getrandbits(n * 8)
    return randi.to_bytes(n, byteorder)


# def id_column_encode(value):
#     # return str(value).encode('utf-8')
#     return md5(value.encode('utf-8')).digest()
#     # if int(value) < 3:
#     #     out["<3"].append(value)
#     # else:
#     #     out[">=3"].append(value)


def divide_to_16iterms(x):
    keys = [0x00, 0x10, 0x20, 0x30,
            0x40, 0x50, 0x60, 0x70,
            0x80, 0x90, 0xa0, 0xb0,
            0xc0, 0xd0, 0xe0, 0xf0]
    keys_for_ret = ['0x0', '0x1', '0x2', '0x3',
                    '0x4', '0x5', '0x6', '0x7',
                    '0x8', '0x9', '0xa', '0xb',
                    '0xc', '0xd', '0xe', '0xf']
    val = x[0] & 0xf0
    if val in keys:
        # index = val >> 4
        return keys_for_ret[val >> 4]

    # if x[0] & 0xf0 == 0x00:
    #     return "0x0"
    # if x[0] & 0xf0 == 0x10:
    #     return "0x1"
    # if x[0] & 0xf0 == 0x20:
    #     return "0x2"
    # if x[0] & 0xf0 == 0x30:
    #     return "0x3"
    # if x[0] & 0xf0 == 0x40:
    #     return "0x4"
    # if x[0] & 0xf0 == 0x50:
    #     return "0x5"
    # if x[0] & 0xf0 == 0x60:
    #     return "0x6"
    # if x[0] & 0xf0 == 0x70:
    #     return "0x7"
    # if x[0] & 0xf0 == 0x80:
    #     return "0x8"
    # if x[0] & 0xf0 == 0x90:
    #     return "0x9"
    # if x[0] & 0xf0 == 0xa0:
    #     return "0xa"
    # if x[0] & 0xf0 == 0xb0:
    #     return "0xb"
    # if x[0] & 0xf0 == 0xc0:
    #     return "0xc"
    # if x[0] & 0xf0 == 0xd0:
    #     return "0xd"
    # if x[0] & 0xf0 == 0xe0:
    #     return "0xe"
    # if x[0] & 0xf0 == 0xf0:
    #     return "0xf"
    # pass


if __name__ == "__main__":
    for i in range(30, 33):
        print(i)
    bn = generate_random_bytes(16)
    # print("===>>bn:", bn+bn, len(bn+bn))
    # f.write()
    js = pickle.dumps(16)
    # print("js:", js, len(js))
    n = pickle.loads(js)
    print("n:", n)
    # print(list(3))
    l = []
    # l.append(19)
    append(l, 19)
    print(l)
    # 3
    # dfa_id = pd.read_csv('../pid0.csv', dtype={'id': 'object'}, usecols=['id'])
    # dfa_id = pd.read_csv(
    #     '../pid40w_0.csv', dtype={'id': 'object'}, usecols=['id'])
    dfa_id = pd.read_csv('test.csv', dtype={'id': 'object'}, usecols=['id'])
    count = dfa_id.shape[0]
    print("===count:", count)
    # dfa_id['unique_index'] = dfa_id.index.tolist()
    print("=======src::\n", dfa_id)
    # print("=======res\n", res)
    # dfa_id['hash_id'] = dfa_id.applymap(
    #     lambda x: md5(x.encode('utf-8')).digest())
    hsId = dfa_id.applymap(
        lambda x: md5(str(x).encode('utf-8')).digest())
    print('+++++++++hsId:\n', hsId)
    print('+++++++++dfa_id:\n', dfa_id)
    print("======>>>>\n", list(dfa_id.loc[range(10), ['id']]['id']))
    s1 = set([1, 2, 4, 7])
    s2 = set([1, 2, 4, 8, 9])
    inter = s1.intersection(s2)
    uni = s1.union(s2)
    print("====", inter)
    print("====", uni)
    print('__________________')
    exit()
    # print(dfa_id['id'].tolist())
    # print("=======\n", dfa_id)

    def hex_ecode(x: bytes):
        return x.hex()
    # dfa_id['hash_id_hex'] = dfa_id['hash_id'].apply(hex_ecode)
    # dd = dict()
    dfa_id['hash_id_key'] = dfa_id['hash_id'].apply(divide_to_16iterms)
    dfa_id['unique_index'] = dfa_id.index.tolist()
    dfa_id.set_index('hash_id', inplace=True)
    dfa_id['hash_id'] = dfa_id.index.tolist()
    dfa_id.set_index('unique_index', inplace=True)
    dfa_id['unique_index'] = dfa_id.index.tolist()
    # dfa_id.set_index('hash_id_key', inplace=True)
    print("=======\n", dfa_id)
    # dfa_hash_id = dfa_id.apply()
    # dfr_id = dfa_hash_id.values.reshape(count)
    # 取出
    keys = ['0x0', '0x1', '0x2', '0x3',
            '0x4', '0x5', '0x6', '0x7',
            '0x8', '0x9', '0xa', '0xb',
            '0xc', '0xd', '0xe', '0xf']
    dict_job = {}
    n = 0
    for key in keys:
        key_df = dfa_id.loc[dfa_id['hash_id_key'] == key]
        lst1 = list(key_df["hash_id"])
        print("====len:", len(lst1))
        n = n+len(lst1)
        dict_job[key] = lst1
    print('===============================', n)
    key_df_1 = dfa_id.loc[[1, 3]]
    print('---------------------\n', key_df_1)
    print('---------------------\n', list(key_df_1['unique_index']) == [1, 3])

    # print('===============================\n', dict_job['0x0'])
    # print(dict_job, n)
    # ##################################
    # psi_n = 200000
    # set_size = 400000
    # ls = [b'']*set_size
    # for i in range(0, psi_n):
    #     # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
    #     ls[i] = md5((str(i)+'qwe').encode('utf-8')).hexdigest()[:16]
    # print("====ls[0]:", ls[0], len(ls[0]))
    # bn = generate_random_bytes(16)
    # for i in range(psi_n, set_size):
    #     # ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')
    #     #             ).hexdigest()[:16].encode('utf-8')
    #     ls[i] = md5((str(i) + 'qqq').encode('utf-8') +
    #                 bn).hexdigest()[:16]
    # df = pd.DataFrame({'id': ls})
    # # f=open("../pid0.csv", 'w')
    # df.to_csv("../pid40w_2.csv")
    # # df.to_csv("../pid40w_2.csv")
    ######################################
    ll = [3, 5, 1, 7]
    l2 = [31, 52, 13, 73]
    ll.sort(reverse=True)
    print(ll)
    if 1 in ll:
        print("1 is in")
    lll = ll
    print(lll)
    lll.append(99)
    print("lll:", lll)
    print("ll :", ll)
    print([x for x in range(16)])
    lll = lll+l2
    print(lll)
    hexs = 'abff'
    bn = bytes.fromhex(hexs)
    print('>>>>bn:', bn, len(bn), len(hexs))
# def funa(x):
#     if x > 3:
#         return True
#     else:
#         return False


# df_tmp['a'] = df_tmp["val_0"].apply(binc)
# # print(df_tmp)
# lst1 = df_tmp.loc[df_tmp['a'] == True]
# print(lst1)
# x = list(lst1["val_0"])
# print(x)
