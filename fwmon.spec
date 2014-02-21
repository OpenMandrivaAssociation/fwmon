Summary:	A linux netlink firewall monitor
Name:		fwmon
Version:	1.1.0
Release:	11
License:	GPLv2+
Group:		System/Servers
Url:		http://www.scaramanga.co.uk/fwmon/
Source0:	%{name}-%{version}.tar.bz2
# http://qa.mandriva.com/show_bug.cgi?id=36213
Patch0:		fwmon-1.1.0-mb.patch
Patch1:		fwmon-1.1.0-sfmt.patch
Buildrequires:	pcap-devel

%description
This program allows you to monitor ipchains/iptables output in realtime.
It  supports both logging to a file/stdout and/or to tcpdump format
capture logs. It also supports security features such as running
non-root, and chrooting itself.

%files
%defattr(0644,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/fwmon
%defattr(0755,root,root)
%{_sbindir}/fwmon
%defattr(644,root,root,755)
%doc README README.2nd README.chroot COPYING
%doc initdb.sql
%{_mandir}/man8/*

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

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .mb
%patch1 -p1

find . -perm 640 | xargs chmod 644

%build
%make CFLAGS="%{optflags} -D_HAVE_LIBPCAP -I/usr/include/pcap"

%install
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 500 fwmon %{buildroot}%{_sbindir}/fwmon
install -m 644 fwmon.8 %{buildroot}%{_mandir}/man8/fwmon.8
install -m 644 logrotate.fwmon %{buildroot}%{_sysconfdir}/logrotate.d/fwmon


