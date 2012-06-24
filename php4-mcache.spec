%define		_name		mcache
%define		php_ver		%(rpm -q --qf '%%{epoch}:%%{version}' php4-devel)

%define		_beta	6
Summary:	mcache PHP Extension
Name:		php4-%{_name}
Version:	1.2.0
Release:	0.beta%{_beta}.1
Epoch:		0
License:	GPL
Group:		Development/Languages/PHP
Source0:	http://www.klir.com/~johnm/php-mcache/php-mcache-ext-%{version}-beta%{_beta}.tar.gz
# Source0-md5:	914b0272fe68d808ffa11edd741f2eae
URL:		http://www.klir.com/~johnm/php-mcache/
BuildRequires:	automake
BuildRequires:	libmemcache-devel >= 1.3.0
BuildRequires:	php4-devel
Requires:	php4-common = %{php_ver}
Requires(post,preun):	php-common >= 4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir)

%description
mcache is a PHP extension that aims to enable developers to easily and
efficiently cache data to Memcached servers.

The mcache php extension has been developed by John McCaskey and is a
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

%prep
%setup -q -n php-%{_name}-ext-%{version}%{?_beta:-beta%{_beta}}

%build
phpize
%{__aclocal}
%configure \
	--with-mcache \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php4-module-install install %{_name} %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php4-module-install remove %{_name} %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc README index.html
%doc mcache.php
%attr(755,root,root) %{extensionsdir}/mcache.so
