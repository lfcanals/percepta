#!/bin/bash

cameraId=$1


cd target
python3 tools/select-eye-fish-calibration.py ../database/${cameraId}
cd ..

