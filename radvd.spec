Summary:	The IPv6 Router Advertisement Daemon
Name:		radvd
Version:	2.17
Release:	3
License:	BSD
Group:		System/Servers
Url:		http://v6web.litech.org/radvd/
Source0:	http://v6web.litech.org/radvd/dist/%{name}-%{version}.tar.gz
Source1:	radvd-tmpfs.conf
Source2:	radvd.service
Source3:	radvd.conf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(libdaemon)
Requires(post,preun):	rpm-helper

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
for F in CHANGES; do
    iconv -f iso-8859-1 -t utf-8 < "$F" > "${F}.new"
    touch -r "$F" "${F}.new"
    mv "${F}.new" "$F"
done

%build
%serverbuild
%configure --with-pidfile=%{_localstatedir}/run/radvd/radvd.pid
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_localstatedir}/run/radvd
mkdir -p %{buildroot}%{_unitdir}

install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/radvd.conf
install -m 644 redhat/radvd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/radvd

install -d -m 755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/tmpfiles.d/radvd.conf
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

%pre
%_pre_useradd radvd / /sbin/nologin
%_pre_groupadd daemon radvd

%post
if [ "$1" = "1" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    /bin/systemctl enable radvd.service >/dev/null 2>&1 || :
fi

%postun
%_postun_groupdel daemon radvd
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart radvd.service >/dev/null 2>&1 || :
fi

%preun
if [ "$1" -eq 0 ]; then
   /bin/systemctl disable radvd.service > /dev/null 2>&1 || :
   /bin/systemctl stop radvd.service > /dev/null 2>&1 || :
fi
 
%files
%doc CHANGES COPYRIGHT INTRO.html README TODO
%{_unitdir}/radvd.service
%config(noreplace) %{_sysconfdir}/radvd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/radvd
%config(noreplace) %{_sysconfdir}/tmpfiles.d/radvd.conf
%dir %attr(-,radvd,radvd) %{_localstatedir}/run/radvd/
%doc radvd.conf.example
%{_mandir}/*/*
%{_sbindir}/radvd
%{_sbindir}/radvdump

