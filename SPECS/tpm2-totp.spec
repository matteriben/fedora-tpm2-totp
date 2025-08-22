Name:           tpm2-totp
Version:        0.3.0
Release:        1%{?dist}
Summary:        Time-based One-Time Passwords using TPM2

License:        BSD-3-Clause
URL:            https://github.com/tpm2-software/tpm2-totp
Source0:        https://github.com/tpm2-software/tpm2-totp/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/tpm2-software/tpm2-totp/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source2:        https://keys.openpgp.org/vks/v1/by-fingerprint/FE2E6249201CA54A4FB90D066E80CA1446879D04
Patch0:         0001-install-module-always.patch

%global dracutmodulesdir %{_prefix}/lib/dracut/modules.d

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  dracut
BuildRequires:  gcc
BuildRequires:  help2man
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pandoc
BuildRequires:  pkgconf
BuildRequires:  pkgconf-pkg-config
BuildRequires:  plymouth
BuildRequires:  plymouth-devel
BuildRequires:  qrencode-devel
BuildRequires:  tpm2-tools
BuildRequires:  tpm2-tss-devel
BuildRequires:  uthash-devel

Requires:       dracut
Requires:       qrencode
Requires:       tpm2-tools

%description
tpm2-totp is a utility that provides "remote attestation" via TOTP (Time-based
One-Time Passwords) securely using a TPM 2.0 device. It integrates with dracut
and Plymouth to provide "remote attestation" during early boot using your TPM.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%files devel
%{_includedir}/tpm2-totp.h
%{_libdir}/libtpm2-totp.so
%{_libdir}/pkgconfig/tpm2-totp.pc
%{_mandir}/man3/tpm2-totp.3.*

%prep
%autosetup -p0
gpg --no-default-keyring --keyring temp.gpg --import %{SOURCE2}
gpg --no-default-keyring --keyring temp.gpg --verify %{SOURCE1} %{SOURCE0}

%build
%set_build_flags
%configure --disable-static
make %{?_smp_mflags}

%check
make check

%undefine __brp_mangle_shebangs

%install
%make_install INSTALL="install -p"

%files
%dir %{_libexecdir}/tpm2-totp
%dir %{dracutmodulesdir}/70tpm2-totp
%{_bindir}/tpm2-totp
%{_libdir}/libtpm2-totp.so.0*
%{_libexecdir}/tpm2-totp/*
%{_mandir}/man1/tpm2-totp.1.*
%{dracutmodulesdir}/70tpm2-totp/*
%license LICENSE
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md INSTALL.md README.md dist/dracut/README

%changelog
* Fri Aug 15 2025 You <you@example.com> - 0.3.0-1
- Initial RPM package
