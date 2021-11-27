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
nohup ./psi3 -m 100000 -p 0 >/dev/null 2>&1 &
nohup ./psi3 -m 100000 -p 1 >/dev/null 2>&1 &
time ./psi3 -m 100000 -p 2