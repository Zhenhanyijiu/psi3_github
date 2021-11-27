
// #include <iostream>
// #include "Network/BtChannel.h"
// #include "Network/BtEndpoint.h"

using namespace std;
#include "Common/Defines.h"
using namespace osuCrypto;

// #include "OtBinMain.h"
// #include "OtBinMain.v2.h"
// #include "bitPosition.h"

// #include <numeric>
// #include "Common/Log.h"
// #include "gbf.h"
// #include "o1party.h"
// #include "tpsi.h"
#include "psi3.h"
#include "psi3out.h"
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>

int psi3_process(u64_t p_idx, u64_t set_size,
				 std::vector<std::vector<char>> ip_array,
				 std::vector<std::vector<u32_t>> port_array,
				 std::vector<std::vector<u8_t>> data_set,
				 std::vector<u64_t> *psi_results_output)
{
	// printf("===>>>>>#okvs:%d\n", PaxosOkvs);
	// printf("===>>>>>>#sec:%d\n", secMalicious);
	party_psi3_only(p_idx, set_size, ip_array, port_array, data_set,
					psi_results_output, PolyOkvs, secMalicious);
	return 0;
}
#ifdef TEST_PSI3
//时间统计us
long start_time()
{
	struct timeval start;
	gettimeofday(&start, NULL);
	return start.tv_sec * 1000000 + start.tv_usec;
}
long get_use_time(long start_time)
{
	struct timeval end;
	gettimeofday(&end, NULL);
	long usetime = end.tv_sec * 1000000 + end.tv_usec - start_time;
	return usetime / 1000;
}
void usage(const char *argv0)
{
	std::cout << "Error! Please use:" << std::endl;
	std::cout << "\t 1. For unit test: " << argv0 << " -u" << std::endl;
	std::cout << "\t 2. For simulation (5 parties <=> 5 terminals): " << std::endl;
	;
	std::cout << "\t\t each terminal: " << argv0 << " -n 5 -t 2 -m 12 -p [pIdx]" << std::endl;
}

int main(int argc, char **argv)
{

	// u64 pSetSize = 5, psiSecParam = 40, bitSize = 128;

	// u64 nParties, tParties, opt_basedOPPRF, setSize, isAug;

	// u64 roundOPPRF;
	u64 setSize;
	switch (argc)
	{
	case 5: //3psi
		if (argv[1][0] == '-' && argv[1][1] == 'm')
			setSize = atoi(argv[2]);
		else
		{
			cout << "setSize: wrong format\n";
			usage(argv[0]);
			return 0;
		}

		if (argv[3][0] == '-' && argv[3][1] == 'p')
		{
			u64 pIdx = atoi(argv[4]);
			//cout << setSize << " \t"  << nParties << " \t" << tParties << "\t" << pIdx << "\n";
			// party_psi3(pIdx, setSize, PaxosOkvs, secSemiHonest);
			// #define GbfOkvs 0
			// #define PolyOkvs 1
			// #define PaxosOkvs 2
			// #define	TableOPPRF 0

			// #define secMalicious 0
			// #define secSemiHonest 1
			printf("===this is only 3 parties,size(%ld)\n", setSize);
			PRNG prngSame(_mm_set_epi32(4253465, 3434565, 234435, 23987045));
			PRNG prngDiff(_mm_set_epi32(434653, 23, pIdx, pIdx));
			u64 expected_intersection = 30;
			std::vector<std::vector<u8_t>> inputSet(setSize);
			for (u64 i = 0; i < expected_intersection; ++i)
			{ // inputSet[i] = prngSame.get<block>();
				inputSet[i].resize(16);
				prngSame.get(inputSet[i].data(), 16);
			}

			for (u64 i = expected_intersection; i < setSize; ++i)
			{ // inputSet[i] = prngDiff.get<block>();
				inputSet[i].resize(16);
				prngDiff.get(inputSet[i].data(), 16);
			}
			char *IP_S[3] = {"127.0.0.1", "127.0.0.2", "127.0.0.3"};
			std::vector<std::vector<char>> ip_arrary(3);
			for (int i = 0; i < 3; i++)
			{
				ip_arrary[i].resize(32);
				memset(ip_arrary[i].data(), 0, 32);
				memcpy(ip_arrary[i].data(), IP_S[i], strlen(IP_S[i]));
			}
			printf("===>>ip set end\n");
			std::vector<u64_t> psiResultsOutput;
			long start1 = start_time();
			vector<vector<u32_t>> port_array(3);
			for (int i = 0; i < 3; i++)
			{
				port_array[i].resize(3);
				for (int j = 0; j <= i - 1; j++)
				{
					port_array[i][j] = port_array[j][i];
				}
				for (int j = i + 1; j < 3; j++)
				{
					port_array[i][j] = 12000 + i + j;
				}
			}
			psi3_process(pIdx, setSize, ip_arrary, port_array, inputSet, &psiResultsOutput);
			long start1_end = get_use_time(start1);
			printf("===>>外层获取求交数据个数:%ld......time:%dms\n", psiResultsOutput.size(), start1_end);
			// for (u64 i = 0; i < psiResultsOutput.size(); ++i)
			// {
			// 	// std::cout << recv.mIntersection[i] << " - " << inputSet[recv.mIntersection[i]] << std::endl;
			// 	std::cout << psiResultsOutput[i] << " - " << ((block *)(inputSet[psiResultsOutput[i]].data()))[0] << std::endl;
			// }

		}
		else
		{
			cout << "pIdx: wrong format\n";
			usage(argv[0]);
			return 0;
		}
		break;
	}

	return 0;
}

#endif