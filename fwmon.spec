%define name fwmon
%define version 1.1.0
%define release  %mkrel 10

Summary: A linux netlink firewall monitor
Name: %name
Version: %version
Release: %release
License: GPL
Group: System/Servers
Source: %name-%{version}.tar.bz2
# http://qa.mandriva.com/show_bug.cgi?id=36213
Patch: fwmon-1.1.0-mb.patch
BuildRoot: %_tmppath/%{name}-buildroot
Buildrequires: libpcap-devel
Url: http://www.scaramanga.co.uk/fwmon/

%description
This program allows you to monitor ipchains/iptables output in realtime.
It  supports both logging to a file/stdout and/or to tcpdump format
capture logs. It also supports security features such as running
non-root, and chrooting itself.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch -p1 -b .mb

%build

%make

%install
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/logrotate.d
mkdir -p $RPM_BUILD_ROOT%_sbindir
mkdir -p $RPM_BUILD_ROOT%_mandir/man8/
install --strip -m 500 fwmon $RPM_BUILD_ROOT%_sbindir/fwmon
install -m 644 fwmon.8 $RPM_BUILD_ROOT%_mandir/man8/fwmon.8
install -m 644 logrotate.fwmon $RPM_BUILD_ROOT%_sysconfdir/logrotate.d/fwmon

%post

# Add the fwmon user
adduser -d /var/log/fwmon -s /bin/false -M fwmon 2>/dev/null || true

# Add the fwmon directory if it isnt already there
if [ ! -d /var/log/fwmon ]; then
	mkdir /var/log/fwmon
	chown fwmon.fwmon /var/log/fwmon
	chmod 700 /var/log/fwmon
fi

# Add a line to init
F_UID=`id -u fwmon`
F_GID=`id -g fwmon`
INITLINE="fw:2345:respawn:fwmon -sa -l /fwmon.log -t /fwmon.cap -u $F_UID -g $F_GID -c /var/log/fwmon"
echo "#$INITLINE" >> /etc/inittab

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root)
%config(noreplace) %_sysconfdir/logrotate.d/fwmon

%defattr(0755,root,root)
%_sbindir/fwmon

%defattr(644,root,root,755)
%doc README README.2nd README.chroot COPYING
%doc initdb.sql
%_mandir/man8/*



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-10mdv2011.0
+ Revision: 618385
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 1.1.0-9mdv2010.0
+ Revision: 428980
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.1.0-8mdv2009.0
+ Revision: 245575
- rebuild

* Wed Jan 09 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.1.0-6mdv2008.1
+ Revision: 147307
- Added patch to address http://qa.mandriva.com/show_bug.cgi?id=36213,
  /usr/include/asm/system.h header doesn't exist anymore. It isn't a bug
  in kernel headers exported to userspace, since system.h includes linux
  spefic code (like alternatives patching), and also I think isn't task
  of linux kernel to define generic macros for userspace to use, like
  mb. So define our own version of mb, the same way/based on
  /usr/include/alsa/iatomic.h from alsa-lib (libalsa2-devel).

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - fix kernel require
    - BR kernel-server-devel-latest for asm/system.h
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - import fwmon


* Thu Jul 07 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.1.0-5mdk
- rebuild

* Wed Jun 02 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.1.0-4mdk
- 1.1.0

* Tue Apr 29 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.1.0-3mdk
- buildrequires

* Thu Jan 30 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.1.0-2mdk
- rebuild

* Fri Feb 15 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.1.0-1mdk
- 1.1.0

* Wed Feb 13 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.11-1mdk
- 1.0.11

* Fri Jan 25 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.10-1mdk
- 1.0.10

* Thu Jan 10 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.9-1mdk
- 1.0.9

* Wed Oct 10 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.0.7-1mdk
- new in contribs
