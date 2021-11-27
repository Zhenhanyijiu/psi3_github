#ifndef __TPSIOUT_H__
#define __TPSIOUT_H__
typedef uint64_t u64_t;
// typedef block block_t;
typedef unsigned char u8_t;
// typedef unsigned int u32_t;
typedef uint32_t u32_t;
int tpsi_process(u64_t p_idx, u64_t set_size,
                 std::vector<std::vector<char>> ip_array,
                 std::vector<std::vector<u32_t>> port_array,
                 std::vector<std::vector<u8_t>> data_set,
                 std::vector<u64_t> *psi_results_output);
#endif