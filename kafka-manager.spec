%define __jar_repack 0
%define debug_package %{nil}
%define _prefix      /usr/share
%define _conf_dir    %{_sysconfdir}/%{name}
%define _log_dir     %{_var}/log/%{name}

Summary: A tool for managing Apache Kafka.

Name: kafka-manager
Version: 1.3.3.18
Release: 1
License: Apache License, Version 2.0
URL: http://kafka.apache.org/
Source0: %{name}-%{version}.zip
Source1: %{name}.service
Source2: %{name}.logrotate
Source3: logback.xml
Source4: %{name}.sysconfig
Source5: %{name}.tmpfiles
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Vendor: Yahoo Inc
Packager: Alexey Musev <musa@1c.ru>
Provides: kafka-manager
BuildRequires: systemd
%systemd_requires

%description
A tool for managing Apache Kafka.

%prep
%setup -q

%build
rm -f bin/*bat

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
mkdir -p $RPM_BUILD_ROOT/run

install -p -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 conf/* $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 $RPM_BUILD_ROOT/run/%{name}/
install -p -D -m 644 lib/* $RPM_BUILD_ROOT%{_prefix}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group kafka-manager >/dev/null || /usr/sbin/groupadd -r kafka-manager
if ! /usr/bin/getent passwd kafka-manager >/dev/null ; then
    /usr/sbin/useradd -r -g kafka-manager -M -d %{_prefix}/%{name} -s /sbin/nologin -c "kafka-manager user daemon" kafka-manager
fi

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun

%files
%defattr(-,root,root)
%attr(0750,kafka-manager,kafka-manager) %dir /run/%{name}/
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_conf_dir}/*
%{_prefix}/%{name}
%attr(0750,kafka-manager,kafka-manager) %dir %{_log_dir}
