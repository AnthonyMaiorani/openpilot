#!/usr/bin/bash

export PASSIVE="0"
echo -en "0.2.0" > /data/params/d/CompletedTrainingVersion
echo -en "2" > /data/params/d/HasAcceptedTerms
exec ./launch_chffrplus.sh

