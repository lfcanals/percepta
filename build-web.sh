#!/bin/bash

function copyModule() {
    module=$1
    mkdir -p target/web/${module}
    cp -r src/main/${module}/* target/web/${module}
}


mkdir -p target/web
cp -r src/web/* target/web

for a in camera bus recording calibration; do
    copyModule $a
done



