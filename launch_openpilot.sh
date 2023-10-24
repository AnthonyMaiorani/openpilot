#!/usr/bin/bash

export PASSIVE="0"
export FINGERPRINT="HONDA ACCORD 2018"
echo -en "0.2.0" > /data/params/d/CompletedTrainingVersion
echo -en "2" > /data/params/d/HasAcceptedTerms
echo -en "1" > /data/params/d/dp_api_custom
exec ./launch_chffrplus.sh