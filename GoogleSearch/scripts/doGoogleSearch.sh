#!/bin/bash
source ~/ResearchProject/ResearchProject/bin/activate


FILE_TO_WATCH=../logs/openvpn.log
SEARCH_PATTERN='*Initialization Sequence Completed*'

tail -f ${FILE_TO_WATCH} | while read LOGLINE
do
   [[ "${LOGLINE}" == ${SEARCH_PATTERN} ]] && pkill -P $$ tail && python ~/ResearchProject/GoogleSearch/src/GoogleSearch.py
done
