Name:      %{package_name}
Version:   %{version}
Vendor:    xiong.xiaox@alibaba-inc.com
Release:   %{release}%{?dist}
Url:       http://gitlab.alibaba-inc.com/xiong.xiaox/ecs-vpn
Summary:   a vpn, snat web for ecs.
License:   Commercial
Group:     Applications/Internet
Source0:   %{name}-%{version}.tar.bz2
Source1:   pyenv.tar.bz2
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

a vpn, snat web for ecs.

%prep
%setup -q -b 0
%setup -q -b 1 -c -n %{pyenv_build_dir}

%build
# set env
export PYENV_ROOT=%{pyenv_build_dir}/pyenv
%{pyenv_build_dir}/pyenv/bin/pyenv init -

# install python
echo "building pyenv"
%{pyenv_build_dir}/pyenv/bin/pyenv install %{py_version}
%{pyenv_build_dir}/pyenv/bin/pyenv rehash

# install pip requirements.txt
%{pyenv_build_dir}/pyenv/versions/%{py_version}/bin/pip install -r %{_builddir}/%{name}-%{version}/requirements.txt

%install
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/usr/local/ecs-vpn/
mkdir -p %{buildroot}/usr/local/ecs-vpn/pyenv/

cp -fv %{_builddir}/%{name}-%{version}/scripts/initecsvpn %{buildroot}/etc/init.d/initecsvpn
cp -fv %{_builddir}/%{name}-%{version}/website_console %{buildroot}/etc/init.d/ecsvpn
cp -rv %{_builddir}/%{name}-%{version}/* %{buildroot}/usr/local/ecs-vpn/
cp -rv %{pyenv_build_dir}/pyenv/* %{buildroot}/usr/local/ecs-vpn/pyenv/

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf ${_builddir}
rm -rf %{buildroot}
rm -rf %{pyenv_build_dir}

%files
%defattr(-,root,root)
/usr/local/ecs-vpn/*
%attr(0755,root,root) /etc/init.d/*
%attr(0755,root,root) /usr/local/ecs-vpn/scripts/*
%exclude /usr/local/ecs-vpn/packaging
%config(noreplace) /usr/local/ecs-vpn/instance/website.db
%doc README.md ChangeLog.md


%changelog

* Thu Aug 21 2014 xiong.xiaox <xiong.xiaox@alibaba-inc.com> - 1.0.0
- Release 1.0
