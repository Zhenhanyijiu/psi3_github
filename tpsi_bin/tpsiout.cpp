
#include <iostream>
#include "Network/BtChannel.h"
#include "Network/BtEndpoint.h"

using namespace std;
#include "Common/Defines.h"
using namespace osuCrypto;

#include "OtBinMain.h"
#include "OtBinMain.v2.h"
#include "bitPosition.h"

#include <numeric>
#include "Common/Log.h"
#include "gbf.h"
#include "o1party.h"
#include "tpsi.h"
#include "psi3.h"
#include "tpsiout.h"
#include <stdio.h>
//int miraclTestMain();

int tpsi_process(u64_t p_idx, u64 n_parties, u64 threshold, u64_t set_size,
				 std::vector<std::vector<char>> ip_array,
				 std::vector<std::vector<u32_t>> port_array,
				 std::vector<std::vector<u8_t>> data_set,
				 std::vector<u64_t> *psi_results_output)
{
	// tpsi_party_fudata(pIdx, 3, 2, 10000, GbfOkvs, secSemiHonest);
	tpsi_party_fudata(p_idx, n_parties, threshold, set_size,
					  ip_array,
					  port_array,
					  data_set,
					  *psi_results_output,
					  GbfOkvs, secSemiHonest);
	return 0;
}

void usage(const char *argv0)
{
	std::cout << "Error! Please use:" << std::endl;
	std::cout << "\t 1. For unit test: " << argv0 << " -u" << std::endl;
	std::cout << "\t 2. For simulation (5 parties <=> 5 terminals): " << std::endl;
	;
	std::cout << "\t\t each terminal: " << argv0 << " -n 5 -t 2 -m 12 -p [pIdx]" << std::endl;
}
#ifdef TPSI_TEST
int main(int argc, char **argv)
{

	u64 pSetSize = 5, psiSecParam = 40, bitSize = 128;

	u64 setSize;

	u64 roundOPPRF;
	u64 nParties = 3;
	u64 threshold = 3;
	printf("======argc=:%d\n", argc);
	u64 pIdx = atoi(argv[1]);
	/////////////
	setSize = 100000;
	setSize = atoi(argv[2]);
	printf("===pIdx=%ld\n", pIdx);
	printf("===this is only %ld parties,size(%ld)\n", nParties, setSize);
	PRNG prngSame(_mm_set_epi32(4253465, 3434565, 234435, 23987045));
	PRNG prngDiff(_mm_set_epi32(434653, 23, pIdx, pIdx));
	u64 expected_intersection = 3000;
	expected_intersection = atoi(argv[3]);
	std::vector<std::vector<u8_t>> inputSet(setSize);
	if (pIdx == 0)
	{
		expected_intersection = expected_intersection - 100;
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
	}
	else if (pIdx == 1)
	{
		expected_intersection = expected_intersection - 200;
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
	}
	else
	{
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
	}
	char *IP_S[4] = {"127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"};
	std::vector<std::vector<char>> ip_arrary(nParties);
	for (int i = 0; i < nParties; i++)
	{
		ip_arrary[i].resize(32);
		memset(ip_arrary[i].data(), 0, 32);
		memcpy(ip_arrary[i].data(), IP_S[i], strlen(IP_S[i]));
	}
	printf("===>>ip set end\n");
	/////////////
	std::vector<u64_t> psiResultsOutput;
	// long start1 = start_time();
	vector<vector<u32_t>> port_array(nParties);
	for (int i = 0; i < nParties; i++)
	{
		port_array[i].resize(nParties);
		for (int j = 0; j <= i - 1; j++)
		{
			port_array[i][j] = port_array[j][i];
		}
		for (int j = i + 1; j < nParties; j++)
		{
			port_array[i][j] = 12000 + i + j;
		}
	}
	tpsi_process(pIdx, nParties, threshold, setSize,
				 ip_arrary,
				 port_array,
				 inputSet,
				 &psiResultsOutput);
	// long start1_end = get_use_time(start1);
	printf("===>>外层获取求交数据个数:%ld......\n",
		   psiResultsOutput.size());
	return 0;
	// switch (argc)
	// {

	// case 9: //tPSI
	// 	//cout << "9\n";
	// 	printf(">>>>>>>>>>>>>>>start");
	// 	if (argv[1][0] == '-' && argv[1][1] == 'm')
	// 		setSize = 1 << atoi(argv[2]);
	// 	else
	// 	{
	// 		cout << "setSize: wrong format\n";
	// 		usage(argv[0]);
	// 		return 0;
	// 	}

	// 	if (argv[3][0] == '-' && argv[3][1] == 'n')
	// 		nParties = atoi(argv[4]);
	// 	else
	// 	{
	// 		cout << "nParties: wrong format\n";
	// 		usage(argv[0]);
	// 		return 0;
	// 	}

	// 	if (argv[5][0] == '-' && argv[5][1] == 't')
	// 		tParties = atoi(argv[6]);
	// 	else
	// 	{
	// 		cout << "tParties: wrong format\n";
	// 		usage(argv[0]);
	// 		return 0;
	// 	}

	// 	if (argv[7][0] == '-' && argv[7][1] == 'p')
	// 	{
	// 		u64 pIdx = atoi(argv[8]);
	// 		//cout << setSize << " \t"  << nParties << " \t" << tParties << "\t" << pIdx << "\n";
	// 		//tpsi_party(pIdx, nParties, tParties, setSize, PaxosOkvs, secSemiHonest);
	// 		printf("============");
	// 		// tpsi_party(pIdx, nParties, tParties, setSize, SimulatedOkvs, secSemiHonest);
	// 	}
	// 	else
	// 	{
	// 		cout << "pIdx: wrong format\n";
	// 		usage(argv[0]);
	// 		return 0;
	// 	}

	// 	break;
	// }

	return 0;
}

#endif