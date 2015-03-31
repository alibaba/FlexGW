Name:      %{package_name}
Version:   %{version}
Vendor:    Flex GateWay Project
Release:   %{release}%{?dist}
Summary:   a vpn, snat web app for ecs.
License:   Commercial
Group:     Applications/Internet
Source0:   %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

AutoReqProv: no

%define __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}
%define  debug_package %{nil}

%description
a vpn, snat web app for ecs vpc vm.

%prep
%setup -q -b 0

%build
# install python
echo "building python..."
[ -f %{python_dir} ] && rm -rf %{python_dir}
export PYTHON_BUILD_BUILD_PATH=/tmp/rpmbuild/PYTHON/sources
export PYTHON_BUILD_CACHE_PATH=/tmp/rpmbuild/PYTHON/cache
python-build -k %{python_version} %{python_dir}

# install pip requirements.txt
echo "install requirements..."
export ac_cv_func_malloc_0_nonnull=yes
%{python_dir}/bin/pip install -r %{_builddir}/%{name}-%{version}/requirements.txt
unset ac_cv_func_malloc_0_nonnull

%install
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/usr/local/flexgw/
mkdir -p %{buildroot}%{python_dir}/

mv -fv %{_builddir}/%{name}-%{version}/scripts/initflexgw %{buildroot}/etc/init.d/initflexgw
cp -fv %{_builddir}/%{name}-%{version}/website_console %{buildroot}/etc/init.d/flexgw
cp -rv %{_builddir}/%{name}-%{version}/* %{buildroot}/usr/local/flexgw/
cp -rv %{python_dir}/* %{buildroot}%{python_dir}/

%post
# for upgrade
if [ $1 -gt 1 ]; then
    # db migrate
    SEED="$(date +%%Y%%m%%d%%H%%M%%S)"
    cp -fv "/usr/local/flexgw/instance/website.db" "/usr/local/flexgw/instance/website.db.${SEED}" &&
    /usr/local/flexgw/scripts/db-manage.py db upgrade --directory "/usr/local/flexgw/scripts/migrations" 1>/dev/null 2>&1 ||
    { echo "error: upgrade db failed."
      echo "backup db is: /usr/local/flexgw/instance/website.db.${SEED}"
      exit 1
    } >&2
    # update strongswan.conf
    cp -fv "/etc/strongswan/strongswan.conf" "/etc/strongswan/strongswan.conf.${SEED}" &&
    cp -fv "/usr/local/flexgw/rc/strongswan.conf" "/etc/strongswan/strongswan.conf" ||
    { echo "error: upgrade strongswan.conf failed."
      echo "backup strongswan.conf is: /etc/strongswan/strongswan.conf.${SEED}"
      exit 1
    }
fi

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf ${_builddir}
rm -rf %{buildroot}
rm -rf %{python_dir}

%files
%defattr(-,root,root)
/usr/local/flexgw/*
%attr(0755,root,root) /etc/init.d/*
%attr(0755,root,root) /usr/local/flexgw/scripts/*
%exclude /usr/local/flexgw/packaging
%exclude /usr/local/flexgw/requirements.txt
%exclude /usr/local/flexgw/develop.py
%config(noreplace) /usr/local/flexgw/instance/*

%changelog

* Mon Mar 23 2015 xiong.xiaox <xiong.xiaox@alibaba-inc.com> - 1.1.0
- Release 1.1

* Thu Aug 21 2014 xiong.xiaox <xiong.xiaox@alibaba-inc.com> - 1.0.0
- Release 1.0
