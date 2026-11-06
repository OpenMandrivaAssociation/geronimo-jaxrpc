%global spec_name geronimo-jaxrpc_1.1_spec

Name:		geronimo-jaxrpc
Version:	2.1
Release:	1
Summary:	Java API for XML-based RPC 1.1
Group:		Development/Java
License:	ASL 2.0 and W3C
URL:		https://geronimo.apache.org/
Source0:	https://repo1.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	geronimo-saaj
BuildRequires:	geronimo-osgi-locator
BuildRequires:	mvn(javax.servlet:javax.servlet-api)
BuildRequires:	mvn(net.java:jvnet-parent:pom::)
BuildSystem:	maven
BuildOption(install):	--file-name %{name} --alias javax.xml:jaxrpc-api

Provides:	jaxrpc_api = 1.1

%description
JAX-RPC 1.1 client API. Servlet types come from javax.servlet.

%prep
%setup -q -n %{spec_name}-%{version}
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE NOTICE
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def local(tag):
    return tag.split("}", 1)[-1]

tree = ET.parse("pom.xml")
root = tree.getroot()
for node in list(root):
    if local(node.tag) in {"parent", "build", "distributionManagement"}:
        root.remove(node)
for node in root.iter(f"{{{NS}}}packaging"):
    node.text = "jar"
for dep in root.iter(f"{{{NS}}}dependency"):
    group = artifact = ""
    group_node = artifact_node = version_node = None
    for node in dep:
        if local(node.tag) == "groupId":
            group_node = node
            group = (node.text or "").strip()
        elif local(node.tag) == "artifactId":
            artifact_node = node
            artifact = (node.text or "").strip()
        elif local(node.tag) == "version":
            version_node = node
    if artifact == "geronimo-servlet_3.0_spec":
        group_node.text = "javax.servlet"
        artifact_node.text = "javax.servlet-api"
        if version_node is not None:
            dep.remove(version_node)
tree.write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE NOTICE
