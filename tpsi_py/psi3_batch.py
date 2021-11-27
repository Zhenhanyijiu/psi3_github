from tpsi import psi3_process_by_boost
import numpy as np
from hashlib import sha256, md5
import sys
import getopt
import time
import random
import socket
import pickle
import pandas as pd
import os


class Server(object):
    def __init__(self, host, port):
        # self.buf_size = 100 * 1024 * 1024
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, port))
        serversocket.listen(1)
        self.clientsocket, self.addr = serversocket.accept()
        print('accept ok ...')

    def send_data(self, msg):
        head = len(msg)
        head_bytes = self.int_to_bytes(head)
        self.clientsocket.sendall(head_bytes)
        self.clientsocket.sendall(msg)
        # print("send n:", n)

    def recv_data(self):
        head = bytes()
        head_len = 0
        while True:
            tmp = self.clientsocket.recv(4 - head_len)
            tmp_n = len(tmp)
            head += tmp
            head_len += tmp_n
            if head_len < 4:
                continue
            else:
                break
        data_len = self.byte_to_int(head)
        data = bytes()
        data_recv = 0
        while True:
            ret = self.clientsocket.recv(data_len - data_recv)
            ret_len = len(ret)
            data += ret
            data_recv += ret_len
            if data_recv < data_len:
                continue
            else:
                break
        return data

    def close(self):
        self.clientsocket.close()
        pass

    def int_to_bytes(self, n: int):
        bys = bytearray(4)
        bys[3] = (n >> 24) & 0xff
        bys[2] = (n >> 16) & 0xff
        bys[1] = (n >> 8) & 0xff
        bys[0] = n & 0xff
        return bytes(bys)

    def byte_to_int(self, b: bytes):
        if len(b) == 4:
            b1 = b[0] & 0xff
            b2 = (b[1] << 8) & 0xff00
            b3 = (b[2] << 16) & 0xff0000
            b4 = (b[3] << 24) & 0xff000000
            return b1 + b2 + b3 + b4
        else:
            print("len:", len(b))
            raise Exception('length error')


class Client(object):
    def __init__(self, host, port):
        self.buf_size = 100 * 1024 * 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务，指定主机和端口
        start = time.time()
        time_end = 3600*2+start
        while True:
            if time.time() < time_end:
                try:
                    self.s.connect((host, port))
                    print("client con ok")
                    break
                except:
                    pass
            else:
                break

    def send_data(self, msg):
        head = len(msg)
        head_bytes = self.int_to_bytes(head)
        self.s.sendall(head_bytes)
        self.s.sendall(msg)

    def recv_data(self):
        head = bytes()
        head_len = 0
        while True:
            tmp = self.s.recv(4 - head_len)
            tmp_n = len(tmp)
            head += tmp
            head_len += tmp_n
            if head_len < 4:
                continue
            else:
                break
        data_len = self.byte_to_int(head)
        data = bytes()
        data_recv = 0
        while True:
            ret = self.s.recv(data_len - data_recv)
            ret_len = len(ret)
            data += ret
            data_recv += ret_len
            if data_recv < data_len:
                continue
            else:
                break
        return data

    def close(self):
        self.s.close()

    def int_to_bytes(self, n: int):
        bys = bytearray(4)
        bys[3] = (n >> 24) & 0xff
        bys[2] = (n >> 16) & 0xff
        bys[1] = (n >> 8) & 0xff
        bys[0] = n & 0xff
        return bytes(bys)

    def byte_to_int(self, b: bytes):
        if len(b) == 4:
            b1 = b[0] & 0xff
            b2 = (b[1] << 8) & 0xff00
            b3 = (b[2] << 16) & 0xff0000
            b4 = (b[3] << 24) & 0xff000000
            return b1 + b2 + b3 + b4
        else:
            print("len:", len(b))
            raise Exception('length error')


class PSI3(object):
    def __init__(self, p_id: int, ip_array: list, port_array: list, set_size: int):
        self.p_id = p_id
        self.ip_array = [x.encode('utf-8') for x in ip_array]
        self.port_array = port_array
        self.set_size = set_size
        self.n_parties = 3

    def psi3_process(self, set_data: np.array):
        # ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
        # ip_array = ["10.100.3.15", "10.100.3.15", "10.100.3.16"]
        if len(set_data) != self.set_size:
            raise Exception('set_size is error,pad data please')
        # ip_array_byte = [str(x).encode('utf-8') for x in self.ip_array]
        # ip_array_byte = [x.encode('utf-8') for x in ip_array]
        print('====psi3_process self.ip_array:', self.ip_array)
        print('====psi3_process self.port_array:', self.port_array)
        # [x.encode('utf-8') for x in ip_array]
        # 测试数据生成
        # psi_n = 6000000
        # ls = [b''] * set_size
        # print("===>>set_size:", set_size)
        # print("===>>psi_n   :", psi_n)
        # for i in range(0, psi_n):
        #     # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
        #     ls[i] = md5(str(i).encode('utf-8')).digest()
        # print("====ls[0]:", ls[0], len(ls[0]))
        # bn = generate_random_bytes(16)
        # for i in range(psi_n, set_size):
        #     # ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')
        #     #             ).hexdigest()[:16].encode('utf-8')
        #     ls[i] = md5((str(i) + 'qqq' + str(p_id)
        #                  ).encode('utf-8')+bn).digest()
        # port_array = [[0, 12001, 12002],
        #               [12001, 0, 12003],
        #               [12002, 12003, 0]]
        port_array = self.port_array
        psi_results = psi3_process_by_boost(
            self.p_id, self.set_size, self.ip_array, port_array, set_data)
        print("===>>psi_result num:", len(psi_results))
        return psi_results


def divide_to_16iterms(x):
    keys = [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
            0x80, 0x90, 0xa0, 0xb0, 0xc0, 0xd0, 0xe0, 0xf0]
    keys_for_ret = ['0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7',
                    '0x8', '0x9', '0xa', '0xb', '0xc', '0xd', '0xe', '0xf']
    val = x[0] & 0xf0
    if val in keys:
        # index = val >> 4
        return keys_for_ret[val >> 4]


class Psi3PocCsv(object):
    def __init__(self, p_id: int, ip_array: list, file_dir: str,
                 is_debug: bool = False,
                 set_size_debug: int = 1000000,
                 inter_size_debug: int = 30000):
        self.p_id = p_id
        self.ip_array = ip_array
        self.file_dir = file_dir
        self.keys = ['0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7',
                     '0x8', '0x9', '0xa', '0xb', '0xc', '0xd', '0xe', '0xf']
        # 将桶存成字典
        self.dict_bucket = {}
        # 每个桶对应的数据个数
        self.dict_bucket_lens = {}
        # 每个桶，协商的最大id个数
        self.dict_bucket_max_sub_set_size = {}
        self.n_parties = 3
        self.is_debug = is_debug
        self.set_size_debug = set_size_debug
        self.inter_size_debug = inter_size_debug
        # self.psi_results_list = []

    def init_psi(self, id_name):
        start_csv = time.time()
        dfa_id = self.__get_id_data_frame(id_name)
        end_csv = time.time()  # 12G mem
        print("=========read csv use time:{} s\n".format(end_csv-start_csv))
        count = dfa_id.shape[0]
        # dfa_id.to_csv("../psi_1e_3kw_"+str(self.p_id)+".csv")
        print("===dataframe row count:", count)
        print('=====sleep\n')
        # time.sleep(10*60)
        # 加一列，hash_id
        hash_id_tmp = pd.DataFrame(dfa_id[id_name]).applymap(
            lambda x: md5(x.encode('utf-8')).digest())
        hash_id_tmp['id_src'] = dfa_id[id_name]
        # 加一列,用于分桶的标志
        hash_id_tmp['hash_id_key'] = hash_id_tmp[id_name].apply(
            divide_to_16iterms)
        # 加一列，索引列
        # dfa_id['unique_index'] = dfa_id.index.tolist()
        # dfa_id['hash_id_len'] = dfa_id['hash_id'].apply(lambda x: len(x))
        print("==========>>索引列use time:{}s".format(time.time()-start_csv))
        n = 0
        # 分成16类
        for cyc_n, key in enumerate(self.keys):
            # 把等于某个key的hash_id取出来,成list
            key_df = hash_id_tmp.loc[hash_id_tmp['hash_id_key'] == key]
            # lst1 = list(key_df["hash_id"]),将这些id分成一桶
            lst1 = list(key_df["id_src"])  # 字符串类型
            n = n+len(lst1)
            # self.dict_bucket[key] = lst1
            # self.dict_bucket_lens[key] = len(lst1)
            print('===每桶的个数:', len(lst1))
            save_df = pd.DataFrame({"id": lst1})
            save_df.to_csv(str(self.p_id)+"_bucket"+"_"+str(cyc_n)+".csv")

        # self.dfa_id = dfa_id
        print('===>>id_num_all:', n)

    def start_psi(self, cyc_n: int):
        bucket_id_df = self.__get_id_data_frame_path(
            str(self.p_id)+"_bucket"+"_"+str(cyc_n)+".csv")
        count = bucket_id_df.shape[0]
        # dfa_id.to_csv("../psi_1e_3kw_"+str(self.p_id)+".csv")
        print("===bucket dataframe row count:", count)
        port_array = get_port_array(self.n_parties, cyc_n, False)
        conns = []
        # ip_array = [x.decode('utf-8') for x in self.ip_array]
        # 建立连接
        for i in range(self.n_parties):
            if i < self.p_id:
                c = Client(self.ip_array[i], port_array[self.p_id][i])
                conns.append(c)
            elif i > self.p_id:
                c = Server(self.ip_array[self.p_id], port_array[self.p_id][i])
                conns.append(c)
        print("===len conns:", len(conns), conns)
        # 协商子集的大小,单次
        set_data_size = count
        sub_set_size_list = [set_data_size]
        for c in conns:
            n_by = pickle.dumps(set_data_size)
            c.send_data(n_by)
        for c in conns:
            n_by = c.recv_data()
            n = pickle.loads(n_by)
            sub_set_size_list.append(n)
        for c in conns:
            c.close()
        # 降序排序
        sub_set_size_list.sort(reverse=True)
        print("===sub_set_size_list:", sub_set_size_list)
        # 取出最大的子集大小
        max_set_size = sub_set_size_list[0]
        # 存在一方的子集大小为0
        if 0 in sub_set_size_list:
            max_set_size = 0
            if self.p_id == 2:
                save_psi_id = pd.DataFrame({'id': []})
                save_psi_id.to_csv(str(self.p_id)+'_psi_'+str(cyc_n)+'.csv')
            return
        # self.dict_bucket_max_sub_set_size[self.keys[i]] = max_set_size
        set_data = list(bucket_id_df['id'])
        max_set_size_need = max_set_size
        if max_set_size < 100:
            # 也补全
            max_set_size_need = 100
            pass

        if set_data_size != max_set_size_need:
            # 补全
            pr_num = generate_random_bytes(16)
            src_id = set_data[0].encode('utf-8')
            for i in range(set_data_size, max_set_size_need):
                tmp_id = md5(src_id+pr_num+(str(i) + '_' +
                             str(self.p_id)).encode('utf-8')).hexdigest()
                set_data.append(tmp_id)
            print("===需补多少个:", max_set_size_need-set_data_size)
        tmp_df = pd.DataFrame({"id_with_pad": set_data})
        tmp_df['id_with_pad_bytes'] = tmp_df.applymap(
            lambda x: x.encode('utf-8'))
        if cyc_n == 0:
            print("=====tmp_df:::\n", tmp_df)
        set_data_for_psi = np.array(list(tmp_df['id_with_pad_bytes']))
        # 开始求交
        psi_id = []
        # index_1 = []
        # count_debug = 0
        port_array = get_port_array(self.n_parties, cyc_n, True)
        psi3_handle = PSI3(self.p_id, self.ip_array,
                           port_array, len(set_data_for_psi))
        # print("=========self.ip_array:", self.ip_array)
        psi_results = psi3_handle.psi3_process(set_data_for_psi)
        # count_debug = count_debug+len(psi_results)
        # self.psi_results_list.append(psi_results)
        print("++++++++++len psi_res:", len(psi_results))
        # return
        if len(psi_results) != 0:
            # tmp_df = pd.DataFrame(
            #     {"bucket_data": self.dict_bucket[self.keys[i]]})
            # 根据索引取出值(hash_id)
            psi_bucket_data_df = bucket_id_df.loc[psi_results]
            psi_id = list(psi_bucket_data_df['id'])
        if self.p_id == 2:
            # self.dfa_id['unique_index'] = self.dfa_id.index.tolist()
            # self.dfa_id.set_index('id', inplace=True)
            # psi3_id_result_all_df = self.dfa_id.loc[psi_id]
            # index_1 = list(psi3_id_result_all_df['unique_index'])
            # index_1.sort()
            # print('===========index_1::\n', index_1[:200], index_1[-200:])
            save_psi_id = pd.DataFrame({'id': psi_id})
            save_psi_id.to_csv(str(self.p_id)+'_psi_'+str(cyc_n)+'.csv')
        # print('=============psi num:', count_debug)
        pass

    def end_psi(self, id_name) -> tuple:
        psi_id_all = []
        all_num = 0
        if self.p_id == 2:
            for cyc_n in range(16):
                psi_id_df = self.__get_id_data_frame_path(
                    str(self.p_id)+'_psi_'+str(cyc_n)+'.csv')
                count = psi_id_df.shape[0]
                all_num = all_num+count
                psi_id_all = psi_id_all+list(psi_id_df['id'])
        print("====inter size:", all_num)
        cmd1 = 'rm -rf '+str(self.p_id)+'_psi_*'
        os.system(cmd1)
        if self.p_id == 2:
            self.dfa_id = self.__get_id_data_frame(id_name)  # 源文件
            # res_ok = list(self.dfa_id.loc[range(all_num), ['id']]['id'])

            self.dfa_id['unique_index'] = self.dfa_id.index.tolist()
            self.dfa_id.set_index(id_name, inplace=True)
            psi3_id_result_all_df = self.dfa_id.loc[psi_id_all]
            index_1 = list(psi3_id_result_all_df['unique_index'])
            index_1.sort()
            print('===========index_1::\n', index_1[:200], index_1[-200:])
            # print("======>>>>验证中：\n")
            # res_ok_set = set(res_ok)
            # psi_id_all_set = set(psi_id_all)
            # print("===res_ok_set:{},psi_id_all_set:{}".format(
            # len(res_ok_set), len(psi_id_all_set)))
            # inter = res_ok_set.intersection(psi_id_all_set)
            # print("===inter:{}".format(len(inter)))
            # for id in psi_id_all:
            #     if id not in res_ok:
            #         print("============error")
            #         # exit()
            #         pass
            # print("=======>>>psi3_id_index_result_all_df:\n",
            #   psi3_id_result_all_df)

        return index_1, psi_id_all

    def __get_id_data_frame_path(self, f_path):
        if self.is_debug:
            ls = ['']*self.set_size_debug
            # 交集数据
            for id in range(0, self.inter_size_debug):
                # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
                # ls[id] = md5(str(id).encode('utf-8')).hexdigest()[:16]
                ls[id] = md5(str(id).encode('utf-8')).hexdigest()
            print("====ls[0]:", ls[0], len(ls[0]))
            bn = generate_random_bytes(16)
            # 不同数据
            for id in range(self.inter_size_debug, self.set_size_debug):
                # ls[id] = md5((str(id) + 'qqq' + str(p_id)
                #               ).encode('utf-8')+bn).hexdigest()[:16]
                ls[id] = md5((str(id) + 'qqq' + str(p_id)
                              ).encode('utf-8')+bn).hexdigest()
            dfa_id = pd.DataFrame({"id": ls})
        else:
            dfa_id = pd.read_csv(
                f_path, dtype={'id': 'object'}, usecols=['id'])
        return dfa_id

    def __get_id_data_frame(self, id_name: str):
        if self.is_debug:
            # ls = ['']*self.set_size_debug
            # # 交集数据
            # for id in range(0, self.inter_size_debug):
            #     # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
            #     # ls[id] = md5(str(id).encode('utf-8')).hexdigest()[:16]
            #     ls[id] = md5(str(id).encode('utf-8')).hexdigest()
            # print("====ls[0]:", ls[0], len(ls[0]))
            # bn = generate_random_bytes(16)
            # # 不同数据
            # for id in range(self.inter_size_debug, self.set_size_debug):
            #     # ls[id] = md5((str(id) + 'qqq' + str(p_id)
            #     #               ).encode('utf-8')+bn).hexdigest()[:16]
            #     ls[id] = md5((str(id) + 'qqq' + str(p_id)
            #                   ).encode('utf-8')+bn).hexdigest()
            # dfa_id = pd.DataFrame({"id": ls})
            pass
        else:
            dfa_id = pd.read_csv(
                self.file_dir, dtype={id_name: 'object'}, usecols=[id_name])
        return dfa_id


def parse_args_psi3(argv):
    p_id, set_size, psi_n, file_dir, cmd, buctke_id = 0, 1000000, 30000, '', '', 0
    if len(argv[1:]) == 0:
        print('test.py --m <12> --i <3> --p <0>')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(
            argv[1:], None, ["b=", "c=", "m=", "p=", "i=", "help=", "f="])
    except getopt.GetoptError:
        print('test.py --m <12> --i <3> --p <0>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("--help"):
            print('test.py --m <12> --i <3> --p <0>')
            sys.exit()
        if opt in ('--c'):
            cmd = str(arg)
        if opt in ('--m'):
            set_size = int(arg)
        if opt in ('--p'):
            p_id = int(arg)
        if opt in ('--i'):
            psi_n = int(arg)
        if opt in ('--f'):
            file_dir = str(arg)
        if opt in ('--b'):
            buctke_id = int(arg)
    return p_id, set_size, psi_n, file_dir, cmd, buctke_id


def get_psi3_args():
    import argparse
    parser = argparse.ArgumentParser(description="run psi3 poc")
    parser.add_argument(
        "cmd",
        metavar="CMD",
        type=str,
        help="command",
    )
    parser.add_argument(
        "--inter",
        metavar="intersection size",
        type=int,
        default=3000,
        help="intersection size",
    )
    parser.add_argument(
        "--pid",
        metavar="party id",
        type=int,
        default=0,
        help="party id",
    )
    parser.add_argument(
        "--num",
        metavar="data number",
        type=int,
        default=1000000,
        help="data number",
    )
    parser.add_argument(
        "--in_file",
        metavar="data set file path",
        type=str,
        default="",
        help="data set file path",
    )
    parser.add_argument(
        "--bucket",
        metavar="bucket id",
        type=int,
        default=0,
        help="bucket id",
    )
    parser.add_argument(
        "--ip0",
        metavar="pid=0,ip",
        type=str,
        default="",
        help="pid=0,ip",
    )
    parser.add_argument(
        "--ip1",
        metavar="pid=1,ip",
        type=str,
        default="",
        help="pid=1,ip",
    )
    parser.add_argument(
        "--ip2",
        metavar="pid=2,ip",
        type=str,
        default="",
        help="pid=2,ip",
    )
    parser.add_argument(
        "--id",
        metavar="id name",
        type=str,
        default="",
        help="id name",
    )
    args = parser.parse_args()
    print(args)
    ip_array = [args.ip0, args.ip1, args.ip2]
    return ip_array, args.bucket, args.in_file, args.num, args.pid, args.inter, args.cmd, args.id


def get_use_time(start: float) -> float:
    return (time.time() - start) * 1000


def generate_random_bytes(n: int, byteorder='big'):
    if n <= 0:
        raise ValueError(f"illegal n: {n}")
    randi = random.SystemRandom().getrandbits(n * 8)
    return randi.to_bytes(n, byteorder)


def get_port_array(n_parties: int, cyc_n: int, is_psi3: bool):
    port_num = n_parties*(n_parties-1)/2
    ports_array = [[]]*n_parties
    offset = 12001
    if is_psi3:
        offset = 13001
    base = offset+n_parties*cyc_n
    # ports = [x for x in range(base, base+3)]
    for i in range(n_parties):
        tmp = [0]*n_parties
        for j in range(n_parties):
            if i < j:
                tmp[j] = base
                base = base+1
            elif i > j:
                tmp[j] = ports_array[j][i]
        ports_array[i] = tmp
    return ports_array


def id_column_encode(value):
    return str(value).encode('utf-8')


def psi_poc_test(p_id: int, file_dir: str):
    # 读取id
    dfa_id = pd.read_csv(file_dir, dtype={'id': 'object'}, usecols=['id'])
    count = dfa_id.shape[0]
    print("===count:", count)
    dfa_hash_id = dfa_id.applymap(lambda idr: id_column_encode(idr))
    dfr_id = dfa_hash_id.values.reshape(count)
    # return dfr_id

    ####
    dfa_id = pd.read_csv('../pid0.csv', dtype={'id': 'object'}, usecols=['id'])
    count = dfa_id.shape[0]
    print("===count:", count)


def psi3_set_size_test(p_id: int, set_size: int, psi_n: int):
    ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    port_array = [[0, 12001, 12002],
                  [12001, 0, 12003],
                  [12002, 12003, 0]]
    port_array = get_port_array(3, 1, False)
    print("===port_array:", port_array)
    conns = []
    for i in range(3):
        if i < p_id:
            c = Client(ip_array[i], port_array[p_id][i])
            conns.append(c)
            # c.recv_data
            pass
        elif i > p_id:
            c = Server(ip_array[p_id], port_array[p_id][i])
            # c.send_data
            # c.recv_data
            conns.append(c)
            pass
    print("len conns:", len(conns), conns)
    num = [set_size]
    for c in conns:
        n_by = pickle.dumps(set_size)
        c.send_data(n_by)

    for c in conns:
        n_by = c.recv_data()
        n = pickle.loads(n_by)
        num.append(n)
    for c in conns:
        c.close()
    print("num:", num)
    pass


# python3 psi3_exe.py  --m=20000000 --i=30000 --p=0 --f=../pid40w_0.csv
if __name__ == '__main__':
    # receiver_size, sender_size, psi_size, ip, port, omp_thread_num = parse_args(sys.argv)
    # print('receiver_size, sender_size, psi_size, ip, port=',
    #       receiver_size, sender_size, psi_size, ip, port, omp_thread_num)
    # p_id, set_size, psi_n, file_dir, cmd, buctke_id = parse_args_psi3(sys.argv)
    ip_array, bucket, in_file, num, pid, inter, cmd, id_name = get_psi3_args()
    print('ip_array, bucket, in_file, num, pid, inter, cmd,id_name=',
          ip_array, bucket, in_file, num, pid, inter, cmd, id_name)
    # psi3_process_test(p_id, set_size, psi_n)
    # psi3_set_size_test(p_id, set_size, psi_n)
    # ip_array = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
    # ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    # ip_array = ["10.100.3.51", "10.100.3.97", "10.100.3.98"]
    # ip_array_byte = [x.encode('utf-8') for x in ip_array]
    # ip_array = ["localhost", "localhost", "localhost"]
    is_debug = False
    if cmd == 'gen':
        ls = ['']*num
        # python3 psi3_batch.py gen --pid=2 --num=100000000 --inter=30000000 --id=id2
        # 交集数据
        for id in range(0, inter):
            # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
            # ls[id] = md5(str(id).encode('utf-8')).hexdigest()[:16]
            ls[id] = md5(str(id).encode('utf-8')).hexdigest()
        print("====ls[0]:", ls[0], len(ls[0]))
        bn = generate_random_bytes(16)
        # 不同数据
        for id in range(inter, num):
            # ls[id] = md5((str(id) + 'qqq' + str(p_id)
            #               ).encode('utf-8')+bn).hexdigest()[:16]
            ls[id] = md5((str(id) + 'qqq' + str(pid)
                          ).encode('utf-8')+bn).hexdigest()
        # 生成测试数据
        dfa_id = pd.DataFrame({id_name: ls})
        dfa_id.to_csv("./psi_test_"+str(pid)+'.csv')
    if cmd == 'init':
        # python3 psi3_batch.py init --pid=2 --in_file=../psi_1e_3kw_2.csv --id=id2
        psi3poc = Psi3PocCsv(pid, ip_array, in_file,
                             is_debug, num, inter)
        psi3poc.init_psi(id_name)
        pass
    if cmd == 'start':
        # python3 psi3_batch.py start --pid=2 --bucket=0 --ip0=10.100.3.51 --ip1=10.100.3.97 --ip2=10.100.3.98
        psi3poc = Psi3PocCsv(pid, ip_array, in_file,
                             is_debug, num, inter)
        psi3poc.start_psi(bucket)
        pass
    if cmd == 'end':
        # python3 psi3_batch.py --c=end --p=2 --f=../psi_1e_3kw_2.csv
        # python3 psi3_batch.py end --pid=2 --in_file=../psi_1e_3kw_2.csv --id=id2
        psi3poc = Psi3PocCsv(pid, ip_array, in_file,
                             is_debug, num, inter)
        psi_index, psi_result = psi3poc.end_psi(id_name)
        if pid == 2:
            df_res = pd.DataFrame({"id": psi_result})
            df_res.to_csv("psi_result_"+str(pid)+".csv")
        pass


# python3 psi3_exe.py  --m=20000000 --i=30000 --p=0 --f=../pid40w_0.csv
if __name__ == '__main__bak':
    # receiver_size, sender_size, psi_size, ip, port, omp_thread_num = parse_args(sys.argv)
    # print('receiver_size, sender_size, psi_size, ip, port=',
    #       receiver_size, sender_size, psi_size, ip, port, omp_thread_num)
    p_id, set_size, psi_n, file_dir, cmd, buctke_id = parse_args_psi3(sys.argv)
    print('p_id, set_size, psi_n,file_dir,cmd,buctke_id=',
          p_id, set_size, psi_n, file_dir, cmd, buctke_id)
    # psi3_process_test(p_id, set_size, psi_n)
    # psi3_set_size_test(p_id, set_size, psi_n)
    ip_array = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
    ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    ip_array = ["10.100.3.51", "10.100.3.97", "10.100.3.98"]
    # ip_array_byte = [x.encode('utf-8') for x in ip_array]
    # ip_array = ["localhost", "localhost", "localhost"]
    is_debug = False
    if cmd == 'gen':
        ls = ['']*set_size
        # python3 psi3_batch.py --c=gen --p=2 --m=100000000 --i=30000000
        # 交集数据
        for id in range(0, psi_n):
            # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
            # ls[id] = md5(str(id).encode('utf-8')).hexdigest()[:16]
            ls[id] = md5(str(id).encode('utf-8')).hexdigest()
        print("====ls[0]:", ls[0], len(ls[0]))
        bn = generate_random_bytes(16)
        # 不同数据
        for id in range(psi_n, set_size):
            # ls[id] = md5((str(id) + 'qqq' + str(p_id)
            #               ).encode('utf-8')+bn).hexdigest()[:16]
            ls[id] = md5((str(id) + 'qqq' + str(p_id)
                          ).encode('utf-8')+bn).hexdigest()
        dfa_id = pd.DataFrame({"id": ls})
        dfa_id.to_csv("../psi_1e_3kw_"+str(p_id)+'.csv')
    if cmd == 'init':
        # python3 psi3_batch.py --c=init --p=2 --f=../psi_1e_3kw_2.csv
        psi3poc = Psi3PocCsv(p_id, ip_array, file_dir,
                             is_debug, set_size, psi_n)
        psi3poc.init_psi()
        pass
    if cmd == 'start':
        # python3 psi3_batch.py --c=start --p=2 --b=0
        psi3poc = Psi3PocCsv(p_id, ip_array, file_dir,
                             is_debug, set_size, psi_n)
        psi3poc.start_psi(buctke_id)
        pass
    if cmd == 'end':
        # python3 psi3_batch.py --c=end --p=2 --f=../psi_1e_3kw_2.csv
        # python3 psi3_batch.py --c=end --p=2 --f=../psi_1e_3kw_2.csv
        psi3poc = Psi3PocCsv(p_id, ip_array, file_dir,
                             is_debug, set_size, psi_n)
        psi_index, psi_result = psi3poc.end_psi()
        if p_id == 2:
            df_res = pd.DataFrame(
                {"psi_res_id": psi_result, "psi_res_index": psi_index})
            df_res.to_csv("psi_all_"+str(p_id)+".csv")
        pass
    exit()
    for i in range(1):
        start = time.time()
        psi3poc = Psi3PocCsv(p_id, ip_array, file_dir,
                             is_debug, set_size, psi_n)
        psi_result, psi_index = psi3poc.get_psi3_ids_results()
        if is_debug == False and p_id == 2:
            df_res = pd.DataFrame(
                {"psi_res_id": psi_result, "psi_res_index": psi_index})
            df_res.to_csv("11_16_psi3_"+str(i)+".csv")
        print("=========psi3 process==========len:", len(psi_result))
        print("========i:{},use time:{}s".format(i, time.time()-start))
        time.sleep(3*60)
    time.sleep(20*60)
