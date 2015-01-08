Summary: ipcast VMOD for Varnish %{VARNISHVER}
Name: vmod-ipcast
Version: 1.2
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemons
Source0: https://github.com/lkarsten/libvmod-ipcast/archive/libvmod-ipcast-1.2.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: varnish > 3.0
BuildRequires: make, python-docutils

%description
ipcast VMOD for Varnish %{VARNISHVER}. Allows casting from a string to an
ip address object in VCL. Typical usage is checking an acl for
req.http.X-Forwarded-For

%prep
test -z "%{?VARNISHVER}" && echo Macro VARNISHVER not defined && exit 1
test -z "%{?VARNISHSRC}" && echo Macro VARNISHSRC not defined && exit 1

%setup -q -n libvmod-ipcast-%{version}
%build

# NOTE: Download and install THE EXACT SAME VERSION of varnish-libs and the
# varnish source in the build environment as the version you want to
# install this module on
#
# First sudo yum install varnish-libs
# Then get the varnish source rpm, and install it to your local rpmbuild tree
# Then rpmbuild -bb varnish.spec. ctrl-c it when it runs the tests, so you get
# a complete prebuilt tree (rpmbuild will clean up and delete the tree when
# a build succeeds)
#
# The following assumes that VARNISHSRC is defined on the rpmbuild
# command line, like this:
# rpmbuild -bb --define 'VARNISHSRC /home/user/rpmbuild/BUILD/varnish-3.0.3' redhat/*spec
#
# My build ons centos6 looks like this:
# rpmbuild --define "dist .el6" --define "VARNISHVER 3.0.6" --define "VARNISHSRC $HOME/rpmbuild/BUILD/varnish-3.0.6" -bb vmod-ipcast.spec

#./autogen.sh
./configure VARNISHSRC=%{VARNISHSRC} VMODDIR="$(PKG_CONFIG_PATH=%{VARNISHSRC} pkg-config --variable=vmoddir varnishapi)" --prefix=/usr
make
make check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/varnis*/vmods/
%{_mandir}/man?/*
%doc README.rst LICENSE

%changelog
* Thu Jan 08 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.2-1
- Clean up build for 1.2
- Update description for 1.2 (no longer access to client.ip)

* Wed Mar  5 2014 Lasse Karstensen <lkarsten@varnish-software.com> - 0.1-0.20140305
- Updated description to work better with Redhat Satellite.

* Tue Nov 14 2012 Lasse Karstensen <lasse@varnish-software.com> - 0.1-0.20121114
- Initial version.
