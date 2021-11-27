#需要工具
#工作目录psi3
DEV_PARH="/tmp"
#创建依赖库目录
if [ ! -d "./libdev" ]; then
	echo "=======不存在libdev目录========"
	echo "create libdev"
	mkdir libdev
 	echo "dev_path:`pwd`/libdev"
else
	echo "=======存在libdev目录========"
	rm -rf ./libdev/*
fi
DEV_PARH=`pwd`/libdev
echo ${DEV_PARH}
#
#if [ ! $1 ]; then
#  echo "IS NULL"
#  echo "dev_path:${DEV_PARH}"
#else
#  echo "NOT NULL"
#  DEV_PARH=$1
#  echo "dev_path:${DEV_PARH}"
#fi

if [ ! -d "./linbox" ]; then
	# rm -rf linbox
	echo "=============git clone linbox====="
	git clone git://github.com/linbox-team/linbox.git
fi

cd linbox
if [ -f "install_start_func.sh" ]; then
	# rm -rf linbox
	rm -rf install_start_func.sh
fi
cp -r ../install_start_func.sh .
bash install_start_func.sh --prefix=${DEV_PARH}  --enable-openblas=yes --enable-gmp=yes --enable-ntl=yes


pwd
pwd
cd ..
#这里是工作目录psi3
###编译ntl
echo "编译ntl==============>"
cd ./linbox/build/ntl-11.4.3/src/
make clean
make ./ntl.a CXXFLAGS="-fPIC -shared"
mv ./ntl.a ${DEV_PARH}/lib/libntl.a
cd -

rm -rf ./linbox/build