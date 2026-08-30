#!/bin/bash

cameraId=$1
numImages=$2

if [ "$numImages" == "" ]; then
  numImages=100
fi


pushd .
cd target
python3 tools/realtime-eye-fish-calibration.py $cameraId $numImages
popd
