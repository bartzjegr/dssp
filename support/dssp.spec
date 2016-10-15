%global commit0 76059b5515178a02b8f229d7bd592cb496c7419e
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 c06d926f738544fb8f58ec7076022eda4289a94d
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%define POLICYVER 30
%define POLICYCOREUTILSVER 2.6

%if %{?BUILD_STANDARD:0}%{!?BUILD_STANDARD:1}
%define BUILD_STANDARD 1
%endif

%if %{?BUILD_MCS:0}%{!?BUILD_MCS:1}
%define BUILD_MCS 1
%endif

Summary: Defensec SELinux Security Policy
Name: dssp
Version: 0.4
Release: %(date +%Y%%m%%d)git%{shortcommit0}%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: https://github.com/Defensec/dssp/archive/%{commit0}/dssp-%{commit0}.tar.gz
Source1: https://github.com/Defensec/dssp-contrib/archive/%{commit1}/dssp-contrib-%{commit1}.tar.gz
URL: https://github.com/Defensec/dssp/wiki
Requires: policycoreutils
BuildRequires: policycoreutils >= %{POLICYCOREUTILSVER}
BuildArch: noarch

%description
SELinux security policy with a strong focus on flexibility and accessibility.
Provides Defensec SELinux Security Policy base package.

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux

%define fileList() \
%defattr(-,root,root,-) \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/logins \
%dir %{_sharedstatedir}/selinux/%1/active \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/semanage.read.LOCK \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/semanage.trans.LOCK \
%dir %attr(700,root,root) %dir %{_sharedstatedir}/selinux/%1/active/modules \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/100 \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/openssh_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/media \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs_dist \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.bin \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs.bin \
%{_sharedstatedir}/selinux/%1/active/commit_num \
%{_sharedstatedir}/selinux/%1/active/users_extra \
%{_sharedstatedir}/selinux/%1/active/homedir_template \
%{_sharedstatedir}/selinux/%1/active/seusers \
%{_sharedstatedir}/selinux/%1/active/file_contexts \
%{_sharedstatedir}/selinux/%1/active/policy.kern \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/exempt.id \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/gdm.id \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/sysadm.id \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/wheel.id \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user.id \
%nil

%if %{BUILD_STANDARD}
%package standard
Summary: Standard Defensec SELinux Security Policy
Group: System Environment/Base
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): dssp = %{version}-%{release}
Requires: dssp = %{version}-%{release}

%description standard
SELinux security policy with a strong focus on flexibility and accessibility.
Provides Defensec SELinux Security Policy standard package.

%files standard
%fileList dssp-standard
%endif

%if %{BUILD_MCS}
%package mcs
Summary: MCS Defensec SELinux Security Policy
Group: System Environment/Base
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): dssp = %{version}-%{release}
Requires: dssp = %{version}-%{release}

%description mcs
SELinux security policy with a strong focus on flexibility and accessibility.
Provides Defensec SELinux Security Policy MCS package.

%files mcs
%fileList dssp-mcs
%endif

%prep
%autosetup -n dssp-%{commit0}
%autosetup -n dssp-%{commit0} -a 1
rmdir sources/modules/contrib
mv -f dssp-contrib-%{commit1} sources/modules/dssp-contrib

%build

%install

%if %{BUILD_STANDARD}
# FIXME
sed -i 's/(tunable enable_rbacsep true)/(tunable enable_rbacsep false)/' sources/global_tunables.cil
sed -i 's/(tunable enable_mcs true)/(tunable enable_mcs false)/' sources/global_tunables.cil
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-standard/logins
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts
install -m0644 contexts/customizable_types.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/customizable_types
install -m0644 contexts/securetty_types.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/securetty_types
install -m0644 contexts/dbus_contexts %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/dbus_contexts
install -m0644 contexts/default_contexts.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/default_contexts
install -m0644 contexts/default_type.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/default_type
install -m0644 contexts/failsafe_context.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/failsafe_context
install -m0644 contexts/openssh_contexts %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/openssh_contexts
# FIXME: need to deal with no-rbacsep scenario
cat > contexts/removable_context.standard <<EOF
sys.id:object_r:removable_fs.fs
EOF
install -m0644 contexts/removable_context.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/removable_context
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/files
# FIXME: need to deal with no-rbacsep scenario
cat > contexts/files/media.standard <<EOF
cdrom sys.id:object_r:removable_storage.storage_dev
floppy sys.id:object_r:removable_storage.storage_dev
disk sys.id:object_r:removable_storage.storage_dev
EOF
install -m0644 contexts/files/media.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/files/media
install -m0644 contexts/files/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/files/file_contexts.subs_dist
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/users
install -m0644 contexts/users/exempt.id.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/users/exempt.id
install -m0644 contexts/users/gdm.id.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/users/gdm.id
install -m0644 contexts/users/sysadm.id.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/users/sysadm.id
install -m0644 contexts/users/wheel.id.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/users/wheel.id
install -m0644 contexts/users/user.id.standard %{buildroot}%{_sysconfdir}/selinux/dssp-standard/contexts/users/user.id
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/selinux
semodule -p %{buildroot} --priority=100 \
	-i `/bin/find ./sources -type f \( -iname "*.cil" \) | /bin/cut -d/ -f2-` \
	-N -s dssp-standard
%endif

%if %{BUILD_MCS}
# FIXME
sed -i 's/(tunable enable_rbacsep false)/(tunable enable_rbacsep true)/' sources/global_tunables.cil
sed -i 's/(tunable enable_mcs false)/(tunable enable_mcs true)/' sources/global_tunables.cil
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/logins
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts
install -m0644 contexts/customizable_types.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/customizable_types
install -m0644 contexts/securetty_types.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/securetty_types
install -m0644 contexts/dbus_contexts %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/dbus_contexts
install -m0644 contexts/default_contexts.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/default_contexts
install -m0644 contexts/default_type.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/default_type
install -m0644 contexts/failsafe_context.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/failsafe_context
install -m0644 contexts/openssh_contexts %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/openssh_contexts
install -m0644 contexts/removable_context.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/removable_context
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/files
install -m0644 contexts/files/media.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/files/media
install -m0644 contexts/files/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/files/file_contexts.subs_dist
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/users
install -m0644 contexts/users/exempt.id.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/users/exempt.id
install -m0644 contexts/users/gdm.id.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/users/gdm.id
install -m0644 contexts/users/sysadm.id.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/users/sysadm.id
install -m0644 contexts/users/wheel.id.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/users/wheel.id
install -m0644 contexts/users/user.id.mcs %{buildroot}%{_sysconfdir}/selinux/dssp-mcs/contexts/users/user.id
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/selinux
semodule -p %{buildroot} --priority=100 \
	-i `/bin/find ./sources -type f \( -iname "*.cil" \) | /bin/cut -d/ -f2-` \
	-N -s dssp-mcs
%endif

%clean
rm -rf %{buildroot}

%post standard
if [ ! -s /etc/selinux/config ]; then
echo "
SELINUX=enforcing
SELINUXTYPE=dssp-standard
" > /etc/selinux/config

	ln -sf /etc/selinux/config /etc/sysconfig/selinux
	restorecon /etc/selinux/config 2> /dev/null || :
else
	. /etc/selinux/config
	[ "${SELINUXTYPE}" == "dssp-standard" ] && selinuxenabled && load_policy
fi
exit 0

%post mcs
if [ ! -s /etc/selinux/config ]; then
echo "
SELINUX=enforcing
SELINUXTYPE=dssp-mcs
" > /etc/selinux/config

	ln -sf /etc/selinux/config /etc/sysconfig/selinux
	restorecon /etc/selinux/config 2> /dev/null || :
else
	. /etc/selinux/config
	[ "${SELINUXTYPE}" == "dssp-mcs" ] && selinuxenabled && load_policy
fi
exit 0

%postun
if [ $1 = 0 ]; then
	setenforce 0 2> /dev/null
	if [ ! -s /etc/selinux/config ]; then
		echo "SELINUX=disabled" > /etc/selinux/config
	else
		sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
	fi
fi
exit 0

%triggerin -- pcre2
selinuxenabled && semodule -nB

%changelog
* Sat Oct 15 2016 Dominick Grift <dac.override@gmail.com> - 0.4-%(date +%Y%%m%%d)git%{shortcommit0}
- Git snapshot
