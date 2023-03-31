%define major 12
%define libname %mklibname %{name}
%define devname %mklibname -d %{name}

%define majorpp 10
%define libnamepp %mklibname %{name}++
%define devnamepp %mklibname -d %{name}++
%global optflags %{optflags} -O3

%define lib32name lib%{name}
%define dev32name lib%{name}-devel
%define lib32namepp lib%{name}++
%define dev32namepp lib%{name}++-devel

# flac is used by audiofile, which is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

Summary:	An encoder/decoder for the Free Lossless Audio Codec
Name:		flac
Version:	1.4.2
Release:	2
License:	BSD and GPLv2+
Group:		Sound
Url:		http://flac.sourceforge.net/
Source0:	http://downloads.xiph.org/releases/flac/%{name}-%{version}.tar.xz
Patch0:		flac-1.3.3-no-Lusrlib.patch
BuildRequires:	libtool
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	gettext-devel
BuildRequires:	id3lib-devel
BuildRequires:	pkgconfig(ogg)
BuildRequires:	doxygen
%if %{with compat32}
BuildRequires:	devel(libogg)
%endif

%description
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

FLAC is comprised of 1) `libFLAC', a library which implements
reference encoders and decoders, licensed under the GNU Lesser
General Public License (LGPL); 2) `flac', a command-line program for
encoding and decoding files, licensed under the GNU General public
License (GPL); 3) `metaflac', a command-line program for editing
FLAC metadata, licensed under the GPL; 4) player plugins for XMMS
and Winamp, licensed under the GPL; and 5) documentation, licensed
under the GNU Free Documentation License.

%package -n %{libname}
Summary:	Shared libraries for FLAC
Group:		System/Libraries

%description  -n %{libname}
This package contains the C libraries.

%package -n %{devname}
Summary:	Libraries and headers needed for building apps using FLAC
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the libraries and header files necessary to develop
applications using FLAC written in C.

%package -n %{libnamepp}
Summary:	Shared C++ libraries for FLAC
Group:		System/Libraries

%description  -n %{libnamepp}
This package contains the libraries for C++ applications.

%package -n %{devnamepp}
Summary:	Libraries and headers needed for building apps using FLAC++
Group:		Development/C++
Requires:	%{libnamepp} = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}++-devel = %{version}-%{release}

%description -n %{devnamepp}
This package contains the libraries and header files necessary to develop
applications using FLAC written in C++.

%package -n %{lib32name}
Summary:	Shared libraries for FLAC (32-bit)
Group:		System/Libraries

%description  -n %{lib32name}
This package contains the C libraries.

%package -n %{dev32name}
Summary:	Libraries and headers needed for building apps using FLAC (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}

%description -n %{dev32name}
This package contains the libraries and header files necessary to develop
applications using FLAC written in C.

%package -n %{lib32namepp}
Summary:	Shared C++ libraries for FLAC (32-bit)
Group:		System/Libraries

%description  -n %{lib32namepp}
This package contains the libraries for C++ applications.

%package -n %{dev32namepp}
Summary:	Libraries and headers needed for building apps using FLAC++ (32-bit)
Group:		Development/C++
Requires:	%{lib32namepp} = %{version}-%{release}
Requires:	%{dev32name} = %{version}-%{release}
Requires:	%{devnamepp} = %{version}-%{release}

%description -n %{dev32namepp}
This package contains the libraries and header files necessary to develop
applications using FLAC written in C++.

%prep
export LC_ALL=C.utf-8
%autosetup -p1
./autogen.sh -V
autoreconf -fi

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
unset PKG_CONFIG_PATH
%endif

mkdir buildnative
cd buildnative
%configure \
	--disable-static \
	--disable-xmms-plugin \
	--disable-thorough-tests \
	--enable-asm-optimizations

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C buildnative

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C buildnative

%files
%doc AUTHORS COPYING*
%{_datadir}/doc/flac/FLAC.tag
%{_datadir}/doc/flac/images/logo*
%{_bindir}/flac
%{_bindir}/metaflac
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libFLAC.so.%{major}*

%files -n %{libnamepp}
%{_libdir}/libFLAC++.so.%{majorpp}*

%files -n %{devname}
%{_includedir}/FLAC
%{_libdir}/libFLAC.so
%{_datadir}/aclocal/libFLAC.m4
%{_libdir}/pkgconfig/flac.pc
%doc %{_docdir}/flac

%files -n %{devnamepp}
%{_includedir}/FLAC++
%{_libdir}/libFLAC++.so
%{_datadir}/aclocal/libFLAC++.m4
%{_libdir}/pkgconfig/flac++.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libFLAC.so.%{major}*

%files -n %{lib32namepp}
%{_prefix}/lib/libFLAC++.so.%{majorpp}*

%files -n %{dev32name}
%{_prefix}/lib/libFLAC.so
%{_prefix}/lib/pkgconfig/flac.pc

%files -n %{dev32namepp}
%{_prefix}/lib/libFLAC++.so
%{_prefix}/lib/pkgconfig/flac++.pc
%endif
