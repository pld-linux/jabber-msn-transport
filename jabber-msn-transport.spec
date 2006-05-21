Summary:	MSN transport module for Jabber
Summary(pl):	Modu³ transportowy MSN dla systemu Jabber
Name:		jabber-msn-transport
Version:	1.2.8rc1
Release:	6
License:	distributable
Group:		Applications/Communications
Source0:	http://msn-transport.jabberstudio.org/msn-transport-%{version}.tar.gz
# Source0-md5:	832ac9fba617f11462c6457eacf4009a
Source2:	jabber-msntrans.init
Source3:	jabber-msntrans.sysconfig
Source4:	msntrans.xml
Patch0:		%{name}-curl-shared.patch
URL:		http://www.jabber.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	jabberd14-devel >= 1.4.3.1-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	jabber-common
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%requires_eq	jabberd14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with MSN servers.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami MSN.

%prep
%setup -qn msn-transport-%{version}
%patch0

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-pth=%{_includedir} \
	--with-curl-libs=%{_libdir} \
	--with-jabberd=/usr/include/jabberd14
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/jabberd14,%{_sysconfdir}/jabber} \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install src/msntrans.so $RPM_BUILD_ROOT%{_libdir}/jabberd14
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-msntrans
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabber-msntrans
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/jabber/msntrans.xml
ln -sf %{_sbindir}/jabberd14 $RPM_BUILD_ROOT%{_sbindir}/jabber-msntrans

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in the config file..."
		%{__sed} -i -e "s/>secret</>$SECRET</" %{_sysconfdir}/jabber/msntrans.xml
	fi
fi

/sbin/chkconfig --add jabber-msntrans
%service jabber-msntrans restart "Jabber msn transport"

%preun
if [ "$1" = "0" ]; then
	%service jabber-msntrans stop
	/sbin/chkconfig --del jabber-msntrans
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/jabberd14/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-msntrans
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jabber-msntrans
