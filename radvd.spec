%define	name	radvd
%define	version	1.0
%define rel	2
%define	release	%mkrel %{rel}

Summary:	The IPv6 Router Advertisement Daemon
Url:		http://v6web.litech.org/radvd/
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Servers
Source0:	http://v6web.litech.org/radvd/dist/%{name}-%{version}.tar.bz2
Source1:	radvd-init.bz2
Source2:	radvd.conf.bz2
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
BuildRequires:	flex bison

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

%build
%serverbuild
%configure
%make


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/radvd.conf
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/radvd.conf

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/radvd
chmod 755 $RPM_BUILD_ROOT%{_initrddir}/radvd
perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*


%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service radvd

%preun
%_preun_service radvd
 
%files
%defattr(-,root,root)
%doc CHANGES COPYRIGHT README TODO INTRO.html radvd.conf.example
%config(noreplace) %{_sysconfdir}/radvd.conf
%{_initrddir}/radvd
%{_sbindir}/*
%{_mandir}/*/*


