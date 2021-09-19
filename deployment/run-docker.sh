#!/bin/sh

# usage: run-docker.sh [path to wm code] [path to cerenaut-pt-core code] [boolean for GPU or not] [command and params to run in container]
# e.g.  deployment/run-docker.sh ~/Dev/WM_Hackathon ~/Dev/cerenaut-pt-core false python 
export WM_SRC_DIR=${1:-~/WM_Hackathon/WM_Hackathon}
export CORE_SRC_DIR=${2:-~/WM_Hackathon/cerenaut-pt-core}
export GPU=${3:-false}

shift
shift
shift

WM_TGT_DIR=/root/wm_hackathon
CORE_TGT_DIR=/root/cerenaut-pt-core
IMG_NAME=cerenaut/wbaiwmhackathon:latest

#if $GPU
#then
#	GPU_STR="--gpus all"
#fi

cmd="docker run --privileged -it --rm --name=wm $GPU_STR -e DISPLAY=$IP:0 -e XAUTHORITY=/.Xauthority -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/.Xauthority -v $WM_SRC_DIR:$WM_TGT_DIR -v $CORE_SRC_DIR:$CORE_TGT_DIR $IMG_NAME bash deployment/setupcore_and_run.sh $@"

#cmd="docker run --privileged --name=wm $GPU_STR  -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/.Xauthority -v $WM_SRC_DIR:$WM_TGT_DIR -v $CORE_SRC_DIR:$CORE_TGT_DIR $IMG_NAME"

echo $cmd
eval $cmd
