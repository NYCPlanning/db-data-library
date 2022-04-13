#!/bin/bash
function set_env {
  envfile=$1
    if [ -f $envfile ];
    then
        export $(cat $envfile | xargs)
        mc config host add spaces $AWS_S3_ENDPOINT $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY --api S3v4
    fi
}
# Set Environmental variables
set_env .env 

function get_version {
  local name=$1
  local config_path=spaces/edm-recipes/datasets/$name/latest/config.json
  local version=$(mc cat $config_path | jq -r '.dataset.version')
  echo "$version"
}

function import {
  local name=$1
  local version=${2:-latest} #default version to latest
  local dataset=
  echo "version: $version"
  
  local target_dir=$(pwd)/.library/datasets/$name
  # Download sql dump for the datasets from data library
  if [ -f $target_dir/$name.sql ]; then
    echo "✅ $name.sql exists in cache"
  else
    echo "🛠 $name.sql doesn't exists in cache, downloading ..."
    mkdir -p $target_dir && (
      cd $target_dir
      local url="spaces/edm-recipes/datasets/$name/$version/$name.sql"
      echo "url: $url"
      mc cp $url $target_dir/$name.sql
    )
  fi
  # Loading into Database
  psql $RECIPE_ENGINE -f $target_dir/$name.sql
}