# psi3
# 简化部署

> 安装依赖

>> apt install pkg-config gfortran autoconf automake libtool

>> git clone git@git.caimi-inc.com:avatar-crypto/psi3.git

>> cd psi

>> bash install_dev.sh

>> cd psi_py/

>> python3 setup.py build_ext --inplace

>> bash run.sh







# 编译步骤

> 编译xxhash

>> cd ../libPaXoS/xxHash
 
>> g++ -g -fPIC -shared -c ./*.c

>> ar rc libxxhash.a ./*.o

> 安装boost

>> cd ../thirdparty/linux

>> wget https://boostorg.jfrog.io/artifactory/main/release/1.64.0/source/boost_1_64_0.tar.bz2

>> tar xfj boost_1_64_0.tar.bz2

>> mv boost_1_64_0 boost

>> cd ./boost

>> ./bootstrap.sh

>> ./b2 stage --with-system --with-thread link=static -mt cxxflags="-fPIC -shared"

>> mkdir includes

>> cp -r boost includes/(或者用软链接也可以)

> 编译miracl

>> cd ../thirdparty/linux/miracl/miracl/source/

>> bash linux64

> 编译ntl

>> cd ../thirdparty/linux/ntl/src

>> make clean

>> make ./ntl.a 

>> mv ./ntl.a ./libntl.a

# centos 可能需要升级一些依赖,g++版本>=8

>> 安装依赖linbox,gmp,openblas,fflas-ffpack,givaro等

>> wget https://github.com/linbox-team/linbox.git

>> ./linbox-auto-install.sh --enable-openblas=yes --enable-gmp=yes(github可能访问不了)

>> ./linbox-auto-install.sh --stable=yes --make-flags="-j 4" --with-blas-libs="-lopenblas"

>> {./configure --with-pic,  ./configure CFLAGS="-fPIC"}


> libtool升级

>> yum remove libtool

>> wget http://mirrors.ustc.edu.cn/gnu/libtool/libtool-2.4.6.tar.gz

>> tar zxvf libtool-2.4.6.tar.gz

>> cd libtool-2.4.6/

>> ./configure --prefix=/usr

>> make && make install

> 安装linbox,之前先安装fflas-ffpack

> 安装fflas-ffpack

>> ./autogen.sh 