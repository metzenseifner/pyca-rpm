#!/bin/sh
set -e

# Handle different package manager changes
if [ -x "$(command -v dnf)" ]; then
    pkgmanager="dnf"
    download_cmd="dnf download"
    builddep_cmd="dnf builddep"

    # For build dependencies: doxygen
    # dnf config-manager --enable powertools
else
    pkgmanager="yum"
    download_cmd="yumdownloader"
    builddep_cmd="yum-builddep"
fi

# Install SPEC dependencies before building
sudo $builddep_cmd -y ~/rpmbuild/SPECS/pyca.spec

# Build from SPEC
rpmbuild -ba ~/rpmbuild/SPECS/pyca.spec
