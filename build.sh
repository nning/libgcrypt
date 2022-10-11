#!/bin/sh

set -e

sudo dnf install dnf-utils rpmdevtools

[ -d libgcrypt ] && {
    cd libgcrypt
    git pull
} || {
    git clone https://src.fedoraproject.org/rpms/libgcrypt.git
    cd libgcrypt
}

sudo yum-builddep libgcrypt.spec
spectool -gR libgcrypt.spec --define "_sourcedir $PWD"
rpmbuild -ba libgcrypt.spec --define "_sourcedir $PWD" --with brainpool

sudo dnf reinstall $(ls -t ~/rpmbuild/RPMS/x86_64/libgcrypt-1*.rpm | head -1)