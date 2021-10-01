# libgcrypt

Allow Brainpool curves in Fedora 35 Beta.

Fedora disabled Brainpool curves in libgcrypt for legal reasons. They patch
libgcrypt before building the RPM package, so it is not a solution to allow
Brainpool curves in the system-wide crypto policy.

## Upstream

    https://src.fedoraproject.org/rpms/libgcrypt.git

## Setup

    sudo yum-builddep libgcrypt.spec
    spectool -gR libgcrypt.spec --define "_sourcedir $PWD"
    rpmbuild -ba libgcrypt.spec --define "_sourcedir $PWD"
    sudo dnf reinstall ~/rpmbuild/RPMS/x86_64/libgcrypt-1.9.4-1.fc35.x86_64.rpm
