from psi3 import psi3_process_by_boost
import numpy as np
from hashlib import sha256, md5
import sys
import getopt
import time
import random
import socket
import pickle
import pandas as pd


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


class Psi3Poc(object):
    def __init__(self, p_id: int, ip_array: list, file_dir: str):
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
        # self.psi_results_list = []

    def __get_max_sub_set_data_size(self):
        port_array = get_port_array(self.n_parties, 6, False)
        # print("===i:{},port_array:{}\n".format(1, port_array))
        conns = []
        # ip_array = [x.decode('utf-8') for x in self.ip_array]
        # 建立连接
        for i in range(self.n_parties):
            if i < self.p_id:
                c = Client(ip_array[i], port_array[self.p_id][i])
                conns.append(c)
            elif i > self.p_id:
                c = Server(ip_array[self.p_id], port_array[self.p_id][i])
                conns.append(c)
        print("===len conns:", len(conns), conns)
        # 协商子集的大小
        for i in range(16):
            set_data_size = self.dict_bucket_lens[self.keys[i]]
            sub_set_size_list = [set_data_size]
            for c in conns:
                n_by = pickle.dumps(set_data_size)
                c.send_data(n_by)
            for c in conns:
                n_by = c.recv_data()
                n = pickle.loads(n_by)
                sub_set_size_list.append(n)
            # 降序排序
            sub_set_size_list.sort(reverse=True)
            print("===sub_set_size_list:", sub_set_size_list)
            # 取出最大的子集大小
            max_set_size = sub_set_size_list[0]
            # 存在一方的子集大小为0
            if 0 in sub_set_size_list:
                max_set_size = 0
            self.dict_bucket_max_sub_set_size[self.keys[i]] = max_set_size
        for c in conns:
            c.close()

    # 分成16个子集,分桶
    def __get_key_list_dict(self):
        dfa_id = pd.read_csv(
            self.file_dir, dtype={'id': 'object'}, usecols=['id'])
        count = dfa_id.shape[0]
        print("===count:", count)
        # 加一列，hash_id
        dfa_id['hash_id'] = dfa_id.applymap(
            lambda x: md5(x.encode('utf-8')).digest())
        # 加一列,用于分桶的标志
        dfa_id['hash_id_key'] = dfa_id['hash_id'].apply(divide_to_16iterms)
        # 加一列，索引列
        dfa_id['unique_index'] = dfa_id.index.tolist()
        # dfa_id['hash_id_len'] = dfa_id['hash_id'].apply(lambda x: len(x))
        n = 0
        # 分成16类
        for key in self.keys:
            # 把等于某个key的hash_id取出来,成list
            key_df = dfa_id.loc[dfa_id['hash_id_key'] == key]
            # lst1 = list(key_df["hash_id"]),将这些id分成一桶
            lst1 = list(key_df["id"])  # 字符串类型
            n = n+len(lst1)
            self.dict_bucket[key] = lst1
            self.dict_bucket_lens[key] = len(lst1)
            print('===每桶的个数:', len(lst1))
        self.dfa_id = dfa_id
        print('===>>id_num_all:', n)
        # print('===>>self.dfa_id:\n', self.dfa_id)
        self.__get_max_sub_set_data_size()

    # 对每个子集求交，并协商大小,并返回子集
    def __get_common_set_size_and_padd_set_data(self, cyc_n: int) -> np.array:
        # 本节点的某个子集
        set_data = self.dict_bucket[self.keys[cyc_n]]
        # 本节点的某个子集大小
        set_data_size = self.dict_bucket_lens[self.keys[cyc_n]]
        # 取出最大的某个子集大小
        max_set_size = self.dict_bucket_max_sub_set_size[self.keys[cyc_n]]
        if max_set_size == 0:
            return np.array([])
        if set_data_size != max_set_size:
            # 补全
            pr_num = generate_random_bytes(16)
            src_id = set_data[0].encode('utf-8')
            for i in range(set_data_size, max_set_size):
                tmp_id = md5(src_id+pr_num+(str(i) + '_' +
                             str(self.p_id)).encode('utf-8')).hexdigest()
                set_data.append(tmp_id)
            print("===需补多少个:", max_set_size-set_data_size)
        tmp_df = pd.DataFrame({"id_with_pad": set_data})
        tmp_df['id_with_pad_bytes'] = tmp_df.applymap(
            lambda x: x.encode('utf-8'))
        if cyc_n == 0:
            print("=====tmp_df_1:::\n", tmp_df)

        return np.array(list(tmp_df['id_with_pad_bytes']))

    def get_psi3_ids_results_bak(self) -> tuple:
        self.__get_key_list_dict()
        # conns = self.tcp_conn_list()
        ret = ([], [])
        psi_hash_id = []
        for i in range(16):
            set_data = self.__get_common_set_size_and_padd_set_data(i)
            if len(set_data) == 0:
                # self.psi_results_list.append([])
                continue
            port_array = get_port_array(self.n_parties, i, True)
            psi3_handle = PSI3(self.p_id, self.ip_array,
                               port_array, len(set_data))
            print("=========self.ip_array:", self.ip_array)
            psi_results = psi3_handle.psi3_process(set_data)
            # self.psi_results_list.append(psi_results)
            tmp_df = pd.DataFrame(
                {"bucket_data": self.dict_bucket[self.keys[i]]})
            # 根据索引取出值(hash_id)
            psi_bucket_data_df = tmp_df.loc[psi_results]
            psi_hash_id = psi_hash_id+list(psi_bucket_data_df['bucket_data'])
        self.dfa_id.set_index('hash_id', inplace=True)
        psi3_id_result_all_df = self.dfa_id.loc[psi_hash_id]
        ret[0] = list(psi3_id_result_all_df['unique_index'])
        ret[1] = list(psi3_id_result_all_df['id'])
        return ret

    def get_psi3_ids_results(self) -> list:
        self.__get_key_list_dict()
        # conns = self.tcp_conn_list()
        # ret = ([], [])
        # ret = []
        psi_id = []
        count_debug = 0
        for i in range(16):
            print("========================\n========================\n")
            print('==============第{}分桶===================\n'.format(i))
            set_data = self.__get_common_set_size_and_padd_set_data(i)
            # len_set_iterm = [len(x) for x in set_data]
            # print(">>>>>>>>>>\n", len(set_data[0]), len(len_set_iterm))
            # set_data_hex = [x.hex() for x in set_data]
            # print(">>>>>>>>>>hex:", len(set_data_hex[0]), len(set_data_hex))
            # dff = pd.DataFrame({"id": set_data_hex})
            # dff.to_csv("t25059_"+str(self.p_id)+".csv")
            # return
            ###############
            # ls = [b'']*25059
            # for id in range(0, 3000):
            #     # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
            #     ls[id] = md5(str(id).encode('utf-8')).digest()
            # print("====ls[0]:", ls[0], len(ls[0]))
            # bn = generate_random_bytes(16)
            # for id in range(3000, 25059):
            #     ls[id] = md5((str(id) + 'qqq' + str(p_id)
            #                   ).encode('utf-8')+bn).digest()
            # set_data = np.array(ls)
            ###############
            if len(set_data) == 0:
                # self.psi_results_list.append([])
                continue
            port_array = get_port_array(self.n_parties, i, True)
            psi3_handle = PSI3(self.p_id, self.ip_array,
                               port_array, len(set_data))
            print("=========self.ip_array:", self.ip_array)
            psi_results = psi3_handle.psi3_process(set_data)
            count_debug = count_debug+len(psi_results)
            # self.psi_results_list.append(psi_results)
            # print("++++++++++len psi_res:", len(psi_results))
            # return
            if len(psi_results) != 0:
                tmp_df = pd.DataFrame(
                    {"bucket_data": self.dict_bucket[self.keys[i]]})
                # 根据索引取出值(hash_id)
                psi_bucket_data_df = tmp_df.loc[psi_results]
                psi_id = psi_id+list(psi_bucket_data_df['bucket_data'])
        if self.p_id == 2:
            self.dfa_id.set_index('id', inplace=True)
            psi3_id_result_all_df = self.dfa_id.loc[psi_id]
            index_1 = list(psi3_id_result_all_df['unique_index'])
            index_1.sort()
            print('===========index_1::\n', index_1[:200])
        print('=============psi num:', count_debug)
        return psi_id


def parse_args_psi3(argv):
    p_id, set_size, psi_n, file_dir = 0, 1000000, 30000, ''
    if len(argv[1:]) == 0:
        print('test.py --m <12> --i <3> --p <0>')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(
            argv[1:], None, ["m=", "p=", "i=", "help=", "f="])
    except getopt.GetoptError:
        print('test.py --m <12> --i <3> --p <0>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("--help"):
            print('test.py --m <12> --i <3> --p <0>')
            sys.exit()
        if opt in ('--m'):
            set_size = int(arg)
        if opt in ('--p'):
            p_id = int(arg)
        if opt in ('--i'):
            psi_n = int(arg)
        if opt in ('--f'):
            file_dir = str(arg)

    return p_id, set_size, psi_n, file_dir


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

# def psi3_process_test(p_id: int, set_size: int, psi_n: int):
#     # ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
#     ip_array = ["10.100.3.15", "10.100.3.15", "10.100.3.16"]
#     ip_array_byte = [x.encode('utf-8') for x in ip_array]
#     # 测试数据生成
#     # psi_n = 6000000
#     ls = [b''] * set_size
#     print("===>>set_size:", set_size)
#     print("===>>psi_n   :", psi_n)
#     for i in range(0, psi_n):
#         # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
#         ls[i] = md5(str(i).encode('utf-8')).digest()
#     print("====ls[0]:", ls[0], len(ls[0]))
#     bn = generate_random_bytes(16)
#     for i in range(psi_n, set_size):
#         # ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')
#         #             ).hexdigest()[:16].encode('utf-8')
#         ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')+bn).digest()
#     port_array = [[0, 12001, 12002],
#                   [12001, 0, 12003],
#                   [12002, 12003, 0]]
#     psi_results = psi3_process_by_boost(
#         p_id, set_size, ip_array_byte, port_array, np.array(ls))
#     print("===>>psi_result:", psi_results[:300], "num:", len(psi_results))


# python3 psi3_exe.py  --m=20000000 --i=30000 --p=0 --f=../pid40w_0.csv
if __name__ == '__main__':
    # receiver_size, sender_size, psi_size, ip, port, omp_thread_num = parse_args(sys.argv)
    # print('receiver_size, sender_size, psi_size, ip, port=',
    #       receiver_size, sender_size, psi_size, ip, port, omp_thread_num)
    p_id, set_size, psi_n, file_dir = parse_args_psi3(sys.argv)
    print('p_id, set_size, psi_n,file_dir=', p_id, set_size, psi_n, file_dir)
    # psi3_process_test(p_id, set_size, psi_n)
    # psi3_set_size_test(p_id, set_size, psi_n)
    ip_array = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
    ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    ip_array = ["10.100.3.51", "10.100.3.97", "10.100.3.98"]
    # ip_array_byte = [x.encode('utf-8') for x in ip_array]
    # ip_array = ["localhost", "localhost", "localhost"]
    psi3poc = Psi3Poc(p_id, ip_array, file_dir)
    psi_result = psi3poc.get_psi3_ids_results()
    print("=========psi3 process==========len:", len(psi_result))
