#!/usr/bin/bash

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

if [ -z "$AGNOS_VERSION" ]; then
  export AGNOS_VERSION="9.1"
fi

if [ -z "$PASSIVE" ]; then
  export PASSIVE="1"
fi

export STAGING_ROOT="/data/safe_staging"

### dp_stock_begin ###
if [ -f /data/media/0/dp_nav_mapbox_token ]; then
  token=$(cat /data/media/0/dp_nav_mapbox_token)
  if [ "$token" != "" ]; then
    export MAPBOX_TOKEN=$token
  fi
fi
### dp_stock_end ###
