%define		_name		mcache
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

%define		_beta	beta10
%define		_rel	2
Summary:	mcache PHP Extension
Summary(pl):	Rozszerzenie PHP mcache
Name:		php4-%{_name}
Version:	1.2.0
Release:	0.%{_beta}.%{_rel}
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://www.klir.com/~johnm/php-mcache/php-mcache-ext-%{version}-%{_beta}.tar.gz
# Source0-md5:	b8c77e53d2c2af75411f574f7ed5e3b7
Source1:	php4-mcache.php
URL:		http://www.klir.com/~johnm/php-mcache/
BuildRequires:	libmemcache-devel >= 1.3.0
BuildRequires:	php4-devel
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires(post,preun):	php-common >= 3:4.1
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mcache is a PHP extension that aims to enable developers to easily and
efficiently cache data to Memcached servers.

The mcache PHP extension has been developed by John McCaskey and is a
wrapper around libmemcache.

The primary advantage to using this mcache extension over other PHP
extensions is speed, and functionality. Previously several PHP
memcache API's have existed. Several of these are very good
feature-wise, but very slow due to native PHP implementation. The PECL
extension has excellent speed (although not as good as mcache), but
does not support multiple servers. Users have been forced to choose
between speed and functionality. With the introduction of this new
extension that is no longer the case. Furthermore, because this
extension is based off libmemcache it will easily benefit from any
testing, bug fixes, or enhancements made to the underlying library.

%description -l pl
mcache to rozszerzenie PHP, którego celem jest umo¿liwienie
programistom ³atwo i wydajnie cache'owaæ ane w serwerach Memcached.

Rozszerzenie PHP mcache zosta³o stworzone przez Johna McCaskeya i jest
wrapperem na libmemcache.

G³ównymi zaletami u¿ywania tego rozszerzenia mcache nad innymi
rozszerzeniami PHP s± szybko¶æ oraz funkcjonalno¶æ. Wcze¶niej istnia³o
kilka ró¿nych API memcache dla PHP. Kilka z nich by³o dobrych pod
wzglêdem funkcjonalno¶ci, ale wolnych ze wzglêdu na natywn±
implementacjê w PHP. Rozszerzenie PECL mia³o znakomit± szybko¶æ (choæ
nie tak dobr± jak mcache), ale nie obs³ugiwa³o wielu serwerów
U¿ytkownicy byli zmuszeni do wybierania miêdzy szybko¶ci± a
funkcjonalno¶ci±. Wraz z wprowadzeniem tego nowego rozszerzenia
problem przesta³ istnieæ. Co wiêcej, poniewa¿ to rozszerzenie jest
oparte na libmemcache, bêdzie ³atwo korzystaæ z ka¿dego testowania,
poprawek b³êdów czy rozszerzeñ dokonanych w tej bibliotece.

%prep
%setup -q -n php-%{_name}-ext-%{version}%{?_beta:-%{_beta}}

%build
cp %{SOURCE1} example.php
phpize
%configure \
	--with-mcache \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_name}.ini
; Enable %{_name} extension module
extension=%{_name}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README index.html example.php
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{extensionsdir}/mcache.so
