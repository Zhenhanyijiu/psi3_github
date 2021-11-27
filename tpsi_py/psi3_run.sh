#使用说明
#./psi3_run.sh此脚本实现三方求交功能
#运行脚本时，后面跟6个参数，参数顺序不能改变
#第1个参数是节点号，取值0,1,2；2号节点表示发起方
#第2个参数是本节点的csv文件路径;
#第3个参数是0号节点的ip
#第4个参数是1号节点的ip
#第5个参数是2号节点的ip
#第6个参数表示csv文件中ID列的字段名字
#例如：
#0号节点
#./psi3_run.sh 0 ../psi_1e_3kw_0.csv 10.100.3.51 10.100.3.97 10.100.3.98 id0_name

#1号节点
#./psi3_run.sh 1 ../psi_1e_3kw_1.csv 10.100.3.51 10.100.3.97 10.100.3.98 id1_name

#2号节点，也是发起方节点
#./psi3_run.sh 2 ../psi_1e_3kw_2.csv 10.100.3.51 10.100.3.97 10.100.3.98 id2_name


export LD_LIBRARY_PATH=../libdev/lib/
P_ID=$1
FILE_PATH=$2
IP_0=$3
IP_1=$4
IP_2=$5
ID_NAME=$6
echo "============pid:${P_ID}"
echo "============开始分桶"
# time python3 psi3_batch.py --c=init --p=${P_ID} --f=${FILE_PATH}
time python3 psi3_batch.py init --pid=${P_ID} --in_file=${FILE_PATH} --id=${ID_NAME}
echo "============开始求交"
for((i=0;i<16;i++));
do
    echo "===第$i个桶求交";
    # time python3 psi3_batch.py --c=start --p=${P_ID} --b=$i
    time python3 psi3_batch.py start --pid=${P_ID} --bucket=$i --ip0=${IP_0} --ip1=${IP_1} --ip2=${IP_2}
done
echo "============最后获取结果"
if [ $1 -eq 2 ];then
    # time python3 psi3_batch.py --c=end --p=${P_ID} --f=${FILE_PATH}
    time python3 psi3_batch.py end --pid=${P_ID} --in_file=${FILE_PATH} --id=${ID_NAME}
    #../psi_1e_3kw_2.csv
fi