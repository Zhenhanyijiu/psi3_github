
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

int tpsi_process(u64_t p_idx, u64_t set_size,
				 std::vector<std::vector<char>> ip_array,
				 std::vector<std::vector<u32_t>> port_array,
				 std::vector<std::vector<u8_t>> data_set,
				 std::vector<u64_t> *psi_results_output)
{
	// tpsi_party_fudata(pIdx, 3, 2, 10000, SimulatedOkvs, secSemiHonest);
	tpsi_party_fudata(p_idx, 3, 2, set_size,
					  ip_array,
					  port_array,
					  data_set,
					  *psi_results_output,
					  SimulatedOkvs, secSemiHonest);
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

	u64 nParties, tParties, opt_basedOPPRF, setSize, isAug;

	u64 roundOPPRF;
	printf("======argc=:%d\n", argc);
	u64 pIdx = atoi(argv[1]);
	tpsi_party_fudata(pIdx, 3, 2, 10000, SimulatedOkvs, secSemiHonest);
	return 0;
	switch (argc)
	{

	case 9: //tPSI
		//cout << "9\n";
		printf(">>>>>>>>>>>>>>>start");
		if (argv[1][0] == '-' && argv[1][1] == 'm')
			setSize = 1 << atoi(argv[2]);
		else
		{
			cout << "setSize: wrong format\n";
			usage(argv[0]);
			return 0;
		}

		if (argv[3][0] == '-' && argv[3][1] == 'n')
			nParties = atoi(argv[4]);
		else
		{
			cout << "nParties: wrong format\n";
			usage(argv[0]);
			return 0;
		}

		if (argv[5][0] == '-' && argv[5][1] == 't')
			tParties = atoi(argv[6]);
		else
		{
			cout << "tParties: wrong format\n";
			usage(argv[0]);
			return 0;
		}

		if (argv[7][0] == '-' && argv[7][1] == 'p')
		{
			u64 pIdx = atoi(argv[8]);
			//cout << setSize << " \t"  << nParties << " \t" << tParties << "\t" << pIdx << "\n";
			//tpsi_party(pIdx, nParties, tParties, setSize, PaxosOkvs, secSemiHonest);
			printf("============");
			// tpsi_party(pIdx, nParties, tParties, setSize, SimulatedOkvs, secSemiHonest);
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