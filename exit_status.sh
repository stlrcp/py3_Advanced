wget -q http://10.201.40.22/files/sw_home/scripts/compare_kv000.py


EXIT_STATUS=0

python3 test.py

EXIT_STATUS=${PIPESTATUS[0]}
if [[ $EXIT_STATUS = 100 ]]; then
  echo "ERROR: compare resnet50 inference in bi with inference in nv failed"
  exit 1
elif [[ $EXIT_STATUS != 0 ]]; then
  EXIT_STATUS=1
else
  EXIT_STATUS=0
fi

exit ${EXIT_STATUS}
