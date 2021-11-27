#n方
NP=7
TH=$1
# nohup ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 0 >/dev/null 2>&1 &
# nohup ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 1 >/dev/null 2>&1 &
# nohup ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 2 >/dev/null 2>&1 &
# nohup ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 3 >/dev/null 2>&1 &
# nohup ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 4 >/dev/null 2>&1 &
# nohup ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 5 >/dev/null 2>&1 &
# ./bin/frontend.exe -m 12 -n ${NP} -t ${TH} -p 6
######nohup ./bin/frontend.exe -m 12 -n ${NP} -t 3 -p 3 > last.txt 2>&1 &
######psi#
#/home/chlf/fromgit/kashan/python37/bin/python3.7
PY37_BIN=python3
nohup ${PY37_BIN} psi3_process.py --m=1000000 --p=0 >/dev/null 2>&1 &
nohup ${PY37_BIN} psi3_process.py --m=1000000 --p=1 >/dev/null 2>&1 &
time ${PY37_BIN} psi3_process.py --m=1000000 --p=2