Summary: thttpd version 2.25b-r0
Name: thttpd
Version: 2.25b
Release: r0
License: BSD
Group: base
Packager: Teppei Asaba <teppeiasaba@jp.fujitsu.com>
URL: http://www.acme.com/software/thttpd/
Source0: thttpd-2.25b
Source1: thttpd-2.25b-r0-patched.tar.gz
Source2: acinclude.m4
Source3: install.patch
Source4: temp
BuildRequires: libtool-cross
BuildRequires: autoconf-native
BuildRequires: libtool-native
BuildRequires: shadow-native
BuildRequires: systemd-systemctl-native
BuildRequires: virtual/arm-ubinux-linux-gnueabi-compilerlibs
BuildRequires: virtual/arm-ubinux-linux-gnueabi-gcc
BuildRequires: gnu-config-native
BuildRequires: shadow-sysroot
BuildRequires: base-files
BuildRequires: virtual/libc
BuildRequires: shadow
BuildRequires: automake-native
Requires: rtld(GNU_HASH)
Requires: libc.so.6(GLIBC_2.7)
Requires: /bin/sh
Requires: base-files
Requires: base-passwd
Requires: libcrypt.so.1
Requires: libc6 >= 2.22
Requires: libcrypt.so.1(GLIBC_2.4)
Requires: shadow
Requires: libc.so.6
Requires: libc.so.6(GLIBC_2.4)
Requires(pre): rtld(GNU_HASH)
Requires(pre): libc.so.6(GLIBC_2.7)
Requires(pre): /bin/sh
Requires(pre): base-files
Requires(pre): base-passwd
Requires(pre): libcrypt.so.1
Requires(pre): libc6 >= 2.22
Requires(pre): libcrypt.so.1(GLIBC_2.4)
Requires(pre): shadow
Requires(pre): libc.so.6
Requires(pre): libc.so.6(GLIBC_2.4)
Provides: elf(buildid) = ba5d1aadd589fa2bd459e498170ea41efc225530
Provides: elf(buildid) = 4b38501761a367e3d0ff227b9c5f381e4d664d55
Provides: elf(buildid) = e0a9a4b556bcac8eaf33d371f76b951c8be643ff
Provides: elf(buildid) = 6c5607b245828c3d6970bf4357b31af9a684325b
Provides: elf(buildid) = 32e434174133a7655b72ad17b36413c607fc8d2b
Provides: elf(buildid) = 57fc8a93551aa668e43227e0c8493e85ab1f92d8

%description
A simple, small, portable, fast, and secure HTTP server.

%package -n thttpd-dbg
Summary: thttpd version 2.25b-r0 - Debugging files
Group: devel
Suggests: libc6-dbg

%description -n thttpd-dbg
A simple, small, portable, fast, and secure HTTP server.  This package
contains ELF symbols and related sources for debugging purposes.

%package -n thttpd-staticdev
Summary: thttpd version 2.25b-r0 - Development files (Static Libraries)
Group: devel
Requires: thttpd-dev = 2.25b-r0

%description -n thttpd-staticdev
A simple, small, portable, fast, and secure HTTP server.  This package
contains static libraries for software development.

%package -n thttpd-dev
Summary: thttpd version 2.25b-r0 - Development files
Group: devel
Requires: thttpd = 2.25b-r0
Suggests: shadow-sysroot-dev
Suggests: base-files-dev
Suggests: base-passwd-dev
Suggests: shadow-dev
Suggests: libc6-dev

%description -n thttpd-dev
A simple, small, portable, fast, and secure HTTP server.  This package
contains symbolic links, header files, and related items necessary for
software development.

%package -n thttpd-doc
Summary: thttpd version 2.25b-r0 - Documentation files
Group: doc

%description -n thttpd-doc
A simple, small, portable, fast, and secure HTTP server.  This package
contains documentation.

%package -n thttpd-locale
Summary: thttpd version 2.25b-r0
Group: base

%description -n thttpd-locale
A simple, small, portable, fast, and secure HTTP server.

%pre
# thttpd - preinst
#!/bin/sh
bbnote () {
	echo "NOTE: $*"
}
bbwarn () {
	echo "WARNING: $*"
}
bbfatal () {
	echo "ERROR: $*"
	exit 1
}
perform_groupadd () {
	local rootdir="$1"
	local opts="$2"
	local retries="$3"
	bbnote "thttpd: Performing groupadd with [$opts] and $retries times of retry"
	local groupname=`echo "$opts" | awk '{ print $NF }'`
	local group_exists="`grep "^$groupname:" $rootdir/etc/group || true`"
	if test "x$group_exists" = "x"; then
		local count=0
		while true; do
			eval $PSEUDO groupadd $opts || true
			group_exists="`grep "^$groupname:" $rootdir/etc/group || true`"
			if test "x$group_exists" = "x"; then
				bbwarn "thttpd: groupadd command did not succeed. Retrying..."
			else
				break
			fi
			count=`expr $count + 1`
			if test $count = $retries; then
				bbfatal "thttpd: Tried running groupadd command $retries times without success, giving up"
			fi
                        sleep $count
		done
	else
		bbnote "thttpd: group $groupname already exists, not re-creating it"
	fi
}
perform_useradd () {
	local rootdir="$1"
	local opts="$2"
	local retries="$3"
	bbnote "thttpd: Performing useradd with [$opts] and $retries times of retry"
	local username=`echo "$opts" | awk '{ print $NF }'`
	local user_exists="`grep "^$username:" $rootdir/etc/passwd || true`"
	if test "x$user_exists" = "x"; then
	       local count=0
	       while true; do
		       eval $PSEUDO useradd $opts || true
		       user_exists="`grep "^$username:" $rootdir/etc/passwd || true`"
		       if test "x$user_exists" = "x"; then
			       bbwarn "thttpd: useradd command did not succeed. Retrying..."
		       else
			       break
		       fi
		       count=`expr $count + 1`
		       if test $count = $retries; then
				bbfatal "thttpd: Tried running useradd command $retries times without success, giving up"
		       fi
		       sleep $count
	       done
	else
		bbnote "thttpd: user $username already exists, not re-creating it"
	fi
}
perform_groupmems () {
	local rootdir="$1"
	local opts="$2"
	local retries="$3"
	bbnote "thttpd: Performing groupmems with [$opts] and $retries times of retry"
	local groupname=`echo "$opts" | awk '{ for (i = 1; i < NF; i++) if ($i == "-g" || $i == "--group") print $(i+1) }'`
	local username=`echo "$opts" | awk '{ for (i = 1; i < NF; i++) if ($i == "-a" || $i == "--add") print $(i+1) }'`
	bbnote "thttpd: Running groupmems command with group $groupname and user $username"
	# groupmems fails if /etc/gshadow does not exist
	local gshadow=""
	if [ -f $rootdir/etc/gshadow ]; then
		gshadow="yes"
	else
		gshadow="no"
		touch $rootdir/etc/gshadow
	fi
	local mem_exists="`grep "^$groupname:[^:]*:[^:]*:\([^,]*,\)*$username\(,[^,]*\)*" $rootdir/etc/group || true`"
	if test "x$mem_exists" = "x"; then
		local count=0
		while true; do
			eval $PSEUDO groupmems $opts || true
			mem_exists="`grep "^$groupname:[^:]*:[^:]*:\([^,]*,\)*$username\(,[^,]*\)*" $rootdir/etc/group || true`"
			if test "x$mem_exists" = "x"; then
				bbwarn "thttpd: groupmems command did not succeed. Retrying..."
			else
				break
			fi
			count=`expr $count + 1`
			if test $count = $retries; then
				if test "x$gshadow" = "xno"; then
					rm -f $rootdir/etc/gshadow
					rm -f $rootdir/etc/gshadow-
				fi
				bbfatal "thttpd: Tried running groupmems command $retries times without success, giving up"
			fi
			sleep $count
		done
	else
		bbnote "thttpd: group $groupname already contains $username, not re-adding it"
	fi
	if test "x$gshadow" = "xno"; then
		rm -f $rootdir/etc/gshadow
		rm -f $rootdir/etc/gshadow-
	fi
}
OPT=""
SYSROOT=""

if test "x$D" != "x"; then
	# Installing into a sysroot
	SYSROOT="$D"
	OPT="--root $D"

	# Make sure login.defs is there, this is to make debian package backend work
	# correctly while doing rootfs.
	# The problem here is that if /etc/login.defs is treated as a config file for
	# shadow package, then while performing preinsts for packages that depend on
	# shadow, there might only be /etc/login.def.dpkg-new there in root filesystem.
	if [ ! -e $D/etc/login.defs -a -e $D/etc/login.defs.dpkg-new ]; then
	    cp $D/etc/login.defs.dpkg-new $D/etc/login.defs
	fi

	# user/group lookups should match useradd/groupadd --root
	export PSEUDO_PASSWD="$SYSROOT:/ubinux/ubinux16/build-armv7-lighttpd/tmp/sysroots/x86_64-linux"
fi

# If we're not doing a special SSTATE/SYSROOT install
# then set the values, otherwise use the environment
if test "x$UA_SYSROOT" = "x"; then
	# Installing onto a target
	# Add groups and users defined only for this package
	GROUPADD_PARAM="-r www"
	USERADD_PARAM="--system --home /var/www/thttpd --no-create-home                        --user-group thttpd"
	GROUPMEMS_PARAM="${GROUPMEMS_PARAM}"
fi

# Perform group additions first, since user additions may depend
# on these groups existing
if test "x$GROUPADD_PARAM" != "x"; then
	echo "Running groupadd commands..."
	# Invoke multiple instances of groupadd for parameter lists
	# separated by ';'
	opts=`echo "$GROUPADD_PARAM" | cut -d ';' -f 1`
	remaining=`echo "$GROUPADD_PARAM" | cut -d ';' -f 2-`
	while test "x$opts" != "x"; do
		perform_groupadd "$SYSROOT" "$OPT $opts" 10
		if test "x$opts" = "x$remaining"; then
			break
		fi
		opts=`echo "$remaining" | cut -d ';' -f 1`
		remaining=`echo "$remaining" | cut -d ';' -f 2-`
	done
fi

if test "x$USERADD_PARAM" != "x"; then
	echo "Running useradd commands..."
	# Invoke multiple instances of useradd for parameter lists
	# separated by ';'
	opts=`echo "$USERADD_PARAM" | cut -d ';' -f 1`
	remaining=`echo "$USERADD_PARAM" | cut -d ';' -f 2-`
	while test "x$opts" != "x"; do
		perform_useradd "$SYSROOT" "$OPT $opts" 10
		if test "x$opts" = "x$remaining"; then
			break
		fi
		opts=`echo "$remaining" | cut -d ';' -f 1`
		remaining=`echo "$remaining" | cut -d ';' -f 2-`
	done
fi

if test "x$GROUPMEMS_PARAM" != "x"; then
	echo "Running groupmems commands..."
	# Invoke multiple instances of groupmems for parameter lists
	# separated by ';'
	opts=`echo "$GROUPMEMS_PARAM" | cut -d ';' -f 1`
	remaining=`echo "$GROUPMEMS_PARAM" | cut -d ';' -f 2-`
	while test "x$opts" != "x"; do
		perform_groupmems "$SYSROOT" "$OPT $opts" 10
		if test "x$opts" = "x$remaining"; then
			break
		fi
		opts=`echo "$remaining" | cut -d ';' -f 1`
		remaining=`echo "$remaining" | cut -d ';' -f 2-`
	done
fi


%files
%defattr(-,-,-,-)
%dir "/var"
%dir "/etc"
%dir "/usr"
%dir "/var/www"
%dir "/var/www/thttpd"
%dir "/var/www/thttpd/cgi-bin"
"/var/www/thttpd/cgi-bin/redirect"
"/var/www/thttpd/cgi-bin/ssi"
"/var/www/thttpd/cgi-bin/phf"
%dir "/usr/sbin"
"/usr/sbin/htpasswd"
"/usr/sbin/thttpd"
"/usr/sbin/makeweb"
"/usr/sbin/syslogtocern"

%files -n thttpd-dbg
%defattr(-,-,-,-)
%dir "/var"
%dir "/usr"
%dir "/var/www"
%dir "/var/www/thttpd"
%dir "/var/www/thttpd/cgi-bin"
%dir "/var/www/thttpd/cgi-bin/.debug"
"/var/www/thttpd/cgi-bin/.debug/redirect"
"/var/www/thttpd/cgi-bin/.debug/ssi"
"/var/www/thttpd/cgi-bin/.debug/phf"
%dir "/usr/sbin"
%dir "/usr/sbin/.debug"
"/usr/sbin/.debug/htpasswd"
"/usr/sbin/.debug/thttpd"
"/usr/sbin/.debug/makeweb"

%files -n thttpd-dev
%defattr(-,-,-,-)

%files -n thttpd-doc
%defattr(-,-,-,-)
%dir "/usr"
%dir "/usr/share"
%dir "/usr/share/man"
%dir "/usr/share/man/man8"
%dir "/usr/share/man/man1"
"/usr/share/man/man8/ssi.8"
"/usr/share/man/man8/thttpd.8"
"/usr/share/man/man8/syslogtocern.8"
"/usr/share/man/man8/redirect.8"
"/usr/share/man/man1/makeweb.1"
"/usr/share/man/man1/htpasswd.1"

%prep -n thttpd
echo "include logs and patches, Please check them in SOURCES"

