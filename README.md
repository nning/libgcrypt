# libgcrypt

Allow Brainpool curves in Fedora 35 Beta.

Fedora disabled Brainpool curves in libgcrypt for legal reasons. They patch
libgcrypt before building the RPM package, so it is not a solution to allow
Brainpool curves in the system-wide crypto policy.

See https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/WUQNAB4EPWSJMMVECL2TZGKB5KIDESII/

## Upstream

    https://src.fedoraproject.org/rpms/libgcrypt.git

## Build & Install for x86_64

    sudo yum-builddep libgcrypt.spec
    spectool -gR libgcrypt.spec --define "_sourcedir $PWD"
    rpmbuild -ba libgcrypt.spec --define "_sourcedir $PWD"
    sudo dnf reinstall ~/rpmbuild/RPMS/x86_64/libgcrypt-1.9.4-1.fc35.x86_64.rpm

## Build & Install for i686

    sudo dnf install mock
    sudo usermod -aG mock $USER
    newgrp -
    mock -r fedora-36-i386 ~/rpmbuild/SRPMS/libgcrypt-1.10.1-2.fc36.src.rpm
    sudo dnf install /var/lib/mock/fedora-36-i686/result/libgcrypt-1.10.1-2.fc36.i686.rpm ~/rpmbuild/RPMS/x86_64/libgcrypt-1.10.1-2.fc36.x86_64.rpm
