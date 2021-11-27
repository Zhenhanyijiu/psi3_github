from tpsi import psi3_process_by_boost
import numpy as np
from hashlib import sha256, md5
import sys
import getopt
import time
import random
import pandas as pd
import socket


def parse_args_psi3(argv):
    p_id, set_size, psi_n = 0, 1000000, 30000
    if len(argv[1:]) == 0:
        print('test.py --m <12> --i <3> --p <0>')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(
            argv[1:], None, ["m=", "p=", "i=", "help="])
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

    return p_id, set_size, psi_n


def get_use_time(start: float) -> float:
    return (time.time() - start) * 1000


def generate_random_bytes(n: int, byteorder='big'):
    if n <= 0:
        raise ValueError(f"illegal n: {n}")
    randi = random.SystemRandom().getrandbits(n * 8)
    return randi.to_bytes(n, byteorder)


def psi3_process_test(p_id: int, set_size: int, psi_n: int):
    ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    # ip_array = ["10.100.3.15", "10.100.3.15", "10.100.3.16"]
    ip_array_byte = [x.encode('utf-8') for x in ip_array]
    print("===========ip_array_byte:", ip_array_byte)

    # 测试数据生成
    # psi_n = 6000000
    ls = [b''] * set_size
    print("===>>set_size:", set_size)
    print("===>>psi_n   :", psi_n)
    for i in range(0, psi_n):
        # ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')
        ls[i] = md5(str(i).encode('utf-8')).digest()
    print("====ls[0]:", ls[0], len(ls[0]))
    bn = generate_random_bytes(16)
    for i in range(psi_n, set_size):
        # ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')
        #             ).hexdigest()[:16].encode('utf-8')
        ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')+bn).digest()
    port_array = [[0, 12001, 12002],
                  [12001, 0, 12003],
                  [12002, 12003, 0]]
    # df = pd.read_csv("../pid40w_"+str(p_id)+".csv",
    #                  dtype={'id': 'object'}, usecols=['id'])
    df = pd.read_csv("t25059_"+str(p_id)+".csv",
                     dtype={'id': 'object'}, usecols=['id'])
    print('==============df:\n', df)
    ls2 = list(df['id'])
    print("==============ls2[0]len:", len(ls2[0]))
    ls = [bytes.fromhex(x) for x in ls2]
    print("==============lenls:", len(ls[0]))
    # return
    set_size = len(ls)
    psi_results = psi3_process_by_boost(
        p_id, set_size, ip_array_byte, port_array, np.array(ls))
    print("===>>psi_result:", psi_results[:300], "num:", len(psi_results))


if __name__ == '__main__':
    # receiver_size, sender_size, psi_size, ip, port, omp_thread_num = parse_args(sys.argv)
    # print('receiver_size, sender_size, psi_size, ip, port=',
    #       receiver_size, sender_size, psi_size, ip, port, omp_thread_num)
    p_id, set_size, psi_n = parse_args_psi3(sys.argv)
    print('p_id, set_size, psi_n=', p_id, set_size, psi_n)
    psi3_process_test(p_id, set_size, psi_n)
    print("=========psi3 process==========")
