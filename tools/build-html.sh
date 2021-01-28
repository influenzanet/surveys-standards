#!/bin/sh
git diff --exit-code $1
if [ $? -ne 0 ];
then
    echo "$1 has changed non commited please commit it before"
    exit 1
fi

NAME=$(git log -n 1 --pretty=format:%H -- $1)
./cli survey:show $1 --output=$2 --tag="$NAME"
