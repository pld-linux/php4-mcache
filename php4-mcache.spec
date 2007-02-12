%define		_name		mcache
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

%define		_beta	beta10
%define		_rel	2
Summary:	mcache PHP Extension
Summary(pl.UTF-8):   Rozszerzenie PHP mcache
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
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Requires(post,preun):	php-common >= 3:4.1
Requires:	%{_sysconfdir}/conf.d
Conflicts:	php4-pecl-memcache
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

%description -l pl.UTF-8
mcache to rozszerzenie PHP, którego celem jest umożliwienie
programistom łatwo i wydajnie cache'ować ane w serwerach Memcached.

Rozszerzenie PHP mcache zostało stworzone przez Johna McCaskeya i jest
wrapperem na libmemcache.

Głównymi zaletami używania tego rozszerzenia mcache nad innymi
rozszerzeniami PHP są szybkość oraz funkcjonalność. Wcześniej istniało
kilka różnych API memcache dla PHP. Kilka z nich było dobrych pod
względem funkcjonalności, ale wolnych ze względu na natywną
implementację w PHP. Rozszerzenie PECL miało znakomitą szybkość (choć
nie tak dobrą jak mcache), ale nie obsługiwało wielu serwerów
Użytkownicy byli zmuszeni do wybierania między szybkością a
funkcjonalnością. Wraz z wprowadzeniem tego nowego rozszerzenia
problem przestał istnieć. Co więcej, ponieważ to rozszerzenie jest
oparte na libmemcache, będzie łatwo korzystać z każdego testowania,
poprawek błędów czy rozszerzeń dokonanych w tej bibliotece.

%prep
%setup -q -n php-%{_name}-ext-%{version}%{?_beta:-%{_beta}}
cp %{SOURCE1} example.php

%build
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
