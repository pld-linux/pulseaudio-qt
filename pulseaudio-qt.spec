#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		pulseaudio-qt
Summary:	pulseaudio Qt
Name:		pulseaudio-qt
Version:	1.4.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/pulseaudio-qt/%{name}-%{version}.tar.xz
# Source0-md5:	741b7282572c5c013d1eb03dd9b7c701
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pulseaudio Qt.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-kcontacts-devel < 20.12.3

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.


%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF6PulseAudioQt.so.*.*
%ghost %{_libdir}/libKF6PulseAudioQt.so.4

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KF6PulseAudioQt
%{_includedir}/KF6/pulseaudioqt_version.h
%{_libdir}/cmake/KF6PulseAudioQt
%{_libdir}/libKF6PulseAudioQt.so
%{_pkgconfigdir}/KF6PulseAudioQt.pc
