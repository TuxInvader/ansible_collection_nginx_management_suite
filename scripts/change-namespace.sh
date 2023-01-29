#!/bin/bash

gitNS=nginxinc
newNS=tuxinvader
dirs="galaxy.yml plugins roles docs README.md"

if [ ! -d .git ]
then
    echo "This script should be run from the root directory of the source tree"
    exit 1
fi

case $1 in
  from-git)
    find $dirs -type f -exec sed -i -re "s/${gitNS}/${newNS}/g" {} \;
    ;;
  to-git)
    find $dirs -type f -exec sed -i -re "s/${newNS}/${gitNS}/g" {} \;
    ;;
  *)
    echo "Usage: $0 [to-git|from-git]"
esac

