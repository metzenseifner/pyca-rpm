FROM centos:8

# Install PyCA's repo
#ADD pyca.repo /etc/yum.repos.d/pyca.repo
COPY py_sdnotify.repo /etc/yum.repos.d/py_sdnotify.repo


RUN dnf install -y \
  make \
  rpm-build \
  sudo \
  'dnf-command(config-manager)' \
  'dnf-command(download)' \
  'dnf-command(builddep)' \
  rsync \
  rpmdevtools &&\
  groupadd rpmbuild &&\
  useradd -d /home/rpmbuild -g rpmbuild rpmbuild &&\
  # Make directory for build in shared location
  mkdir -p /base/build

#USER rpmbuild
#RUN mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
RUN rpmdev-setuptree
COPY pyca.spec /root/rpmbuild/SPECS/pyca.spec

# 1. Build
# 2. Test by installing and running
#    Remove any installed packages from previous docker-compose runs
# 3. Copy the RPMs back onto the host volume
CMD /base/pyca_rebuild.sh && \
    dnf remove -y pyca* && \
    dnf install -y ~/rpmbuild/RPMS/noarch/pyca* && \
    echo "==> TODO: Simulate running app here" && \
    mkdir -p /base/build/centos8 && \
    rsync --no-relative -vahu ~/rpmbuild/RPMS ~/rpmbuild/SRPMS /base/build/centos8/
