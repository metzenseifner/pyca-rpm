%global srcname pyca
%define uid   pyca
%define gid   pyca
%define nuid  8967
%define ngid  8967

Name:           %{srcname}
Version:        4.1
Release:        1%{?dist}
Summary:        Python Capture Agent for Opencast

License:        LGPL
URL:            https://github.com/opencast/pyCA
%undefine _disable_source_fetch
Source0:        https://github.com/opencast/pyCA/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  npm
BuildRequires:  gcc-c++

#Requires:       python%{python3_pkgversion}-gunicorn
Requires:       python%{python3_pkgversion}-pycurl
Requires:       python%{python3_pkgversion}-dateutil
Requires:       python%{python3_pkgversion}-configobj
Requires:       python%{python3_pkgversion}-sqlalchemy
#Requires:       python%{python3_pkgversion}-sdnotify
Requires:       python%{python3_pkgversion}-flask

# needed for tests:
BuildRequires: python%{python3_pkgversion}-pycurl
BuildRequires: python%{python3_pkgversion}-dateutil
BuildRequires: python%{python3_pkgversion}-configobj
BuildRequires: python%{python3_pkgversion}-sqlalchemy
#BuildRequires: python%{python3_pkgversion}-sdnotify
BuildRequires: python%{python3_pkgversion}-flask
BuildRequires: python%{python3_pkgversion}-psutil

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
PyCA is a fully functional Opencast capture agent written in Python. It is free
software licensed under the terms of the GNU Lesser General Public License.

The goals of pyCA are to be…

- flexible for any kind of capture device
- simplistic in code and functionality
- nonrestrictive in terms of choosing capture software

PyCA can be run on almost any kind of devices: A regular PC equipped with
capture cards, a server to capture network streams, small boards or embedded
devices like the Raspberry Pi.

%prep
%autosetup -n pyCA-%{version}
yes | pip3 install sdnotify gunicorn

%build
npm ci
npm run build
%py3_build

%install
%py3_install

# Install Systemd unit file
install -dm 0755 %{buildroot}%{_unitdir}/
install -p -D -m 0644 init/systemd/*.service %{buildroot}%{_unitdir}/

# Install configuration
install -dm 0755 %{buildroot}%{_sysconfdir}/pyca/
install -p -D -m 0644 etc/gunicorn.conf.py %{buildroot}%{_sysconfdir}/pyca/
install -p -D -m 0600 etc/pyca.conf %{buildroot}%{_sysconfdir}/pyca/

# Data directory
install -dm 0755 %{buildroot}%{_sharedstatedir}/pyca/recordings
sed -i 's_#database *=.*$_database = sqlite://%{_sharedstatedir}/pyca/pyca.db_' \
   %{buildroot}%{_sysconfdir}/pyca/pyca.conf
sed -i 's_directory *=.*$_directory = %{_sharedstatedir}/pyca/recordings_' \
   %{buildroot}%{_sysconfdir}/pyca/pyca.conf
sed -i 's!#preview_dir *=.*$!#preview_dir = %{_sharedstatedir}/pyca/recordings!' \
   %{buildroot}%{_sysconfdir}/pyca/pyca.conf

%check
%{__python3} -m unittest discover -s tests
rm -r %{buildroot}%{python3_sitelib}/tests


%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -u %{nuid} -d /srv/opencast -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -d /srv/opencast -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi


%post
%systemd_post pyca-agentstate.service
%systemd_post pyca-capture.service
%systemd_post pyca-ingest.service
%systemd_post pyca-schedule.service
%systemd_post pyca-ui.service
%systemd_post pyca.service


%preun
%systemd_preun pyca-agentstate.service
%systemd_preun pyca-capture.service
%systemd_preun pyca-ingest.service
%systemd_preun pyca-schedule.service
%systemd_preun pyca-ui.service
%systemd_preun pyca.service


%postun
%systemd_postun_with_restart pyca-agentstate.service
%systemd_postun_with_restart pyca-capture.service
%systemd_postun_with_restart pyca-ingest.service
%systemd_postun_with_restart pyca-schedule.service
%systemd_postun_with_restart pyca-ui.service
%systemd_postun_with_restart pyca.service


%files
%license license.lgpl
%doc README.rst
%config(noreplace) %dir %{_sysconfdir}/%{srcname}
%config(noreplace) %{_sysconfdir}/%{srcname}/gunicorn.conf.py
%config(noreplace) %attr(600,%{uid},%{gid}) %{_sysconfdir}/%{srcname}/%{srcname}.conf
%{python3_sitelib}/%{srcname}-*.egg-info
%{python3_sitelib}/%{srcname}/
%{_bindir}/pyca
%{_unitdir}/pyca*.service
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/pyca


%changelog
* Tue Mar 02 2021 Lars Kiesow <lkiesow@uos.de> - 4.1-1
- Update to pyCA 4.1

* Tue Dec 01 2020 Lars Kiesow <lkiesow@uos.de> - 3.3-1
- Update to pyCA 3.3

* Sat Jul 18 2020 Lars Kiesow <lkiesow@uos.de> - 3.2-1
- Update to pyCA 3.2

* Sun Jun 21 2020 Lars Kiesow <lkiesow@uos.de> - 3.1-2
- Initial build
