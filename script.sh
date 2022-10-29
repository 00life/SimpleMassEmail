#!/bin/sh

list_py=$(ls|grep -e "\.py")
path_dir=$(pwd)

for i in $list_py; do
python3 "$path_dir/$i";
done
