%global apiver  1
%global gtk_version 4.11.3

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:           libadwaita
Version:        1.4.2
Release:        2%{?dist}
Summary:        Building blocks for modern GNOME applications

# part of src/adw-spring-animation.c is MIT
License:        LGPL-2.1-or-later AND MIT
URL:            https://gitlab.gnome.org/GNOME/libadwaita
Source0:        https://download.gnome.org/sources/%{name}/1.4/%{name}-%{tarball_version}.tar.xz

Patch0:         0001-downgrade-glib-requirement-to-2_68.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 0.59.0
BuildRequires:  vala
BuildRequires:  pkgconfig(appstream)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk4) >= %{gtk_version}

Requires:       gtk4%{?_isa} >= %{gtk_version}

%description
Building blocks for modern GNOME applications.


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vala
Recommends:     %{name}-demo = %{version}-%{release}
Recommends:     %{name}-doc = %{version}-%{release}

%description    devel
Development files for %{name}.


%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

Recommends:     %{name}-devel = %{version}-%{release}

%description    doc
Documentation files for %{name}.


%package        demo
Summary:        Demo files for %{name}
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}
Suggests:       %{name}-devel = %{version}-%{release}

%description    demo
Demo files for %{name}.


%prep
%autosetup -p1 -n %{name}-%{tarball_version}


%build
%meson \
    -Dgtk_doc=false \
    %{nil}
%meson_build


%install
%meson_install
%find_lang %{name}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%license COPYING
%doc README.md AUTHORS NEWS
%{_bindir}/adwaita-%{apiver}-demo
%{_libdir}/*-%{apiver}.so.0*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*-%{apiver}.gir
%{_datadir}/vala/vapi/%{name}-%{apiver}.*
%{_includedir}/%{name}-%{apiver}/
%{_libdir}/*-%{apiver}.so
%{_libdir}/pkgconfig/*-%{apiver}.pc

%files doc
%doc HACKING.md

%files demo
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_metainfodir}/*.metainfo.xml


%changelog
* Tue Jan 2 2024 Tomas Popela <tpopela@redhat.com> - 1.42.2-2
- Add gating configuration (needs a new build)

* Thu Dec 7 2023 Tomas Popela <tpopela@redhat.com> - 1.42.2-1
- Initial RHEL packaging based on Fedora package with rpmautospec disabled,
  disabled documentation (no gi-docgen in RHEL 9) and downstream patch to
  be able to compile with glib2 2.68 (thanks to Milan Crha)
- Resolves: RHEL-3234
