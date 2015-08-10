#!/bin/bash


#flexgw_refs="v1.0.0"
flexgw_refs="origin/develop"
package_name="flexgw"
flexgw_version="1.0.0"
flexgw_release="1"
python_version="2.7.9"
python_dir="/usr/local/flexgw/python"

curdir=$(pwd)

if [ ! -f ./mkrpm.sh ]; then
    echo "please run this script in directory where mkrpm.sh located in"
    exit 1
fi

#create necessary directories
mkdir -p /tmp/rpmbuild/SOURCES
mkdir -p /tmp/rpmbuild/PYTHON/cache
mkdir -p /tmp/rpmbuild/PYTHON/sources

[ -d /tmp/rpmbuild/SOURCES/flexgw ] && rm -rf /tmp/rpmbuild/SOURCES/flexgw

#clone repositories
git clone git@gitlab.alibaba-inc.com:netplatform/ecs-vpn.git /tmp/rpmbuild/SOURCES/flexgw

#archive source from git repositories
cd /tmp/rpmbuild/SOURCES/flexgw
git archive --format="tar" --prefix="$package_name-$flexgw_version/" $flexgw_refs|bzip2 > /tmp/rpmbuild/SOURCES/$package_name-$flexgw_version.tar.bz2

# rpmbuild
cd $curdir
rpmbuild --define "_topdir /tmp/rpmbuild" \
--define "package_name $package_name" \
--define "version $flexgw_version" \
--define "release $flexgw_release" \
--define "python_version $python_version" \
--define "python_dir $python_dir" \
-bb $curdir/flexgw.spec

rm -rf /tmp/rpmbuild/SOURCES
rm -rf /tmp/rpmbuild/BUILD
