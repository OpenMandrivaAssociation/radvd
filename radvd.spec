Summary:	The IPv6 Router Advertisement Daemon
Name:		radvd
Version:	1.6
Release:	%mkrel 3
License:	BSD
Group:		System/Servers
URL:		http://v6web.litech.org/radvd/
Source0:	http://v6web.litech.org/radvd/dist/%{name}-%{version}.tar.gz
Source1:	radvd.init
Source2:	radvd.conf
Source3:	radvd.sysconfig
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	flex bison
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
IPv6 has a lot more support for autoconfiguration than IPv4. But
for this autoconfiguration to work on the hosts of a network, the
routers of the local network have to run a program which answers
the autoconfiguration requests of the hosts.

On Linux this program is called radvd, which stands for Router
ADVertisement Daemon. This daemon listens to router solicitations (RS)
and answers with router advertisement (RA). Furthermore unsolicited
RAs are also send from time to time.

These RAs contain information, which is used by hosts to configure
their interfaces. This information includes address prefixes, the MTU of
the link and information about default routers.

%prep

%setup -q
cp %{SOURCE1} radvd.init
cp %{SOURCE2} radvd.conf
cp %{SOURCE3} radvd.sysconfig

%build
%serverbuild
%configure2_5x
%make


%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}

install -m0644 radvd.conf %{buildroot}%{_sysconfdir}/radvd.conf
install -m0644 radvd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/radvd
install -m0755 radvd.init %{buildroot}%{_initrddir}/radvd
perl -pi -e "s|/etc/rc.d/init\.d|%{_initrddir}|" %{buildroot}%{_initrddir}/*

%clean
rm -rf %{buildroot}

%post
%_post_service radvd

%preun
%_preun_service radvd
 
%files
%defattr(-,root,root)
%doc CHANGES COPYRIGHT README TODO INTRO.html radvd.conf.example
%config(noreplace) %{_sysconfdir}/radvd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/radvd
%{_initrddir}/radvd
%{_sbindir}/*
%{_mandir}/*/*
