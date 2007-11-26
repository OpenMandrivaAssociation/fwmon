%define name fwmon
%define version 1.1.0
%define release 5mdk

Summary: A linux netlink firewall monitor
Name: %name
Version: %version
Release: %release
License: GPL
Group: System/Servers
Source: %name-%{version}.tar.bz2
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

