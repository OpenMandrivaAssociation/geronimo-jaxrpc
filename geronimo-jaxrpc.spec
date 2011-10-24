%global spec_ver 1.1
%global spec_name geronimo-jaxrpc_%{spec_ver}_spec

Name:             geronimo-jaxrpc
Version:          2.1
Release:          2
Summary:          Java EE: Java API for XML Remote Procedure Call v1.1
Group:            Development/Java
License:          ASL 2.0

URL:              http://geronimo.apache.org/
Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz
Source1:          %{name}.depmap
# Use parent pom files instead of unavailable 'genesis-java5-flava'
Patch1:           use_parent_pom.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven2 >= 2.2.1
BuildRequires:    geronimo-parent-poms
BuildRequires:    maven-resources-plugin
BuildRequires:    saaj_api
BuildRequires:    geronimo-osgi-locator
BuildRequires:    servlet >= 2.5

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires:         saaj_api
Requires:         geronimo-osgi-locator
Requires:         servlet >= 2.5
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

Provides:         jaxrpc_api = %{spec_ver}

%description
This package contains the core JAX-RPC APIs for the client programming model. 

%package javadoc
Group:            Development/Java
Summary:          Javadoc for %{name}
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{spec_name}-%{version}
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE
%patch1 -p0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file="%{SOURCE1}" \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{spec_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/jaxrpc.jar

# poms
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.geronimo.specs %{spec_name} %{version} JPP %{name}
%add_to_maven_depmap javax.xml jaxrpc-api %{spec_ver} JPP %{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

