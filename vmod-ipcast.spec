
%define         VARNISH     varnish
%define         VARNISHVER  3.0.5

Name:           varnish-libvmod-ipcast
Version:        0.1
Release:        3%{?dist}
Summary:        Varnish VMOD for casting IP addresses
License:        BSD
Group:          System Environment/Daemons
URL:            https://github.com/lkarsten/libvmod-ipcast
Source0:        https://github.com/lkarsten/libvmod-ipcast/archive/master.tar.gz
Source1:        http://repo.varnish-cache.org/source/%{VARNISH}-%{VARNISHVER}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64
# runtime requirements
Requires:       %{VARNISH} = %{VARNISHVER}
Requires:       %{VARNISH}-libs = %{VARNISHVER}

# Varnish build requirements
BuildRequires:  pcre-devel automake libtool pkgconfig ncurses-devel libxslt groff readline-devel
# ipcast build requirements
BuildRequires:  python-docutils

%description
The ipcast VMOD for Varnish %{VARNISHVER}. Allows assigning to client.ip from VCL.

%prep
%setup -n libvmod-ipcast
# to build a VMOD, we'll  need the compiled varnish source tree
# so we have to build varnish first
%setup -n libvmod-ipcast -D -T -a 1
cd %{VARNISH}-%{VARNISHVER}
%configure && %{__make} %{?_smp_mflags}
cd ..

%build
./autogen.sh
%{__chmod} +x configure
export VARNISHSRC=%{_builddir}/libvmod-ipcast/%{VARNISH}-%{VARNISHVER}
export VMODDIR=%{_libdir}/varnish/vmods
%configure
%{__make} %{?_smp_mflags}

%check
%{__make} check

%install
[ %{buildroot} != "/" ] && %{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
[ %{buildroot} != "/" ] && %{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/varnish/vmods/*
%doc README.rst LICENSE
%{_mandir}/man*/*

%changelog
* Fri Mar 14 2014 Martin Probst <github@megamaddin.org> - 0.1-3
- improved spec for automated build environments
- added ability to build against several varnish versions
- changed commands to macros

* Wed Mar  5 2014 Lasse Karstensen <lkarsten@varnish-software.com> - 0.1-0.20140305
- Updated description to work better with Redhat Satellite.

* Tue Nov 14 2012 Lasse Karstensen <lasse@varnish-software.com> - 0.1-0.20121114
- Initial version.
