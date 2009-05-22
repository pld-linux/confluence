# TODO:
# - ask atlassian for permission to redistribute it.
%include	/usr/lib/rpm/macros.java
Summary:	Confluence - Enterprise wiki
Name:		confluence
Version:	2.10.3
Release:	0.1
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
# You can download it from:
# http://www.atlassian.com/software/confluence/downloads/binary/confluence-2.10.3.tar.gz
Source0:	%{name}-%{version}.tar.gz
# NoSource0-md5:	40e613c4be7cbc91613ef143275564d8
NoSource:	0
Source1:	%{name}-context.xml
Source2:	%{name}-init.properties
Source3:	%{name}-README.PLD
URL:		http://www.atlassian.com/software/confluence/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	tomcat
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Confluence is a simple, powerful wiki that lets you create and share pages,
documents and rich content with your team.

If you're looking for a better way to collaborate or a replacement for an
open-source wiki, Confluence has the essential enterprise features for your
organisation. 

%prep
%setup -q

cp %{SOURCE3} README.PLD

%build
CLASSPATH=$(build-classpath-directory lib/endorsed)
%ant

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},/var/log/%{name}}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
cp -a tmp/build/war $RPM_BUILD_ROOT%{_datadir}/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/classes/confluence-init.properties

# configuration
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/confluence,%{_sharedstatedir}/tomcat/conf/Catalina/localhost}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/confluence.xml

ln -s %{_sharedstatedir}/tomcat/conf/Catalina/localhost/confluence.xml $RPM_BUILD_ROOT%{_sysconfdir}/confluence/tomcat-context.xml

mv $RPM_BUILD_ROOT%{_datadir}/confluence/WEB-INF/classes/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/confluence/log4j.properties
ln -s %{_sysconfdir}/confluence/log4j.properties $RPM_BUILD_ROOT%{_datadir}/confluence/WEB-INF/classes/log4j.properties

mv $RPM_BUILD_ROOT%{_datadir}/confluence/WEB-INF/classes/confluence-init.properties $RPM_BUILD_ROOT%{_sysconfdir}/confluence/confluence-init.properties
ln -s %{_sysconfdir}/confluence/confluence-init.properties $RPM_BUILD_ROOT%{_datadir}/confluence/WEB-INF/classes/confluence-init.properties

mv $RPM_BUILD_ROOT%{_datadir}/confluence/WEB-INF/classes/atlassian-user.xml $RPM_BUILD_ROOT%{_sysconfdir}/confluence/atlassian-user.xml
ln -s %{_sysconfdir}/confluence/atlassian-user.xml $RPM_BUILD_ROOT%{_datadir}/confluence/WEB-INF/classes/atlassian-user.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%{_datadir}/confluence
%dir %{_sysconfdir}/confluence
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/confluence/log4j.properties
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/confluence/confluence-init.properties
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/confluence/atlassian-user.xml
%{_sysconfdir}/confluence/tomcat-context.xml
%config(noreplace) %verify(not md5 mtime size) %attr(2775,root,tomcat) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/confluence.xml
%attr(2775,root,servlet) %dir %{_sharedstatedir}/confluence
%attr(2775,root,servlet) %dir /var/log/confluence
%doc README.PLD
