## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global apiver  1
%global gtk_version 4.15.2
%global glib_version 2.76.0

%global tarball_version 1.6.2

Name:           libadwaita
Version:        1.6.6
Release:        %autorelease
Summary:        Building blocks for modern GNOME applications

# part of src/adw-spring-animation.c is MIT
License:        LGPL-2.1-or-later AND MIT
URL:            https://gitlab.gnome.org/GNOME/libadwaita
Source0:        https://download.gnome.org/sources/%{name}/1.6/%{name}-%{tarball_version}.tar.xz

# Backports for post-1.6.2. What would be patch 0004
# removed pre-generated CSS support making /usr/bin/sassc
# a build requirement that we cannot/will-not use.
Patch:          0001-dialog-Properly-unparent-the-child-when-backed-by-a-.patch
Patch:          0002-dialog-Handle-close-before-and-right-after-present.patch
Patch:          0003-bottom-sheet-Fix-more-criticals-on-dispose.patch
Patch:          0005-ci-Build-sysext.patch
Patch:          0006-ci-Do-releases-from-CI.patch
Patch:          0007-clamp-Fix-multi-child-support.patch
Patch:          0008-bottom-sheet-Fix-a-crash-when-closing-twice.patch
Patch:          0009-header-bar-Ignore-split-views-outside-sheets.patch
Patch:          0010-combo-row-Fix-property-notification.patch
Patch:          0011-button-row-Add-accessible-role-presentation.patch
Patch:          0012-action-row-Set-accessible-role-presentation.patch
Patch:          0013-length-unit-Also-fall-back-if-gtk-xft-dpi-is-default.patch
Patch:          0014-Release-1.6.3.patch
Patch:          0015-preferences-dialog-Document-navigation.pop.patch
Patch:          0016-tab-box-grid-Fix-scrolling-to-newly-appearing-tabs.patch
Patch:          0017-dialog-Fix-closed-emission-with-window-backed-dialog.patch
Patch:          0018-combo-row-Set-width-chars-1-for-the-item-labels.patch
Patch:          0019-tab-box-grid-Fix-a-copypaste-error.patch
Patch:          0020-Update-Italian-translation.patch
Patch:          0021-breakpoint-Make-sure-to_string-is-locale-agnostic.patch
Patch:          0022-dialog-always-clear-priv-last_focus-weak-pointer.patch
Patch:          0023-dialog-keep-a-weak-pointer-on-focus_widget.patch
Patch:          0024-Release-1.6.4.patch
Patch:          0025-dialog-notify-for-current-breakpoint-passed-through-.patch
Patch:          0026-preferences-dialog-window-Fix-the-search-filter-stac.patch
Patch:          0027-Release-1.6.5.patch
Patch:          0028-meson-Don-t-install-internal-static-library.patch
Patch:          0029-shadow-helper-Avoid-needlessly-reassigning-CSS-class.patch
Patch:          0030-toast-overlay-The-role-is-GROUP-not-TAB_GROUP.patch
Patch:          0031-docs-clarify-translator-credits-for-multiple-contrib.patch
Patch:          0032-Release-1.6.6.patch
Patch:          0033-Update-Portuguese-translation.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 0.59.0
BuildRequires:  vala
BuildRequires:  pkgconfig(appstream)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib_version}
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
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends:     gi-docgen-fonts

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
    -Dgtk_doc=true \
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
%{_libdir}/%{name}-%{apiver}.so.0*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*-%{apiver}.gir
%{_datadir}/vala/vapi/%{name}-%{apiver}.*
%{_includedir}/%{name}-%{apiver}/
%{_libdir}/%{name}-%{apiver}.so
%{_libdir}/pkgconfig/*-%{apiver}.pc

%files doc
%doc HACKING.md
%{_docdir}/%{name}-%{apiver}/

%files demo
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_metainfodir}/*.metainfo.xml


%changelog
## START: Generated by rpmautospec
* Tue Apr 29 2025 Christian Hergert <chergert@redhat.com> - 1.6.6-1
- Update to 1.6.6 with manual patching

* Mon Nov 04 2024 Christian Hergert <chergert@redhat.com> - 1.6.1-1
- Update to libadwaita 1.6.1

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 1.6.0-2
- Bump release for October 2024 mass rebuild:

* Fri Sep 27 2024 Christian Hergert <chergert@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Wed Sep 04 2024 Christian Hergert <chergert@redhat.com> - 1.6~rc-1
- Bump to libadwaita-1.6-rc

* Tue Jul 16 2024 Tomas Popela <tpopela@redhat.com> - 1.6~alpha-1
- Update to 1.6~alpha

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 1.5.1-4
- Bump release for June 2024 mass rebuild

* Wed Jun 12 2024 Christian Hergert <chergert@redhat.com> - 1.5.1-3
- Fix various openscan issues

* Fri Jun 07 2024 Tomas Pelka <tpelka@redhat.com> - 1.5.1-2
- Add gating.yaml via API

* Fri May 31 2024 Christian Hergert <chergert@redhat.com> - 1.5.1-1
- update to libadwaita-1.5.1

* Thu Apr 11 2024 Tomas Popela <tpopela@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Fri Feb 09 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5~beta-1
- Update to 1.5.beta

* Fri Feb 09 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.3-1
- Update to 1.4.3 (rhbz#2263525)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 02 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.2-1
- Update to 1.4.2 (rhbz#2252500)

* Fri Dec 01 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.1-1
- Update to 1.4.1 (rhbz#2252428)

* Tue Nov 14 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.0-7
- Rebuild against appstream-1.0

* Tue Nov 07 2023 Florian Müllner <fmuellner@gnome.org> - 1.4.0-6
- Drop sassc dependency

* Tue Nov 07 2023 Kalev Lember <klember@redhat.com> - 1.4.0-5
- Fix the build with appstream 1.0

* Mon Oct 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.4.0-4
- Restore URL

* Mon Oct 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.4.0-3
- Fix SPDX license list

* Sun Oct 08 2023 Miroslav Suchý <msuchy@redhat.com> - 1.4.0-2
- Migrate to SPDX license

* Fri Sep 15 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.0-1
- Update to 1.4.0 (rhbz#2239181)

* Sun Sep 03 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4~rc-1
- Update to 1.4.rc (rh#2237061)

* Fri Aug 04 2023 Kalev Lember <klember@redhat.com> - 1.4~beta-1
- Update to 1.4.beta

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Kalev Lember <klember@redhat.com> - 1.4~alpha-1
- Update to 1.4.alpha (rhbz#2219015)

* Fri Jun 09 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.3-1
- Update to 1.3.3 (rhbz#2213865)

* Tue May 09 2023 Niels De Graef <nielsdegraef@gmail.com> - 1.3.2-2
- libadwaita uses gettext instead of intltool

* Sat Apr 22 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Fri Mar 17 2023 David King <amigadave@amigadave.com> - 1.3.1-1
- Update to 1.3.1

* Sun Mar 05 2023 David King <amigadave@amigadave.com> - 1.3~rc-1
- Update to 1.3.rc

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 1.3~beta-1
- Update to 1.3.beta

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 1.3~alpha-1
- Update to 1.3.alpha

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.2.0-2
- Ensure correct fonts are installed for HTML docs

* Thu Sep 15 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Fri Sep 02 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2~rc-1
- Update to 1.2.rc

* Fri Aug 05 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2~beta-1
- Update to 1.2.beta

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Kalev Lember <klember@redhat.com> - 1.2~alpha-1
- Update to 1.2.alpha

* Wed Jun 01 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.2-1
- chore(update): 1.1.2

* Fri Apr 22 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.1-1
- chore(update): 1.1.1

* Fri Mar 18 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.0-1
- chore(update): 1.1.0

* Mon Mar 07 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1~rc-1
- chore(update): 1.1.rc

* Mon Feb 14 2022 David King <amigadave@amigadave.com> - 1.1~beta-1
- Update to 1.1.beta (#2053942)

* Sat Feb 12 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.2-1
- chore(update): 1.0.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 02 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.1-1
- chore(update): 1.0.1

* Sat Jan 01 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-1
- chore(update): 1.0.0-1

* Tue Dec 07 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.7.beta.1
- chore(update): 1.0.0-0.7.beta.1

* Tue Nov 02 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.6.alpha.4
- chore(update): 1.0.0-0.6.alpha.4
- build: Add Demo subpackage

* Fri Oct 01 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.5.alpha.3
- chore(update): 1.0.0-0.5.alpha.3

* Mon Aug 30 2021 Lyes Saadi <fedora@lyes.eu> - 1.0.0-0.4.alpha.2
- Updating to alpha.2

* Thu Jun 24 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.3.alpha.1
- Initial package

## END: Generated by rpmautospec
