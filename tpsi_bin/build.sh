#该脚本编译出frontend.exe可执行文件
#当前目录有lib依赖库libcryptoTools.a、liblibOPRF.a、liblibOTe.a、liblibPaXoS.a
#否则先编译出上述依赖库
#-lboost_system
# -fPIC -shared
#g++ -O3 -DNDEBUG -O2 -g -O0 -ffunction-sections -Wall -Wfatal-errors \
#-maes -msse2 -msse4.1 -mpclmul -std=gnu++14 -pthread \
#-I ./cryptoTools \
#-I ./thirdparty/linux/boost/includes \
#-I ./libOPRF \
#-I ./libOTe \
#-I ./libPaXoS \
#-I ./thirdparty/linux/miracl/ \
#-I ./thirdparty/linux/ntl/include/ \
#-I ./frontend \
#-L ./thirdparty/linux/boost/stage/lib \
#-L lib \
#-L thirdparty/linux/miracl/miracl/source \
#-L thirdparty/linux/ntl/src/ \
#frontend/CLP.cpp \
#frontend/OtBinMain.cpp \
#frontend/OtBinMain.v2.cpp \
#frontend/bitPosition.cpp \
#frontend/miraclTest.cpp \
#frontend/util.cpp \
#./lib/liblibPaXoS.a \
#./lib/liblibOTe.a \
#./lib/liblibOPRF.a \
#-lcryptoTools -lmiracl -lntl -lboost_system \
#./frontend/main.cpp -o frontend.exe \

# -lcryptoTools -llibOPRF -llibOTe -lmiracl -lntl \
#nasm -f elf64 ../cryptoTools/Crypto/asm/sha_lnx.S -o ../cryptoTools/Crypto/asm/sha_lnx.S.o
#../cryptoTools/Crypto/asm/sha_lnx.S.o \
# -DNO_INTEL_ASM_SHA1=1 -DTEST_PSI3 \
#-fPIC -shared
#./b2 stage --with-system --with-thread link=static -mt -fPIC -shared
#-lboost_system 
#-I ../thirdparty/linux/ntl/include/ \
#-L ../thirdparty/linux/ntl/src/ \
#编译ntl

CURRENT_PATH="$PWD"
echo ${CURRENT_PATH}
if [ ! -f "../thirdparty/linux/ntl-11.4.3.tar.gz" ];then
    # cd ../thirdparty/linux/ntl/src/
    cd ../thirdparty/linux/
    wget https://libntl.org/ntl-11.4.3.tar.gz
    tar zxvf ntl-11.4.3.tar.gz
    mv ntl-11.4.3 ntl
    cd ntl/src/
    ./configure PREFIX=`pwd` GMP_PREFIX="${CURRENT_PATH}/../libdev"
    make -j4
    make install
    cp -r lib/libntl.a .
    # make clean
    # make -j4 ./ntl.a 
    # mv ./ntl.a ./libntl.a
    # bash ntl.get
    # cd - & cd ../../psi3_bin/
    cd ${CURRENT_PATH}
fi

echo "========pwds start==========="
pwd
pwd
echo "========pwds end=============="

if [ -f "tpsi" ];then
    rm -rf tpsi
fi

g++ -O3 -DNDEBUG -O2 -g -O0 -ffunction-sections -Wall -Wfatal-errors \
-maes -msse2 -msse3 -msse4.1 -mpclmul -std=c++11 -pthread \
-DNO_INTEL_ASM_SHA1=1 -DTPSI_TEST \
-I . \
-I ../cryptoTools \
-I ../thirdparty/linux/boost/includes \
-I ../libdev/include \
-I ../libOPRF \
-I ../libOTe \
-I ../libPaXoS \
-I ../thirdparty/linux/miracl/ \
-L ../thirdparty/linux/boost/stage/lib \
-L ../thirdparty/linux/miracl/miracl/source \
-L ../libdev/lib \
../cryptoTools/Network/*.cpp \
../cryptoTools/Crypto/*.cpp \
../cryptoTools/Common/*.cpp \
../libOTe/TwoChooseOne/*.cpp \
../libOTe/NChooseOne/*.cpp \
../libOTe/Base/*.cpp \
../libOTe/Tools/*.cpp \
../libOPRF/OPPRF/*.cpp \
../libOPRF/Hashing/*.cpp \
../libPaXoS/ObliviousDictionary.cpp \
../libPaXoS/gf2e_mat_solve.cpp \
./*.cpp \
../libPaXoS/xxHash/libxxhash.a \
../libdev/lib/liblinbox.a \
../libdev/lib/libgivaro.a \
../libdev/lib/libgmpxx.a \
../libdev/lib/libgmp.a \
../libdev/lib/libopenblas.a \
../thirdparty/linux/ntl/src/libntl.a \
-lmiracl -lboost_system \
-o tpsi
# ../thirdparty/linux/ntl/src/libntl.a \
# -o libpsi3.so
#-llinbox
# -lboost_system 
# -lopenblas  -lgmp -lgomp \
#-I ../thirdparty/linux/linbox/build/fflas-ffpack \
# -I ../thirdparty/linux/linbox \
# -I ../thirdparty/linux/linbox/build/fflas-ffpack \
#-llinbox -lgivaro -lopenblas -lgmp \
# /tmp/lib/liblinbox.a \
# /tmp/lib/libgivaro.a \
# /tmp/lib/libgmpxx.a \
# /tmp/lib/libopenblas.a \
# /tmp/lib/libgmp.a \
#-lgomp 
#../libdev/lib/libgmp.a \ 