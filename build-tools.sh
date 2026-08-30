#!/bin/bash

function copyModule() {
    module=$1
    mkdir -p target/tools/${module}
    cp -r src/main/${module}/* target/tools/${module}
}


mkdir -p target/tools
cp src/tools/*.py target/tools

for a in camera bus recording calibration realtime; do
    copyModule $a
done



