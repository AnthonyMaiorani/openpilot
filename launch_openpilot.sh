#!/usr/bin/bash

export PASSIVE="0"
export FINGERPRINT="HONDA ACCORD 2018"
export SKIP_FW_QUERY=1
echo -en "HONDA ACCORD 2018" > /data/params/d/dp_car_assigned
exec ./launch_chffrplus.sh

