#!/bin/bash

pushd .

export BASE_FOLDER=`pwd`
mkdir $BASE_FOLDER/recordings 2> /dev/null
mkdir $BASE_FOLDER/database 2> /dev/null

cd target/web

python3 server.py $*

popd . 
