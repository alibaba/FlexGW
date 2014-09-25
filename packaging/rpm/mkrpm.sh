#!/bin/bash

pyenv_refs="origin/master"
pyenv_build_dir="/usr/local/flexgw"
py_version="2.7.6"
#flexgw_refs="v1.0.0"
flexgw_refs="origin/develop"
flexgw_version="1.0.0"
flexgw_release="1"
package_name="flexgw"

curdir=$(pwd)

if [ ! -f ./mkrpm.sh ]; then
    echo "please run this script in directory where mkrpm.sh located in"
    exit 1
fi

#create necessary directories
mkdir -p /tmp/rpmbuild/SOURCES

[ -d /tmp/rpmbuild/SOURCES/pyenv ] && rm -rf /tmp/rpmbuild/SOURCES/pyenv
[ -d /tmp/rpmbuild/SOURCES/flexgw ] && rm -rf /tmp/rpmbuild/SOURCES/flexgw

#clone repositories
git clone git@gitlab.alibaba-inc.com:xiong.xiaox/pyenv.git /tmp/rpmbuild/SOURCES/pyenv
git clone git@gitlab.alibaba-inc.com:xiong.xiaox/ecs-vpn.git /tmp/rpmbuild/SOURCES/flexgw

#archive source from git repositories
cd /tmp/rpmbuild/SOURCES/pyenv
git archive --format="tar" --prefix="pyenv/" $pyenv_refs|bzip2 > /tmp/rpmbuild/SOURCES/pyenv.tar.bz2
cd /tmp/rpmbuild/SOURCES/flexgw
git archive --format="tar" --prefix="$package_name-$flexgw_version/" $flexgw_refs|bzip2 > /tmp/rpmbuild/SOURCES/$package_name-$flexgw_version.tar.bz2

cd $curdir
rpmbuild --define "_topdir /tmp/rpmbuild" --define "py_version $py_version" \
--define "package_name $package_name" --define "version $flexgw_version" \
--define "release $flexgw_release" --define "pyenv_build_dir $pyenv_build_dir" \
-bb $curdir/flexgw.spec

rm -rf /tmp/rpmbuild/SOURCES
rm -rf /tmp/rpmbuild/BUILD
