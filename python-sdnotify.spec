%global srcname sdnotify

Name:           python-%{srcname}
Version:        0.3.2
Release:        1%{?dist}
Summary:        A Python implementation of systemd's service notification protocol

License:        MIT
URL:            https://pypi.python.org/pypi/sdnotify
Source0:        %{pypi_source}
Source1:        https://raw.githubusercontent.com/bb4242/sdnotify/v%{version}/README.md

BuildArch:      noarch

%global _description %{expand:
systemd Service Notification

This is a pure Python implementation of the systemd sd_notify protocol. This
protocol can be used to inform systemd about service start-up completion,
watchdog events, and other service status changes. Thus, this package can be
used to write system services in Python that play nicely with systemd.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}
cp %{SOURCE1} .

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info
%{python3_sitelib}/%{srcname}/

%changelog
* Sun May 31 2020 Lars Kiesow <lkiesow@uos.de> - 0.3.2-1
- Initial build
