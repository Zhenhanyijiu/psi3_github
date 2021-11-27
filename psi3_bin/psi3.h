#pragma once
#include "OtBinMain.h"
#include "OtBinMain.v2.h"
#include "bitPosition.h"
#include "o1party.h"

#include "Crypto/PRNG.h"
#include "Common/Defines.h"
#include "Common/Log.h"
#include "Common/Log1.h"
#include <set>
#include "gbf.h"
#include <fstream>
#include <util.h>
#include "Network/Channel.h"
#include "Network/BtEndpoint.h"
#include "NChooseOne/KkrtNcoOtReceiver.h"
#include "NChooseOne/KkrtNcoOtSender.h"
#include "OPPRF/OPPRFReceiver.h"
#include "OPPRF/OPPRFSender.h"
#include <Common/ByteStream.h>
#include <string.h>
#include <Crypto/sha1.h>

using namespace osuCrypto;
//参数type_security没有意义
inline void party_psi3_only(u64 myIdx, u64 setSize,
							std::vector<std::vector<char>> ip_array,
							std::vector<std::vector<u32>> port_arrays,
							std::vector<std::vector<u8>> data_set,
							std::vector<u64> *psiResultsOutput,
							u64 type_okvs, u64 type_security)
{
	// u32 PORT_S[3] = {10200, 10201, 10202};
	printf("===>>(in party_psi3_only)setSize:%ld,data_set.size:%d\n", setSize, data_set.size());
	printf("====>>>##per_id_size:%ld\n", data_set[0].size());
	int count = 0;
	for (int i = 0; i < data_set.size(); i++)
	{
		if (data_set[i].size() == 16)
		{
			count++;
		}
		else
		{
			// printf("===>>not 16:::%ld\n", data_set[i].size());
		}
	}
	printf("===>>>###count_debug:%d\n", count);
	u64 nParties = 3;
	int ff = 8;
	// std::fstream textout;
	// textout.open("./runtime_" + myIdx, textout.app | textout.out);

#pragma region setup
	// u64 psiSecParam = 40, bitSize = 128, numChannelThreads = 1, okvsTableSize = setSize;
	u64 psiSecParam = 40, bitSize = 128, numChannelThreads = 1, okvsTableSize = setSize;
	Timer timer;
	PRNG prng(_mm_set_epi32(4253465, 3434565, myIdx, myIdx));
	// (*(u64*)&prng.get<block>()) % setSize;

	// if (type_okvs == GbfOkvs)
	// 	okvsTableSize = okvsLengthScale * setSize;
	// else if (type_okvs == PolyOkvs)
	// 	okvsTableSize = setSize;
	// std::string ip_array[3][3] = {{"", "", ""},
	// 							  {"127.0.0.1", "", ""},
	// 							  {"10.100.3.15", "10.100.3.15", ""}};

	std::string name("psi3");
	BtIOService ios(0);
	std::vector<BtEndpoint> ep(nParties);
	std::vector<std::vector<Channel *>> chls(nParties);
	for (u64 i = 0; i < nParties; ++i)
	{
		if (i < myIdx)
		{
			//myIdx=0,i=0,no;  i=1,no;   i=2,no
			//myIdx=1,i=0,1201;i=1,no;   i=2,no
			//myIdx=2,i=0,1202;i=1,1302; i=2,no
			// u32 port = 10200 + i * 100 + myIdx;
			//get the same port; i=1 & pIdx=2 =>port=102
			//channel bwt i and pIdx, where i is sender
			// ep[i].start(ios, ip_array[myIdx].data(), port_arrays[myIdx][i], false, name);
			char ip_char[32] = {0};
			memset(ip_char, 0, 32);
			memcpy(ip_char, ip_array[i].data(), ip_array[i].size());
			ep[i].start(ios, ip_char, port_arrays[myIdx][i], false, name);
			// ep[i].start(ios, ip_array[i].data(), port_arrays[myIdx][i], false, name);
			// ep[i].start(ios, ip_array[myIdx][i], port_arrays[myIdx][i], false, name);
		}
		else if (i > myIdx)
		{
			//myIdx=0,i=0,no;i=1,1201; i=2,1202
			//myIdx=1,i=0,no;i=1,no;   i=2,1302
			//myIdx=2,i=0,no;i=1,no;   i=2,no
			// u32 port = 10200 + myIdx * 100 + i;
			//get the same port; i=2 & pIdx=1 =>port=102
			//channel bwt i and pIdx, where i is receiver
			// ep[i].start(ios, ip_array[i].data(), port_arrays[myIdx][i], true, name);
			char ip_char[32] = {0};
			memset(ip_char, 0, 32);
			memcpy(ip_char, ip_array[myIdx].data(), ip_array[myIdx].size());
			printf("===in psi3_process_only,i:%d,curr_ip:%s\n", i, ip_char);
			ep[i].start(ios, ip_char, port_arrays[myIdx][i], true, name);
			// ep[i].start(ios, ip_array[myIdx].data(), port_arrays[myIdx][i], true, name);
			// ep[i].start(ios, "0", port_arrays[myIdx][i], true, name);
		}
	}

	// for (u64 i = 0; i < myIdx; i++)
	// {
	// 	ep[i].start(ios, IP_S[i], PORT_S[i], true, name);
	// }

	// for (u64 i = myIdx + 1; i < nParties; i++)
	// {
	// 	ep[i].start(ios, IP_S[myIdx], PORT_S[myIdx], true, name);
	// }
	printf("=============network end===========\n");
	for (u64 i = 0; i < nParties; ++i)
	{
		if (i != myIdx)
		{
			chls[i].resize(numChannelThreads);
			for (u64 j = 0; j < numChannelThreads; ++j)
				chls[i][j] = &ep[i].addChannel(name, name);
		}
	}

	// u64 maskSize = roundUpTo(psiSecParam + 2 * std::log2(setSize) - 1, 8) / 8;

	// PRNG prngSame(_mm_set_epi32(4253465, 3434565, 234435, 23987045)), prngDiff(_mm_set_epi32(434653, 23, myIdx, myIdx));
	std::vector<block> inputSet(setSize);
	SHA1 sha1_hash;
	u8 output[20];
	for (u64 i = 0; i < setSize; i++)
	{
		// memcpy((char *)(inputSet.data() + i), data_set[i].data(), 16);
		sha1_hash.Reset();
		sha1_hash.Update(data_set[i].data(), data_set[i].size());
		sha1_hash.Final(output);
		inputSet[i] = *(block *)output;
	}
	// for (u64 i = 0; i < expected_intersection; ++i)
	// 	inputSet[i] = prngSame.get<block>();

	// for (u64 i = expected_intersection; i < setSize; ++i)
	// 	inputSet[i] = prngDiff.get<block>();
#pragma endregion

	// u64 num_threads = nParties - 1; //for party 1

	timer.reset();
	auto start = timer.setTimePoint("start");

	std::vector<block> aesKeys(2); // for party 1 and 2

	std::vector<block> inputSet2PSI(setSize, ZeroBlock); //for party 2 and 3
	std::vector<std::vector<block>> ciphertexts(3);		 //for party 1 and 2 to compute F(k, a)
	for (int i = 0; i < ciphertexts.size(); i++)
		ciphertexts[i].resize(setSize); //ciphertexts[2] <= payload recived from party 2 via opprf

	//====================================
	//============sending aes keys========
	if (myIdx == 0)
	{
		//generating aes key and sends it to party 2
		aesKeys[0] = prng.get<block>();
		chls[1][0]->asyncSend(&aesKeys[0], sizeof(block)); //sending aesKeys_party1 to party 2 (idx=1)
		printf("===>>id0:1....\n");
		/*	std::cout << IoStream::lock;
			std::cout << aesKeys_party1 << std::endl;
			std::cout << IoStream::unlock;*/

		AES party1_AES(aesKeys[0]);
		party1_AES.ecbEncBlocks(inputSet.data(), inputSet.size(), ciphertexts[0].data()); //compute F_ki(xi)
	}

	if (myIdx == 1)
	{
		chls[0][0]->recv(&aesKeys[1], sizeof(block)); //receiving aesKey from paty 1 (idx=0)
													  /*	std::cout << IoStream::lock;
			std::cout << aesReceivedKey <<  " - aesReceivedKey - " <<myIdx << std::endl;
			std::cout << IoStream::unlock;*/

		//P2 computes encoding========
		AES party2_AES(aesKeys[1]);
		party2_AES.ecbEncBlocks(inputSet.data(), inputSet.size(), ciphertexts[1].data()); //compute F_ki(xi)
	}
	bool noStash = 0;
	//====================================
	//============compute OPPRF========
	//节点0和2之间进行opprf
	if (myIdx == 0 || myIdx == 2) //for opprf btw party 1 and 3
	{
		std::vector<KkrtNcoOtReceiver> otRecv(2);
		std::vector<KkrtNcoOtSender> otSend(2);
		OPPRFSender send;	//opprf发送方
		OPPRFReceiver recv; //opprf接收方
		binSet bins;
		//opt==0
		//psiSecParam=40,myIdx=0
		bins.init(myIdx, 2, setSize, psiSecParam, 0, noStash); //nostash==1
		u64 otCountSend = bins.mSimpleBins.mBins.size();
		u64 otCountRecv = bins.mCuckooBins.mBins.size();
		printf(">>>(mSimpleBins)otCountSend:%ld\n", otCountSend);
		printf(">>>(mCuckooBins)otCountRecv:%ld\n", otCountRecv);

		if (myIdx == 0)
		{
			//I am a sender -> party_1
			send.init(bins.mOpt, 2, setSize, psiSecParam, bitSize,
					  chls[2], otCountSend,
					  otSend[1],
					  otRecv[1],
					  prng.get<block>(), false);
		}
		else if (myIdx == 2)
		{
			//I am a recv <-party_3
			recv.init(bins.mOpt, 2, setSize, psiSecParam, bitSize,
					  chls[0], otCountRecv,
					  otRecv[0],
					  otSend[0],
					  ZeroBlock, false);
		}
		printf("===>>id0:2....\n");
		bins.hashing2Bins(inputSet, 1); //布谷鸟bins
		if (myIdx == 0)
		{
			printf("===>>id0:2.3333....\n");
			//I am a sender to my next neigbour
			send.getOPRFkeys(1, bins, chls[2], false);
			printf("===>>id0:2.2222....\n");
			send.sendSS(1, bins, ciphertexts[0], chls[2]);
			printf("===>>id0:2.111....\n");
		}
		else if (myIdx == 2)
		{
			//I am a recv to my previous neigbour
			recv.getOPRFkeys(0, bins, chls[0], false);
			recv.recvSS(0, bins, ciphertexts[2], chls[0]);
		}
		printf("===>>id0:3....\n");
		int as = 9;
	}

	/*std::cout << IoStream::lock;
		if (myIdx == 0 || myIdx == 2)
		{
			for (u64 i = 0; i < expected_intersection + 2; ++i)
				std::cout << ciphertexts[myIdx][i] << " - ciphertexts[0][0]  - " << myIdx << std::endl;
		}
		std::cout << IoStream::unlock;*/

	//====================================
	//============compute 2psi======== (inputSet2PSI has been filled before)

	if (myIdx == 1 || myIdx == 2) //for 2psi btw party 2 and 3
	{
		u64 mMaskSize = roundUpTo(40 + 2 * std::log2(setSize), 8) / 8;
		for (int i = 0; i < setSize; i++)
		{
			memcpy((u8 *)&inputSet2PSI[i], (u8 *)&ciphertexts[myIdx][i], mMaskSize);
			inputSet2PSI[i] = inputSet2PSI[i] ^ inputSet[i]; // ai||\hat{ai}
		}

		std::vector<KkrtNcoOtReceiver> otRecv(2);
		std::vector<KkrtNcoOtSender> otSend(2);
		OPPRFSender send;
		OPPRFReceiver recv;
		binSet bins;

		bins.init(myIdx, 2, setSize, psiSecParam, 0, noStash);
		//	bins.mMaskSize = 8;
		u64 otCountSend = bins.mSimpleBins.mBins.size();
		u64 otCountRecv = bins.mCuckooBins.mBins.size();

		if (myIdx == 1)
		{
			//I am a sender -> party_2
			send.init(bins.mOpt, 2, setSize, psiSecParam, bitSize,
					  chls[2], otCountSend,
					  otSend[1],
					  otRecv[1],
					  prng.get<block>(), false);
		}
		else if (myIdx == 2)
		{
			//I am a recv <-party_3
			recv.init(bins.mOpt, 2, setSize, psiSecParam, bitSize,
					  chls[1], otCountRecv,
					  otRecv[0],
					  otSend[0],
					  ZeroBlock, false);
		}

		//##########################
		//### Hashing
		//##########################
		bins.hashing2Bins(inputSet2PSI, 1);

		if (myIdx == 1)
		{
			//I am a sender to my next neigbour
			send.getOPRFkeysfor2PSI(1, bins, chls[2], false);
			send.sendLastPSIMessage(1, bins, chls[2]);
		}
		else if (myIdx == 2)
		{
			//I am a recv to my previous neigbour
			recv.getOPRFkeysfor2PSI(0, bins, chls[1], false);
			recv.compute2PSI(0, bins, chls[1]);
		}

		//##########################
		//### online phasing - compute intersection
		//##########################
		//获取求交数据
		if (myIdx == 2)
		{
			Log::out << "mIntersection.size(): " << recv.mIntersection.size() << Log::endl;
			// for (u64 i = 0; i < recv.mIntersection.size(); ++i)
			// {
			// 	// std::cout << recv.mIntersection[i] << " - " << inputSet[recv.mIntersection[i]] << std::endl;
			// 	std::cout << recv.mIntersection[i] << " - " << inputSet[recv.mIntersection[i]] << std::endl;
			// }
			u64 psi_num = recv.mIntersection.size();
			psiResultsOutput->resize(psi_num);
			for (u64 i = 0; i < psi_num; ++i)
			{
				(*psiResultsOutput)[i] = recv.mIntersection[i];
			}
		}
	}
	auto timer_end = timer.setTimePoint("end");

	double dataSent = 0, dataRecv = 0, Mbps = 0, MbpsRecv = 0;
	for (u64 i = 0; i < nParties; ++i)
	{
		if (i != myIdx)
		{
			//chls[i].resize(numThreads);
			dataSent += chls[i][0]->getTotalDataSent();
			dataRecv += chls[i][0]->getTotalDataRecv();
		}
	}

	if (myIdx == 2)
		std::cout << timer << std::endl;

	std::cout << "party #" << myIdx << "\t Comm: " << ((dataSent + dataRecv) / std::pow(2.0, 20)) << " MB" << std::endl;
	//total comm cost= (p1+p2+p3)/2

	//close chanels
	for (u64 i = 0; i < nParties; ++i)
		if (i != myIdx)
			for (u64 j = 0; j < numChannelThreads; ++j)
				chls[i][j]->close();

	for (u64 i = 0; i < nParties; ++i)
		if (i != myIdx)
			ep[i].stop();

	ios.stop();
}

inline void party_psi3(u64 myIdx, u64 setSize, u64 type_okvs, u64 type_security)
{
	char *IP_S[3] = {"127.0.0.1", "127.0.0.2", "127.0.0.3"};
	u32 PORT_S[3] = {10200, 10201, 10202};
	printf("===>>data size:%ld\n");
	u64 nParties = 3;
	// std::fstream textout;
	// textout.open("./runtime_" + myIdx, textout.app | textout.out);

#pragma region setup
	u64 psiSecParam = 40, bitSize = 128, numChannelThreads = 1, okvsTableSize = setSize;
	Timer timer;
	PRNG prng(_mm_set_epi32(4253465, 3434565, myIdx, myIdx));
	u64 expected_intersection = 3; // (*(u64*)&prng.get<block>()) % setSize;

	if (type_okvs == GbfOkvs)
		okvsTableSize = okvsLengthScale * setSize;
	else if (type_okvs == PolyOkvs)
		okvsTableSize = setSize;

	std::string name("psi3");
	BtIOService ios(0);
	std::vector<BtEndpoint> ep(nParties);
	std::vector<std::vector<Channel *>> chls(nParties);

	for (u64 i = 0; i < nParties; ++i)
	{
		if (i < myIdx)
		{
			//myIdx=0,i=0,no;  i=1,no;   i=2,no
			//myIdx=1,i=0,1201;i=1,no;   i=2,no
			//myIdx=2,i=0,1202;i=1,1302; i=2,no
			u32 port = 1200 + i * 100 + myIdx;
			;												  //get the same port; i=1 & pIdx=2 =>port=102
			ep[i].start(ios, IP_S[myIdx], port, false, name); //channel bwt i and pIdx, where i is sender
		}
		else if (i > myIdx)
		{
			//myIdx=0,i=0,no;i=1,1201; i=2,1202
			//myIdx=1,i=0,no;i=1,no;   i=2,1302
			//myIdx=2,i=0,no;i=1,no;   i=2,no
			u32 port = 1200 + myIdx * 100 + i;			 //get the same port; i=2 & pIdx=1 =>port=102
			ep[i].start(ios, IP_S[i], port, true, name); //channel bwt i and pIdx, where i is receiver
		}
	}

	// for (u64 i = 0; i < myIdx; i++)
	// {
	// 	ep[i].start(ios, IP_S[i], PORT_S[i], true, name);
	// }

	// for (u64 i = myIdx + 1; i < nParties; i++)
	// {
	// 	ep[i].start(ios, IP_S[myIdx], PORT_S[myIdx], true, name);
	// }
	printf("=============network end===========\n");
	for (u64 i = 0; i < nParties; ++i)
	{
		if (i != myIdx)
		{
			chls[i].resize(numChannelThreads);
			for (u64 j = 0; j < numChannelThreads; ++j)
				chls[i][j] = &ep[i].addChannel(name, name);
		}
	}

	u64 maskSize = roundUpTo(psiSecParam + 2 * std::log2(setSize) - 1, 8) / 8;

	PRNG prngSame(_mm_set_epi32(4253465, 3434565, 234435, 23987045)), prngDiff(_mm_set_epi32(434653, 23, myIdx, myIdx));
	std::vector<block> inputSet(setSize);

	for (u64 i = 0; i < expected_intersection; ++i)
		inputSet[i] = prngSame.get<block>();

	for (u64 i = expected_intersection; i < setSize; ++i)
		inputSet[i] = prngDiff.get<block>();
#pragma endregion

	u64 num_threads = nParties - 1; //for party 1

	timer.reset();
	auto start = timer.setTimePoint("start");

	std::vector<block> aesKeys(2); // for party 1 and 2

	std::vector<block> inputSet2PSI(setSize, ZeroBlock); //for party 2 and 3
	std::vector<std::vector<block>> ciphertexts(3);		 //for party 1 and 2 to compute F(k, a)
	for (int i = 0; i < ciphertexts.size(); i++)
		ciphertexts[i].resize(setSize); //ciphertexts[2] <= payload recived from party 2 via opprf

	//====================================
	//============sending aes keys========
	if (myIdx == 0)
	{
		//generating aes key and sends it to party 2
		aesKeys[0] = prng.get<block>();
		chls[1][0]->asyncSend(&aesKeys[0], sizeof(block)); //sending aesKeys_party1 to party 2 (idx=1)

		/*	std::cout << IoStream::lock;
			std::cout << aesKeys_party1 << std::endl;
			std::cout << IoStream::unlock;*/

		AES party1_AES(aesKeys[0]);
		party1_AES.ecbEncBlocks(inputSet.data(), inputSet.size(), ciphertexts[0].data()); //compute F_ki(xi)
	}

	if (myIdx == 1)
	{
		chls[0][0]->recv(&aesKeys[1], sizeof(block)); //receiving aesKey from paty 1 (idx=0)
													  /*	std::cout << IoStream::lock;
			std::cout << aesReceivedKey <<  " - aesReceivedKey - " <<myIdx << std::endl;
			std::cout << IoStream::unlock;*/

		//P2 computes encoding========
		AES party2_AES(aesKeys[1]);
		party2_AES.ecbEncBlocks(inputSet.data(), inputSet.size(), ciphertexts[1].data()); //compute F_ki(xi)
	}

	//====================================
	//============compute OPPRF========
	if (myIdx == 0 || myIdx == 2) //for opprf btw party 1 and 3
	{
		std::vector<KkrtNcoOtReceiver> otRecv(2);
		std::vector<KkrtNcoOtSender> otSend(2);
		OPPRFSender send;
		OPPRFReceiver recv;
		binSet bins;

		bins.init(myIdx, 2, setSize, psiSecParam, 0, 1);
		u64 otCountSend = bins.mSimpleBins.mBins.size();
		u64 otCountRecv = bins.mCuckooBins.mBins.size();

		if (myIdx == 0)
		{
			//I am a sender -> party_1
			send.init(bins.mOpt, 2, setSize, psiSecParam, bitSize, chls[2], otCountSend, otSend[1], otRecv[1], prng.get<block>(), false);
		}
		else if (myIdx == 2)
		{
			//I am a recv <-party_3
			recv.init(bins.mOpt, 2, setSize, psiSecParam, bitSize, chls[0], otCountRecv, otRecv[0], otSend[0], ZeroBlock, false);
		}

		bins.hashing2Bins(inputSet, 1);

		if (myIdx == 0)
		{
			//I am a sender to my next neigbour
			send.getOPRFkeys(1, bins, chls[2], false);
			send.sendSS(1, bins, ciphertexts[0], chls[2]);
		}
		else if (myIdx == 2)
		{
			//I am a recv to my previous neigbour
			recv.getOPRFkeys(0, bins, chls[0], false);
			recv.recvSS(0, bins, ciphertexts[2], chls[0]);
		}
	}

	/*std::cout << IoStream::lock;
		if (myIdx == 0 || myIdx == 2)
		{
			for (u64 i = 0; i < expected_intersection + 2; ++i)
				std::cout << ciphertexts[myIdx][i] << " - ciphertexts[0][0]  - " << myIdx << std::endl;
		}
		std::cout << IoStream::unlock;*/

	//====================================
	//============compute 2psi======== (inputSet2PSI has been filled before)

	if (myIdx == 1 || myIdx == 2) //for 2psi btw party 2 and 3
	{
		u64 mMaskSize = roundUpTo(40 + 2 * std::log2(setSize), 8) / 8;
		for (int i = 0; i < setSize; i++)
		{
			memcpy((u8 *)&inputSet2PSI[i], (u8 *)&ciphertexts[myIdx][i], mMaskSize);
			inputSet2PSI[i] = inputSet2PSI[i] ^ inputSet[i]; // ai||\hat{ai}
		}

		std::vector<KkrtNcoOtReceiver> otRecv(2);
		std::vector<KkrtNcoOtSender> otSend(2);
		OPPRFSender send;
		OPPRFReceiver recv;
		binSet bins;

		bins.init(myIdx, 2, setSize, psiSecParam, 0, 1);
		//	bins.mMaskSize = 8;
		u64 otCountSend = bins.mSimpleBins.mBins.size();
		u64 otCountRecv = bins.mCuckooBins.mBins.size();

		if (myIdx == 1)
		{
			//I am a sender -> party_2
			send.init(bins.mOpt, 2, setSize, psiSecParam, bitSize, chls[2], otCountSend, otSend[1], otRecv[1], prng.get<block>(), false);
		}
		else if (myIdx == 2)
		{
			//I am a recv <-party_3
			recv.init(bins.mOpt, 2, setSize, psiSecParam, bitSize, chls[1], otCountRecv, otRecv[0], otSend[0], ZeroBlock, false);
		}

		//##########################
		//### Hashing
		//##########################
		bins.hashing2Bins(inputSet2PSI, 1);

		if (myIdx == 1)
		{
			//I am a sender to my next neigbour
			send.getOPRFkeysfor2PSI(1, bins, chls[2], false);
			send.sendLastPSIMessage(1, bins, chls[2]);
		}
		else if (myIdx == 2)
		{
			//I am a recv to my previous neigbour
			recv.getOPRFkeysfor2PSI(0, bins, chls[1], false);
			recv.compute2PSI(0, bins, chls[1]);
		}

		//##########################
		//### online phasing - compute intersection
		//##########################

		if (myIdx == 2)
		{
			Log::out << "mIntersection.size(): " << recv.mIntersection.size() << Log::endl;
			/*for (u64 i = 0; i < recv.mIntersection.size(); ++i)
				{
					std::cout << recv.mIntersection[i] << " - " << inputSet[recv.mIntersection[i]] << std::endl;

				}*/
		}
	}
	auto timer_end = timer.setTimePoint("end");

	double dataSent = 0, dataRecv = 0, Mbps = 0, MbpsRecv = 0;
	for (u64 i = 0; i < nParties; ++i)
	{
		if (i != myIdx)
		{
			//chls[i].resize(numThreads);
			dataSent += chls[i][0]->getTotalDataSent();
			dataRecv += chls[i][0]->getTotalDataRecv();
		}
	}

	if (myIdx == 2)
		std::cout << timer << std::endl;

	std::cout << "party #" << myIdx << "\t Comm: " << ((dataSent + dataRecv) / std::pow(2.0, 20)) << " MB" << std::endl;
	//total comm cost= (p1+p2+p3)/2

	//close chanels
	for (u64 i = 0; i < nParties; ++i)
		if (i != myIdx)
			for (u64 j = 0; j < numChannelThreads; ++j)
				chls[i][j]->close();

	for (u64 i = 0; i < nParties; ++i)
		if (i != myIdx)
			ep[i].stop();

	ios.stop();
}

inline void party_psi2_server_aided(u64 myIdx, u64 setSize, u64 type_security)
{
	u64 nParties = 3;
	std::fstream textout;
	textout.open("./runtime_" + myIdx, textout.app | textout.out);

#pragma region setup
	u64 psiSecParam = 40, bitSize = 128, numChannelThreads = 1, okvsTableSize = setSize;
	Timer timer;
	PRNG prng(_mm_set_epi32(4253465, 3434565, myIdx, myIdx));
	u64 expected_intersection = rand() % setSize; // (*(u64*)&prng.get<block>()) % setSize;
	std::vector<u32> mIntersection;

	std::string name("psi");
	BtIOService ios(0);
	std::vector<BtEndpoint> ep(nParties);
	std::vector<std::vector<Channel *>> chls(nParties);

	for (u64 i = 0; i < nParties; ++i)
	{
		if (i < myIdx)
		{
			u32 port = 1200 + i * 100 + myIdx;
			;												  //get the same port; i=1 & pIdx=2 =>port=102
			ep[i].start(ios, "localhost", port, false, name); //channel bwt i and pIdx, where i is sender
		}
		else if (i > myIdx)
		{
			u32 port = 1200 + myIdx * 100 + i;				 //get the same port; i=2 & pIdx=1 =>port=102
			ep[i].start(ios, "localhost", port, true, name); //channel bwt i and pIdx, where i is receiver
		}
	}

	for (u64 i = 0; i < nParties; ++i)
	{
		if (i != myIdx)
		{
			chls[i].resize(numChannelThreads);
			for (u64 j = 0; j < numChannelThreads; ++j)
				chls[i][j] = &ep[i].addChannel(name, name);
		}
	}

	u64 maskSize = roundUpTo(psiSecParam + 2 * std::log2(setSize) - 1, 8) / 8;

	PRNG prngSame(_mm_set_epi32(4253465, 3434565, 234435, 23987045)), prngDiff(_mm_set_epi32(434653, 23, myIdx, myIdx));
	std::vector<block> inputSet(setSize);

	if (myIdx == 0 || myIdx == 1) //two parties have input
	{
		for (u64 i = 0; i < expected_intersection; ++i)
			inputSet[i] = prngSame.get<block>();

		for (u64 i = expected_intersection; i < setSize; ++i)
			inputSet[i] = prngDiff.get<block>();
	}
#pragma endregion

	timer.reset();
	auto start = timer.setTimePoint("start");

	std::vector<block> aesKeys(2);					// for party 1 and 2
	std::vector<std::vector<block>> ciphertexts(2); //for party 1 and 2 to compute F(k, a)
	for (int i = 0; i < ciphertexts.size(); i++)
		ciphertexts[i].resize(setSize);

	std::vector<std::vector<block>> recv_ciphertexts(2); //for server to receive pi(F(k, a)) form party 1 and 2
	for (int i = 0; i < recv_ciphertexts.size(); i++)
		recv_ciphertexts[i].resize(setSize);

	//====================================
	//============exchange aes keys => send pi(F_ki(xi)) to server => server computes intersection========
	if (myIdx == 0)
	{
		//generating aes key and sends it to party 2
		aesKeys[0] = prng.get<block>();
		chls[1][0]->asyncSend(&aesKeys[0], sizeof(block)); //sending aesKeys_party1 to party 2 (idx=1)

		AES party1_AES(aesKeys[0]);
		party1_AES.ecbEncBlocks(inputSet.data(), inputSet.size(), ciphertexts[0].data()); //compute F_ki(xi)
		//shuffle(ciphertexts[0].begin(), ciphertexts[0].end(), prngSame); //

		shuffle(ciphertexts[0].begin(), ciphertexts[0].end(), prng);

		chls[2][0]->asyncSend(ciphertexts[0].data(), ciphertexts[0].size() * sizeof(block)); //send pi(F_ki(xi)) to server (party 3)

		/*std::cout << IoStream::lock;
				for (u64 i = 0; i < expected_intersection + 2; ++i)
					std::cout << ciphertexts[0][i] << " - ciphertexts[0][0]  - " << myIdx << std::endl;
			std::cout << IoStream::unlock;*/
	}

	else if (myIdx == 1)
	{
		chls[0][0]->recv(&aesKeys[1], sizeof(block)); //receiving aesKey from paty 1 (idx=0)

		//P2 computes encoding========
		AES party2_AES(aesKeys[1]);
		party2_AES.ecbEncBlocks(inputSet.data(), inputSet.size(), ciphertexts[1].data()); //compute F_ki(xi)
		//shuffle(ciphertexts[1].begin(), ciphertexts[1].end(), prngDiff);

		shuffle(ciphertexts[1].begin(), ciphertexts[1].end(), prng);

		chls[2][0]->asyncSend(ciphertexts[1].data(), ciphertexts[1].size() * sizeof(block)); // send pi(F_ki(xi)) to server (party 3)

		/*std::cout << IoStream::lock;
			for (u64 i = 0; i < expected_intersection + 2; ++i)
				std::cout << ciphertexts[1][i] << " - ciphertexts[1][0]  - " << myIdx << std::endl;
			std::cout << IoStream::unlock;*/
	}
	else if (myIdx == 2) //server
	{
		chls[0][0]->recv(recv_ciphertexts[0].data(), setSize * sizeof(block)); // receive pi(F_ki(xi)) from party 1
		chls[1][0]->recv(recv_ciphertexts[1].data(), setSize * sizeof(block)); // receive pi(F_ki(xi)) from party 2

		/*std::cout << IoStream::lock;
			for (u64 i = 0; i < expected_intersection + 2; ++i)
			{
				std::cout << recv_ciphertexts[0][i] << " - recv_ciphertexts[0][0]  - " << myIdx << std::endl;
				std::cout << recv_ciphertexts[1][i] << " - recv_ciphertexts[1][0]  - " << myIdx << std::endl;
			}
			std::cout << IoStream::unlock;*/

		////compute intersection here

		std::unordered_map<u64, std::pair<block, u64>> localMasks;
		for (u32 i = 0; i < setSize; i++) //create an unordered_map for recv_ciphertexts[0]
		{
			localMasks.emplace(*(u64 *)&recv_ciphertexts[0][i], std::pair<block, u32>(recv_ciphertexts[0][i], i));
		}

		for (int i = 0; i < setSize; i++) //for each item in recv_ciphertexts[1], we check it in localMasks
		{
			u64 shortcut;
			memcpy((u8 *)&shortcut, (u8 *)&recv_ciphertexts[1][i], sizeof(u64));
			auto match = localMasks.find(shortcut);

			//if match, check for whole bits
			if (match != localMasks.end())
			{
				if (memcmp((u8 *)&recv_ciphertexts[1][i], &match->second.first, sizeof(block)) == 0) // check full mask
				{
					mIntersection.push_back(match->second.second);
				}
			}
		}
		Log::out << "mIntersection.size(): " << mIntersection.size() << Log::endl;
	}

	if (myIdx == 2)
	{ //Skip this steps

		chls[0][0]->asyncSend(mIntersection.data(), mIntersection.size() * sizeof(u32)); // send index of the intersection
																						 //chls[1][0]->asyncSend(mIntersection.data(), mIntersection.size() * sizeof(u32)); // send index of the intersection
	}
	else if (myIdx == 0)
	{
		ByteStream maskBuffer;
		chls[2][0]->recv(maskBuffer);
	}
	//if (myIdx == 0 || myIdx == 1)
	//{
	//	chls[2][0]->recv(mIntersection.data(),mIntersection.size() * sizeof(u32)); // receive pi(F_ki(xi)) from party 1
	//}

	auto end = timer.setTimePoint("end");

	double dataSent = 0, dataRecv = 0, Mbps = 0, MbpsRecv = 0;
	for (u64 i = 0; i < nParties; ++i)
	{
		if (i != myIdx)
		{
			//chls[i].resize(numThreads);
			dataSent += chls[i][0]->getTotalDataSent();
			dataRecv += chls[i][0]->getTotalDataRecv();
		}
	}

	if (myIdx == 2)
	{
		std::cout << timer << std::endl;
		std::cout << "party #" << myIdx << "\t Comm: " << ((dataSent + dataRecv) / std::pow(2.0, 20)) << " MB" << std::endl;
	}

	//total comm cost = send+recv (server 3)

	//close chanels
	for (u64 i = 0; i < nParties; ++i)
		if (i != myIdx)
			for (u64 j = 0; j < numChannelThreads; ++j)
				chls[i][j]->close();

	for (u64 i = 0; i < nParties; ++i)
		if (i != myIdx)
			ep[i].stop();

	ios.stop();
}
