#allows the terminal to throw an exception where it finds the error and then the code stop execution. 
set -e

TAXI_TYPE=$1 # "yellow"
YEAR=$2 # 2020

URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

for MONTH in {1..12}; do
  FMONTH=`printf "%02d" ${MONTH}`

  URL="${URL_PREFIX}/${TAXI_TYPE}/${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv.gz"

  LOCAL_PREFIX="data/raw/${TAXI_TYPE}/${YEAR}/${FMONTH}"
  LOCAL_FILE="${TAXI_TYPE}_tripdata_${YEAR}_${FMONTH}.csv.gz"
  LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

  echo "donwloading ${URL} to ${LOCAL_PATH}"
  mkdir -p ${LOCAL_PREFIX}
  wget ${URL} -O ${LOCAL_PATH}

  #echo "compressing ${LOCAL_PATH}"
  #gzip ${LOCAL_PATH}
done