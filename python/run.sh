#!/bin/bash

SCRIPT='nm.py'

# layer 1
for C in {0..4}
do
  # python $SCRIPT $C 1 100000 &
  V=$(($C * 4))
  echo "layer 2 channel $V"
  python $SCRIPT $V 2 1000000 &
  echo "layer 2 channel $(($V+1))"
  python $SCRIPT $(($V+1)) 2 1000000 &
  echo "layer 2 channel $(($V+2))"
  python $SCRIPT $(($V+2)) 2 1000000 &
  echo "layer 2 channel $(($V+3))"
  python $SCRIPT $(($V+3)) 2 1000000 
done

# layer 2
for C in {0..8}
do
  V=$(($C * 4))
  echo "layer 2 channel $V"
  python $SCRIPT $V 2 10000000 &
  echo "layer 2 channel $(($V+1))"
  python $SCRIPT $(($V+1)) 2 10000000
  echo "layer 2 channel $(($V+2))"
  python $SCRIPT $(($V+2)) 2 10000000 &
  echo "layer 2 channel $(($V+3))"
  python $SCRIPT $(($V+3)) 2 10000000
done
