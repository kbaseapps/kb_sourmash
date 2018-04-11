#!/bin/bash

. /kb/deployment/user-env.sh

python ./scripts/prepare_deploy_cfg.py ./deploy.cfg ./work/config.properties

if [ -f ./work/token ] ; then
  export KB_AUTH_TOKEN=$(<./work/token)
fi

if [ $# -eq 0 ] ; then
  sh ./scripts/start_server.sh
elif [ "${1}" = "test" ] ; then
  echo "Run Tests"
  make test
elif [ "${1}" = "async" ] ; then
  ls -l /data
  sh ./scripts/run_async.sh
elif [ "${1}" = "init" ] ; then
  echo "Initialize module"
  cd /data
  echo "Getting databases"
  curl -O https://s3-us-west-1.amazonaws.com/spacegraphcats.ucdavis.edu/microbe-genbank-sbt-k31-2017.05.09.tar.gz
  tar xzf microbe-genbank-sbt-k31-2017.05.09.tar.gz
  curl -O ftp://ftp.kbase.us/sourmash_data/img_arch_isol.tar.gz
  tar xzf img_arch_isol.tar.gz
  curl -O ftp://ftp.kbase.us/sourmash_data/img_arch_mags.tar.gz
  tar xzf img_arch_mags.tar.gz
  curl -O ftp://ftp.kbase.us/sourmash_data/img_arch_sags.tar.gz
  tar xzf img_arch_sags.tar.gz
  curl -O ftp://ftp.kbase.us/sourmash_data/img_bact_isol.tar.gz
  tar xzf img_bact_isol.tar.gz
  curl -O ftp://ftp.kbase.us/sourmash_data/img_bact_sags.tar.gz
  tar xzf img_bact_sags.tar.gz
  curl -O ftp://ftp.kbase.us/sourmash_data/img_bact_mags.tar.gz
  tar xzf img_bact_mags.tar.gz
  curl -o genbank-k31.lca.json.gz "https://files.osf.io/v1/resources/vk4fa/providers/osfstorage/5a02520e594d90026566b698?action=download&amp;version=1&amp;direct"
  gunzip genbank-k31.lca.json.gz
  echo '[' > .dotfiles
  echo '{"name":".sbt.genbank-k31", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ',{"name":".sbt.img_arch_isol", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ',{"name":".sbt.img_arch_mags", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ',{"name":".sbt.img_arch_sags", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ',{"name":".sbt.img_bact_isol", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ',{"name":".sbt.img_bact_mags", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ',{"name":".sbt.img_bact_sags", "type":"directory","mtime":"1", "size":1}' >> .dotfiles
  echo ']' >> .dotfiles
  if [[ -d ".sbt.genbank-k31" && -d ".sbt.img_arch_isol" && -d ".sbt.img_bact_mags" ]] ; then
    touch __READY__
  else
    echo "init failed"
  fi
elif [ "${1}" = "bash" ] ; then
  bash
elif [ "${1}" = "report" ] ; then
  export KB_SDK_COMPILE_REPORT_FILE=./work/compile_report.json
  make compile
else
  echo Unknown
fi
