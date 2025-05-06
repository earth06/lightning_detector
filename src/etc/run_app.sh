#! /bin/bash -l

SCRIPT_DIR=$(cd $(dirname $0); pwd -P)
UV=$HOME/.local/bin/uv

cd $SCRIPT_DIR/../../

$UV run -m src.tileserver.run_tileserver > /dev/null 2>&1 & 
