#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module		zodbpickle

Summary:	Fork of Python 3 pickle module
Summary(pl.UTF-8):	Alternatywna implementacja modułu pickle z Pythona 3
Name:		python3-%{module}
Version:	4.2
Release:	1
License:	PSFL v2 and ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zodbpickle/
Source0:	https://files.pythonhosted.org/packages/source/z/zodbpickle/%{module}-%{version}.tar.gz
# Source0-md5:	5e212281d2a2d29d8cf6bc4d71f93722
URL:		https://pypi.org/project/zodbpickle/
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package presents a uniform pickling interface for ZODB:
- Under Py3k, this package forks the pickle module (and the supporting
  C extension) from both Python 3.2 and Python 3.3. The fork add
  support for the noload operations used by ZODB.

%description -l pl.UTF-8
Ten pakiet udostępnia ujednolicony interfejs pickle dla ZODB:
- dla Py3k jest to zmodyfikowany moduł pickle (wraz ze wspierającym
  rozszerzeniem w C) z Pythona 3.2 i 3.3. Modyfikacja dodaje obsługę
  operacji noload, używanych przez ZODB.

%package apidocs
Summary:	API documentation for Python zodbpickle module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zodbpickle
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python zodbpickle module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zodbpickle.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zodbpickle/*.c
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zodbpickle/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/_pickle.cpython-*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,historical,*.html,*.js}
%endif
