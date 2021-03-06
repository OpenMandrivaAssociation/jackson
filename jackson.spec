%{?_javapackages_macros:%_javapackages_macros}
Name:    jackson
Version: 1.9.11
Release: 4.3
Group:	Development/Java
Summary: Jackson Java JSON-processor
License: ASL 2.0 or LGPLv2
URL:     http://jackson.codehaus.org
Source0: http://jackson.codehaus.org/1.9.11/jackson-src-1.9.11.tar.gz
# Build plain jar files instead of OSGi bundles in order to avoid depending on
# BND:
Patch0:  %{name}-build-plain-jars-instead-of-osgi-bundles.patch
# Don't require a repackaged version of ASM:
Patch1:  %{name}-dont-require-repackaged-asm.patch
# Don't bundle the ASM classes:
Patch2:  %{name}-dont-bundle-asm.patch
# fix for JACKSON-875
Patch3:  %{name}-1.9.11-to-1.9.13.patch
# Fix javadoc build
Patch4:  %{name}-1.9.11-javadoc.patch

BuildArch: noarch

Requires: java-headless
Requires: jpackage-utils
Requires: joda-time >= 1.6.2
Requires: stax2-api >= 3.1.1
Requires: jsr-311 >= 1.1.1
Requires: objectweb-asm3 >= 3.3

BuildRequires: jpackage-utils
BuildRequires: java-devel
BuildRequires: ant >= 1.8.2
BuildRequires: joda-time >= 1.6.2
BuildRequires: stax2-api >= 3.1.1
BuildRequires: jsr-311 >= 1.1.1
BuildRequires: objectweb-asm3 >= 3.3
BuildRequires: cglib >= 2.2
BuildRequires: groovy >= 1.8.5

%description
JSON processor (JSON parser + JSON generator) written in Java. Beyond basic
JSON reading/writing (parsing, generating), it also offers full node-based Tree
Model, as well as full OJM (Object/Json Mapper) data binding functionality.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

# Remove all the binary jar files, as the packaging policies
# forbids using them:
find . -type f -name '*.jar' -exec rm {} \;

# Remove some tests to avoid additional dependencies:
rm src/test/org/codehaus/jackson/map/interop/TestHibernate.java
rm src/perf/perf/TestJsonPerf.java
rm src/test/org/codehaus/jackson/map/interop/TestGoogleCollections.java

# Make symbolic links to the jar files expected by the ant build
# scripts:
ln -s $(build-classpath joda-time) lib/ext/joda-time.jar
ln -s $(build-classpath stax2-api) lib/xml/sta2-api.jar
ln -s $(build-classpath jsr-311) lib/jaxrs/jsr-311.jar
ln -s $(build-classpath objectweb-asm3/asm) lib/ext/asm/asm.jar
ln -s $(build-classpath objectweb-asm3/asm) lib/repackaged/jackson-asm.jar
ln -s $(build-classpath cglib) lib/ext/cglib/cglib-nodep.jar
ln -s $(build-classpath groovy) lib/ext/groovy/groovy.jar
ln -s $(build-classpath junit) lib/junit/junit.jar

sed -i "s,59 Temple Place,51 Franklin Street,;s,Suite 330,Fifth Floor,;s,02111-1307,02110-1301," \
 release-notes/lgpl/LGPL2.1

native2ascii -encoding UTF8 src/test/org/codehaus/jackson/jaxrs/TestUntouchables.java \
 src/test/org/codehaus/jackson/jaxrs/TestUntouchables.java
 
%build

ant dist

%install

# Create the directories for the jar and pom files:
mkdir -p %{buildroot}%{_javadir}/jackson
install -d -m 755 %{buildroot}%{_mavenpomdir}

# For each jar file install it and its pom:
jars='
jackson-core-asl
jackson-mapper-asl
jackson-xc
jackson-smile
jackson-mrbean
jackson-jaxrs
'
for jar in ${jars}
do
  cp -p dist/${jar}-%{version}.jar %{buildroot}%{_javadir}/jackson/${jar}.jar
  install -pm 644 dist/${jar}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP.jackson-${jar}.pom
  %add_maven_depmap JPP.jackson-${jar}.pom jackson/${jar}.jar
done

# Javadoc files:
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp dist/javadoc/* %{buildroot}%{_javadocdir}/%{name}/.

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc README.txt
%doc release-notes

%files javadoc
%{_javadocdir}/%{name}
%doc README.txt
%doc release-notes

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 1.9.11-3
- switch to java-headless (build)requires (rhbz#1068160)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 1.9.11-2
- use objectweb-asm3

* Wed Sep 25 2013 gil cattaneo <puntogil@libero.it> 1.9.11-1
- Update to upstream version 1.9.11

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Juan Hernandez <juan.hernandez@redhat.com> - 1.9.4-5
- Don't bundle ASM classes (#842603)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.9.4-3
- Remove the build dependency on maven ant tasks

* Wed Feb 15 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.9.4-2
- Updated license to ASL 2.0 or LGPLv2
- Removed macros from the source URL

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.9.4-1
- Update to upstream version 1.9.4

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.6.3-3
- Include jackson-jarxrs.jar in the package

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.6.3-2
- Don't use absolute references but build-classpath

* Thu Feb 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.6.3-1
- Initial packaging


