from psi3 import psi3_process_by_boost
import numpy as np
from hashlib import sha256, md5
import sys
import getopt
import time
import socket


def parse_args_psi3(argv):
    p_id, set_size = 0, 12
    if len(argv[1:]) == 0:
        print('test.py --m <12> --p <0>')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(
            argv[1:], None, ["m=", "p=", "help="])
    except getopt.GetoptError:
        print('test.py --m <12> --p <0>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("--help"):
            print('test.py --m <12> --p <0>')
            sys.exit()
        if opt in ('--m'):
            set_size = int(arg)
        if opt in ('--p'):
            p_id = int(arg)

    return p_id, set_size


def get_use_time(start: float) -> float:
    return (time.time() - start) * 1000


def psi3_process_test(p_id: int, set_size: int):
    ip_array = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    ip_array_byte = [x.encode('utf-8') for x in ip_array]
    # 测试数据生成
    psi_n = 300
    ls = [b''] * set_size
    print("===>>set_size:", set_size)
    for i in range(0, psi_n):
        ls[i] = md5(str(i).encode('utf-8')).hexdigest()[:16].encode('utf-8')

    for i in range(psi_n, set_size):
        ls[i] = md5((str(i) + 'qqq' + str(p_id)).encode('utf-8')).hexdigest()[:16].encode('utf-8')
    port_array = [[0, 12001, 12002],
                  [12001, 0, 12003],
                  [12002, 12003, 0]]
    psi_results = psi3_process_by_boost(p_id, set_size, ip_array_byte, port_array, np.array(ls))
    print("===>>psi_result:", psi_results, len(psi_results))


if __name__ == '__main__':
    # receiver_size, sender_size, psi_size, ip, port, omp_thread_num = parse_args(sys.argv)
    # print('receiver_size, sender_size, psi_size, ip, port=',
    #       receiver_size, sender_size, psi_size, ip, port, omp_thread_num)
    p_id, set_size = parse_args_psi3(sys.argv)
    print('p_id, set_size=', p_id, set_size)
    psi3_process_test(p_id, set_size)
    print("=========psi3 process==========")
