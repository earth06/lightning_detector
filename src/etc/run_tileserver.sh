#! /bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd -P)

cd $SCRIPT_DIR/../../

uv run -m src.tileserver.run_tileserver > /dev/null 2>&1 & 
