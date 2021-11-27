

#当前目录是psi3/psi3_py/
CURRENT_PATH="$PWD"
##编译xxhash
echo "编译xxhash==============>"
cd ../libPaXoS/xxHash 
g++ -g -fPIC -shared -c ./*.c
ar rc libxxhash.a ./*.o
cd -


##boost 安装boost
echo "安装boost==============>"
# if [ -f "../thirdparty/linux/boost_1_64_0.tar.bz2" ]; then
#     cd ../thirdparty/linux
#     tar xfj boost_1_64_0.tar.bz2
#     mv boost_1_64_0 boost
#     cd ./boost
#     ./bootstrap.sh
#     ./b2 stage --with-system --with-thread link=static -mt cxxflags="-fPIC -shared"
#     mkdir includes
#     ##cp -r boost includes/(或者用软链接也可以)
#     ##用软链接
#     cd includes
#     ln -s ../boost boost
#     cd ${CURRENT_PATH}
# fi
if [ ! -f "../thirdparty/linux/boost_1_64_0.tar.bz2" ]; then
    cd ../thirdparty/linux
    wget https://boostorg.jfrog.io/artifactory/main/release/1.64.0/source/boost_1_64_0.tar.bz2
    tar xfj boost_1_64_0.tar.bz2
    mv boost_1_64_0 boost
    cd ./boost
    ./bootstrap.sh
    ./b2 stage --with-system --with-thread link=static -mt cxxflags="-fPIC -shared"
    mkdir includes
    ##cp -r boost includes/(或者用软链接也可以)
    ##用软链接
    cd includes
    ln -s ../boost boost
    cd ${CURRENT_PATH}
fi

##编译miracl
echo "编译miracl==============>"
if [ ! -f "../thirdparty/linux/miracl/miracl/source/libmiracl.a" ]; then
  cd ../thirdparty/linux/miracl/miracl/source/
  bash linux64
  cd -
fi
