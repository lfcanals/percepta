#!/bin/bash

cameraId=$1
numImages=$2

if [ "${numImages}" == "" ]; then
  numImages=100
fi


pushd .
cd target
python3 tools/realtime-eye-fish-calibration.py $cameraId $numImages
popd

now=$(date +"%Y%m%d.%H%M%S")
destination="./database/$cameraId/$now"
mkdir -p "$destination"
mv ./database/*.json "$destination/" 2> /dev/null




echo Information about the error:
echo "    < 0.3 px	    Excellent"
echo "    0.3–0.7 px	Very good"
echo "    0.7–1.0 px	Good"
echo "    1.0–2.0 px	Acceptable"
echo "    2–3 px	    Maybe you should repeat"
echo "    >3 px         Maybe there is problem inside"
