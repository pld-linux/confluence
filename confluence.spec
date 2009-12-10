# TODO:
# - ask atlassian for permission to redistribute it.
# - install more language packs from
#   http://confluence.atlassian.com/display/DISC/Language+Pack+Translations

# Conditional build
%bcond_with	customized	# use patch for confluence-%{version}.jar

%include	/usr/lib/rpm/macros.java
Summary:	Confluence - Enterprise wiki
Name:		confluence
Version:	3.0.2
Release:	0.1
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
# You can download it from:
# http://www.atlassian.com/software/confluence/downloads/binary/confluence-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# NoSource0-md5:	954b71929bbd44a970cd2013f2b7c19a
NoSource:	0
Source1:	%{name}-context.xml
Source2:	%{name}-init.properties
Source3:	%{name}-log4j.properties
Source4:	%{name}-README.PLD
# http://confluence.atlassian.com/download/attachments/173229/confluence-pl_PL-plugin-1.0.jar
Source5:	confluence-pl_PL-plugin-1.0.jar
# NoSource5-md5:	b8d219e791a536fd98b1a717747e55bc
NoSource:	5
URL:		http://www.atlassian.com/software/confluence/
%{?with_customized:BuildRequires:	jar}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	tomcat
Suggests:	graphviz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Confluence is a simple, powerful wiki that lets you create and share pages,
documents and rich content with your team.

If you're looking for a better way to collaborate or a replacement for an
open-source wiki, Confluence has the essential enterprise features for your
organisation. 

%package lang-pl
Summary:        Polish translation for Confluence
Summary(pl.UTF-8):      Polskie tłumaczenie Confluence
Group:          I18n

%description lang-pl
Polish rtanslation for Confluence.

%description lang-pl -l pl.UTF-8
Polskie tłumaczenie Confluence.

%prep
%setup -q -n confluence-%{version}

cp %{SOURCE4} README.PLD

%if %{with customized}
mkdir work
mkdir -p edit-webapp/WEB-INF/lib
cd work
jar xf ../confluence/WEB-INF/lib/confluence-%{version}.jar
patch -p1 < $RPM_SOURCE_DIR/confluence-customize.patch
jar cf ../edit-webapp/WEB-INF/lib/confluence-%{version}.jar *
%endif

%build
CLASSPATH=$(build-classpath-directory lib/endorsed)
%ant

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},/var/log/%{name}}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
cp -a tmp/build/war $RPM_BUILD_ROOT%{_datadir}/%{name}

# configuration
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_sharedstatedir}/tomcat/conf/Catalina/localhost}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/confluence/tomcat-context.xml
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/confluence-init.properties
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/log4j.properties

install %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/lib/confluence-pl_PL-plugin-1.0.jar

ln -s %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/%{name}.xml

ln -sf %{_sysconfdir}/%{name}/log4j.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/log4j.properties
ln -sf %{_sysconfdir}/%{name}/confluence-init.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/confluence-init.properties
ln -sf %{_sysconfdir}/%{name}/log4j.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/log4j.properties

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/log4j-diagnostic.properties $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/log4j-diagnostic.properties
ln -s %{_sysconfdir}/%{name}/log4j-diagnostic.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/log4j-diagnostic

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/osuser.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/osuser.xml
ln -s %{_sysconfdir}/%{name}/osuser.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/osuser.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/atlassian-user.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/atlassian-user.xml
ln -s %{_sysconfdir}/%{name}/atlassian-user.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/atlassian-user.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/seraph-config.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/seraph-config.xml
ln -s %{_sysconfdir}/%{name}/seraph-config.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/seraph-config.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/seraph-paths.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/seraph-paths.xml
ln -s %{_sysconfdir}/%{name}/seraph-paths.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/seraph-paths.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/decorators.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/decorators.xml
ln -s %{_sysconfdir}/%{name}/decorators.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/decorators.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/glue-config.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/glue-config.xml
ln -s %{_sysconfdir}/%{name}/glue-config.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/glue-config.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/urlrewrite.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/urlrewrite.xml
ln -s %{_sysconfdir}/%{name}/urlrewrite.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/urlrewrite.xml

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/web.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/web.xml
ln -s %{_sysconfdir}/%{name}/web.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/web.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.PLD licenses
%dir %attr(750,root,servlet) %{_sysconfdir}/confluence
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/log4j.properties
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/log4j-diagnostic.properties
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/confluence-init.properties
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/atlassian-user.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/osuser.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/seraph-config.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/seraph-paths.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/decorators.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/glue-config.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/urlrewrite.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/web.xml
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,servlet) %{_sysconfdir}/%{name}/tomcat-context.xml

%{_datadir}/confluence
%exclude %{_datadir}/confluence/WEB-INF/lib/confluence-pl_PL-plugin-1.0.jar

%{_sharedstatedir}/tomcat/conf/Catalina/localhost/confluence.xml
%attr(2775,root,servlet) %dir %{_sharedstatedir}/confluence
%attr(2775,root,servlet) %dir /var/log/confluence

%files lang-pl
%{_datadir}/confluence/WEB-INF/lib/confluence-pl_PL-plugin-1.0.jar
