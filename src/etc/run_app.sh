#! /bin/bash -l

SCRIPT_DIR=$(cd $(dirname $0); pwd -P)
UV=$HOME/.local/bin/uv

# run on src/ directory
cd $SCRIPT_DIR/../

$UV run -m app #> /dev/null 2>&1 
