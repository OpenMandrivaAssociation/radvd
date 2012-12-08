Summary:	The IPv6 Router Advertisement Daemon
Name:		radvd
Version:	1.9.1
Release:	1
License:	BSD
Group:		System/Servers
URL:		http://v6web.litech.org/radvd/
Source0:	http://v6web.litech.org/radvd/dist/%{name}-%{version}.tar.gz
Source1:	radvd-tmpfs.conf
Source2:	radvd.service
Source3:	radvd.conf
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	flex bison
BuildRequires:	pkgconfig(libdaemon)

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
%configure2_5x --with-pidfile=%{_localstatedir}/run/radvd/radvd.pid
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


%changelog
* Fri Jun 29 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.9.1-1
+ Revision: 807518
- version update 1.9.1

* Mon Mar 26 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.8.5-1
+ Revision: 787125
- version update 1.8.5

* Sat Nov 05 2011 Alexander Khrukin <akhrukin@mandriva.org> 1.8.3-1
+ Revision: 721552
- version update to upstream

* Mon May 30 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8-1
+ Revision: 681821
- 1.8

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6-3
+ Revision: 669404
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6-2mdv2011.0
+ Revision: 607302
- rebuild

* Sat Mar 06 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.6-1mdv2010.1
+ Revision: 515236
- o update to 1.6
  o use %%configure2_5x

* Thu Aug 20 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4-1mdv2010.0
+ Revision: 418608
- update to new version 1.4

* Sat Jul 25 2009 Frederik Himpe <fhimpe@mandriva.org> 1.3-1mdv2010.0
+ Revision: 399841
- Update to new version 1.3

* Wed Mar 11 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2-1mdv2009.1
+ Revision: 353777
- 1.2
- bunzip initscripts and config
- sync with the bundled fedora stuff (use a %%{_sysconfdir}/sysconfig/radvd file)

* Sun Mar 02 2008 Pascal Terjan <pterjan@mandriva.org> 1.1-1mdv2008.1
+ Revision: 177747
- update to new version 1.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-2mdv2008.0
+ Revision: 90248
- rebuild

