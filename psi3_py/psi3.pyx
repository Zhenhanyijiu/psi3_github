# cython:language_level=3
from libcpp.vector cimport vector
from libc cimport string
from libc.stdio cimport printf
import numpy as np
import time


# from libcpp.string cimport string as cppstr
# cdef extern from "Python.h":
#     ctypedef struct PyObject:
#         pass
#     long Py_REFCNT(PyObject *)


# cdef extern from "psi3out.h" namespace "osuCrypto":
cdef extern from "psi3out.h":
    ctypedef unsigned long long u64_t
    ctypedef unsigned char u8_t
    ctypedef unsigned int u32_t
    # cdef cppclass PsiSender:
    #     PsiSender()except+
    #     int init(u8_t *commonSeed, u64_t senderSize, u64_t matrixWidth, u64_t logHeight,
    #              int threadNum, u64_t hash2LengthInBytes, u64_t bucket2ForComputeH2Output)
    #     int genPublicParamFromNpot(u8_t ** pubParamBuf, u64_t *pubParamBufByteSize)
    #     int genMatrixTxorRBuff(u8_t *pk0Buf, const u64_t pk0BufSize,
    #                            u8_t ** uBuffOutputTxorR, u64_t *uBuffOutputSize)
    #     int computeAllHashOutputByH1(const vector[vector[u8_t]] senderSet)
    #     int recoverMatrixC(const u8_t *recvMatrixADBuff, const u64_t recvMatixADBuffSize)
    #     int isSendEnd()
    #     int computeHashOutputToReceiverOnce(u8_t ** sendBuff, u64_t *sendBuffSize)

    # cdef cppclass PsiReceiver:
    #     PsiReceiver()except+
    #     int init(u8_t *commonSeed, u64_t receiverSize, u64_t senderSize, u64_t matrixWidth,
    #              u64_t logHeight, int threadNum, u64_t hash2LengthInBytes,
    #              u64_t bucket2ForComputeH2Output)
    #     int genPK0FromNpot(u8_t *pubParamBuf, const u64_t pubParamBufByteSize,
    #                        u8_t ** pk0Buf, u64_t *pk0BufSize)
    #     int getSendMatrixADBuff(const u8_t *uBuffInputTxorR, const u64_t uBuffInputSize,
    #                             const vector[vector[u8_t]] receiverSet,
    #                             u8_t ** sendMatrixADBuff, u64_t *sendMatixADBuffSize)
    #     int genenateAllHashesMap()
    #     int isRecvEnd()
    #     # int recvFromSenderAndComputePSIOnce(const u8_t *recvBuff, const u64_t recvBufSize,
    #     #                                     vector[u32_t] *psiMsgIndex)
    #     int recvFromSenderAndComputePSIOnce(const u8_t *recvBuff, const u64_t recvBufSize)
    #     int getPsiResultsForAll(vector[u32_t] *psiResultsOutput)
    ###集成socket oprf-psi ,单独提供出来
    # int oprf_psi_receiver_process(u64_t receiverSize, u64_t senderSize, char*address,
    #                               int port, u8_t *commonSeed, u64_t matrixWidth,
    #                               u64_t logHeight, u64_t hash2LengthInBytes,
    #                               u64_t bucket2ForComputeH2Output, int omp_num,
    #                               vector[vector[u8_t]] receiver_set,
    #                               vector[u32_t] *psiResultsOutput)
    # int oprf_psi_sender_process(u64_t receiverSize, u64_t senderSize, char*address,
    #                             int port, u8_t *commonSeed, u64_t matrixWidth,
    #                             u64_t logHeight, u64_t hash2LengthInBytes,
    #                             u64_t bucket2ForComputeH2Output, int omp_num,
    #                             vector[vector[u8_t]] sender_set)
    # int psi3_process(u64_t pIdx, u64_t setSize)
    int psi3_process(u64_t p_idx, u64_t set_size,
                     vector[vector[char]] ip_array,
                     vector[vector[u32_t]] port_array,
                     vector[vector[u8_t]] data_set,
                     vector[u64_t] *psi_results_output)

def psi3_process_by_boost(p_idx: int, set_size: int, ip_array: list,
                          port_array: list, data_set: np.array):
    if len(ip_array) != 3:
        raise Exception('psi3_process_by_boost: error,len(ip_array)!=3')
    cdef vector[vector[char]] ip_array_c = <vector[vector[char]]> ip_array
    cdef vector[vector[u32_t]] port_array_c = <vector[vector[u32_t]]> port_array
    cdef vector[vector[u8_t]] data_set_c = <vector[vector[u8_t]]> data_set
    cdef vector[u64_t] psi_results
    cdef ret = psi3_process(p_idx, set_size, ip_array_c, port_array_c, data_set_c, &psi_results)
    if ret != 0:
        raise Exception('psi3_process_by_boost: error')
    return <list> psi_results

#Opef psi receiver
# cdef class OprfPsiReceiver:
#     cdef PsiReceiver psi_receiver
#     #common_seed:16字节的bytes，双方必须做到统一
#     def __init__(self, common_seed: bytes, receiver_size: int, sender_size: int,
#                  omp_thread_num: int = 1, matrix_width: int = 128):
#         if common_seed is None or len(common_seed) < 16:
#             raise Exception('oprf psi receiver: param error')
#         cdef int ret = self.psi_receiver.init(common_seed, receiver_size, sender_size, matrix_width,
#                                               20, omp_thread_num, 10, 10240)
#         if ret != 0:
#             raise Exception('oprf psi receiver: init error')
#
#     def gen_pk0s(self, public_param: bytes):
#         cdef u64_t pubParamBufByteSize = len(public_param)
#         cdef u8_t *pk0s
#         cdef u64_t pk0BufSize
#         cdef int ret = self.psi_receiver.genPK0FromNpot(public_param, pubParamBufByteSize, &pk0s, &pk0BufSize)
#         if ret != 0:
#             raise Exception('oprf psi receiver: generate pk0s error')
#         pk0s_val = bytes(pk0BufSize)
#         string.memcpy(<u8_t*> pk0s_val, pk0s, pk0BufSize)
#         return pk0s_val, pk0BufSize
#
#     def gen_matrix_A_xor_D(self, matrix_TxorR: bytes, receiver_set: np.array):
#         cdef u64_t uBuffInputSize = len(matrix_TxorR)
#         cdef u8_t *matrix_AxorD_buff
#         cdef u64_t matrix_AxorD_buff_size
#         start = time.time()
#         cdef vector[vector[u8_t]] receiverSet = <vector[vector[u8_t]]> receiver_set
#         end = time.time()
#         print('===>>循环赋值recvset用时:{}s'.format(end - start))
#         cdef int ret = self.psi_receiver.getSendMatrixADBuff(matrix_TxorR, uBuffInputSize, receiverSet,
#                                                              &matrix_AxorD_buff, &matrix_AxorD_buff_size)
#         if ret != 0:
#             raise Exception('oprf psi receiver: generate matrix A_xor_D error')
#         matrix_AxorD_val = bytes(matrix_AxorD_buff_size)
#         start = time.time()
#         string.memcpy(<u8_t*> matrix_AxorD_val, matrix_AxorD_buff, matrix_AxorD_buff_size)
#         end = time.time()
#         print('===>>matrix_AxorD_val memcpy用时:{}s'.format(end - start))
#         return matrix_AxorD_val, matrix_AxorD_buff_size
#
#     def gen_all_hash2_map(self):
#         cdef int ret = self.psi_receiver.genenateAllHashesMap()
#         if ret != 0:
#             raise Exception('oprf psi receiver: generate all hash2 output map error')
#
#     def is_receiver_end(self)-> bool:
#         cdef int ret = self.psi_receiver.isRecvEnd()
#         if ret == 1:
#             return True
#         return False
#
#     # def compute_psi_by_hash2_output(self, hash2_from_sender: bytes)-> list:
#     #     cdef u64_t recvBufSize = len(hash2_from_sender)
#     #     cdef vector[u32_t] psi_msg_index
#     #     cdef int ret = self.psi_receiver.recvFromSenderAndComputePSIOnce(hash2_from_sender, recvBufSize, &psi_msg_index)
#     #     if ret != 0:
#     #         raise Exception('oprf psi receiver: compute psi by hash2 output from sender error')
#     #     return <list> psi_msg_index
#     def compute_psi_by_hash2_output(self, hash2_from_sender: bytes):
#         cdef u64_t recvBufSize = len(hash2_from_sender)
#         # cdef vector[u32_t] psi_msg_index
#         cdef int ret = self.psi_receiver.recvFromSenderAndComputePSIOnce(hash2_from_sender, recvBufSize)
#         if ret != 0:
#             raise Exception('oprf psi receiver: compute psi by hash2 output from sender error')
#     #int getPsiResultsForAll(vector[u32_t] *psiResultsOutput)
#     def get_psi_results_for_all(self)-> list:
#         cdef vector[u32_t] psi_results_output
#         cdef int ret = self.psi_receiver.getPsiResultsForAll(&psi_results_output)
#         if ret != 0:
#             raise Exception('oprf psi receiver: get psi results  error')
#         return <list> psi_results_output

# #Oprf psi sender
# cdef class OprfPsiSender(object):
#     cdef PsiSender psi_sender
#     #common_seed:16字节的bytes，双方必须做到统一
#     def __init__(self, common_seed: bytes, sender_size: int, omp_thread_num: int = 1,
#                  matrix_width: int = 128):
#         if common_seed is None or len(common_seed) < 16:
#             raise Exception('oprf psi sender: param error')
#         cdef int ret = self.psi_sender.init(common_seed, sender_size, matrix_width, 20,
#                                             omp_thread_num, 10, 10240)
#         if ret != 0:
#             raise Exception('oprf psi sender: init error')
#
#     def gen_public_param(self):
#         cdef u8_t *pub_param
#         cdef u64_t pub_param_byte_size
#         cdef int ret = self.psi_sender.genPublicParamFromNpot(&pub_param, &pub_param_byte_size)
#         if ret != 0:
#             raise Exception('oprf psi sender: generate public param error')
#         print('===>>public_param:', pub_param)
#         pub_param_val = bytes(pub_param_byte_size)
#         string.memcpy(<u8_t*> pub_param_val, pub_param, pub_param_byte_size)
#         return pub_param_val, pub_param_byte_size
#
#     def gen_matrix_T_xor_R(self, pk0s: bytes):
#         cdef u64_t pk0BufSize = len(pk0s)
#         cdef u8_t *uBuffOutputTxorR
#         cdef u64_t uBuffOutputSize
#         cdef int ret = self.psi_sender.genMatrixTxorRBuff(pk0s, pk0BufSize, &uBuffOutputTxorR, &uBuffOutputSize)
#         if ret != 0:
#             raise Exception('oprf psi sender: generate matrix T_xor_R error')
#         T_xor_R = bytes(uBuffOutputSize)
#         string.memcpy(<u8_t*> T_xor_R, uBuffOutputTxorR, uBuffOutputSize)
#         return T_xor_R, uBuffOutputSize
#
#     def compute_all_hash_output_by_H1(self, sender_set: np.array):
#         cdef vector[vector[u8_t]] senderSet = <vector[vector[u8_t]]> sender_set
#         cdef int ret = self.psi_sender.computeAllHashOutputByH1(senderSet)
#         if ret != 0:
#             raise Exception('oprf psi sender: recover matrix_C error')
#
#     def recover_matrix_C(self, recv_matrix_A_xor_D: bytes):
#         cdef u64_t recvMatixADBuffSize = len(recv_matrix_A_xor_D)
#         cdef int ret = self.psi_sender.recoverMatrixC(recv_matrix_A_xor_D, recvMatixADBuffSize)
#         if ret != 0:
#             raise Exception('oprf psi sender: recover matrix_C error')
#
#     def is_sender_end(self)-> bool:
#         cdef int ret = self.psi_sender.isSendEnd()
#         if ret == 1:
#             return True
#         return False
#
#     def compute_hash2_output_to_receiver(self)-> tuple:
#         # hash2_output_val = bytes(102400)
#         # cdef u8_t *hash2_output_buff = hash2_output_val
#         cdef u8_t *hash2_output_buff
#         cdef u64_t hash2_output_buff_size
#         cdef int ret = self.psi_sender.computeHashOutputToReceiverOnce(&hash2_output_buff, &hash2_output_buff_size)
#         if ret != 0:
#             raise Exception('oprf psi sender: compute hash2 output error')
#         hash2_output_val = bytes(hash2_output_buff_size)
#         string.memcpy(<u8_t*> hash2_output_val, hash2_output_buff, hash2_output_buff_size)
#         # return hash2_output_buff[:hash2_output_buff_size], hash2_output_buff_size
#         return hash2_output_val, hash2_output_buff_size

# 带有socket的oprf-psi 接收端接口
# def oprf_psi_receiver_by_socket(receiverSize: int, senderSize: int, receiver_set: np.array,
#                                 address: bytes, port: int, commonSeed: bytes, omp_num: int = 1,
#                                 bucket2ForComputeH2Output: int = 10240, matrixWidth: int = 128,
#                                 logHeight: int = 20, hash2LengthInBytes: int = 10)-> list:
#     if receiverSize != len(receiver_set):
#         raise Exception('oprf_psi_receiver_process:receiverSize!=len(receiver_set) error')
#     cdef vector[u32_t] psiResultsOutput
#     start0 = time.time()
#     cdef vector[vector[u8_t]] receiverSet = <vector[vector[u8_t]]> receiver_set
#     print("###类型转换用时:{}s".format(time.time() - start0))
#     cdef ret = oprf_psi_receiver_process(receiverSize, senderSize, address, port,
#                                          commonSeed, matrixWidth, logHeight,
#                                          hash2LengthInBytes, bucket2ForComputeH2Output,
#                                          omp_num, receiverSet, &psiResultsOutput)
#     if ret != 0:
#         raise Exception('oprf_psi_receiver_process: error')
#     return <list> psiResultsOutput
#
# # 带有socket的oprf-psi 发送端接口
# def oprf_psi_sender_by_socket(senderSize: int, sender_set: np.array,
#                               address: bytes, port: int, commonSeed: bytes, omp_num: int = 1,
#                               bucket2ForComputeH2Output: int = 10240, matrixWidth: int = 128,
#                               logHeight: int = 20, hash2LengthInBytes: int = 10):
#     if senderSize != len(sender_set):
#         raise Exception('oprf_psi_sender_process:senderSize != len(sender_set) error')
#     cdef vector[vector[u8_t]] senderSet = <vector[vector[u8_t]]> sender_set
#     receiverSize = 0
#     cdef ret = oprf_psi_sender_process(receiverSize, senderSize, address, port,
#                                        commonSeed, matrixWidth, logHeight,
#                                        hash2LengthInBytes, bucket2ForComputeH2Output,
#                                        omp_num, senderSet)
#     if ret != 0:
#         raise Exception('oprf_psi_sender_process: error')
