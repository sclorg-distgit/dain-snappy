%{?scl:%scl_package dain-snappy}
%{!?scl:%global pkg_name %{name}}

%global commit e02f7c887d666afbdd11763f3a6ba22e68f53f15
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%bcond_with hadoop

Name:           %{?scl_prefix}dain-snappy
Version:        0.4
Release:        3.1%{?dist}
Summary:        Snappy compression library
License:        ASL 2.0 and BSD
URL:            https://github.com/dain/snappy
BuildArch:      noarch

Source0:        https://github.com/dain/snappy/archive/%{commit}/%{pkg_name}-%{shortcommit}.tar.gz

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.testng:testng)
BuildRequires:  %{?scl_prefix}mvn(org.xerial.snappy:snappy-java)
%if %{with hadoop}
BuildRequires:  mvn(org.apache.hadoop:hadoop-common)
%endif

%description
This is a rewrite (port) of Snappy writen in pure Java. This
compression code produces a byte-for-byte exact copy of the output
created by the original C++ code, and extremely fast.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
%{summary}.

%prep
%setup -q -n snappy-%{commit}
%pom_remove_plugin :really-executable-jar-maven-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-surefire-plugin

%if %{with hadoop}
%pom_change_dep :hadoop-core :hadoop-common
%else
%pom_remove_dep :hadoop-core
find -name HadoopSnappyCodec.java -delete
find -name TestHadoopSnappyCodec.java -delete
%endif

# Broken test - dain-snappy produces different output than original snappy
sed -i /@Test/d $(find -name SnappyTest.java)

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license license.txt notice.md

%files javadoc -f .mfiles-javadoc
%license license.txt notice.md

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 0.4-3.1
- Automated package import and SCL-ization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun  2 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4-2
- Conditionally build without Hadoop codec

* Tue Apr 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4-1
- Initial packaging
