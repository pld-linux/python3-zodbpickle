#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		zodbpickle

Summary:	Fork of Python 2 pickle module
Summary(pl.UTF-8):	Alternatywna implementacja modułu pickle z Pythona 2
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.6
Release:	1
License:	PSFL v2 and ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zodbpickle/
Source0:	https://files.pythonhosted.org/packages/source/z/zodbpickle/%{module}-%{version}.tar.gz
# Source0-md5:	b7c206f87bd99226b915597d80a41215
URL:		https://pypi.org/project/zodbpickle/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.testrunner
%endif
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package presents a uniform pickling interface for ZODB:
- Under Python2, this package forks both Python 2.7's pickle and
  cPickle modules, adding support for the "protocol 3" opcodes.
  It also provides a new subclass of bytes, zodbpickle.binary,
  which Python2 applications can use to pickle binary values such that
  they will be unpickled as bytes under Py3k.

%description -l pl.UTF-8
Ten pakiet udostępnia ujednolicony interfejs pickle dla ZODB:
- dla Pythona 2 są to zmodyfikowane moduły pickle i cPickle z Pythona
  2.7, dodające obsługę kodu binarnego "protocol 3". Zawiera także
  nową podklasę bytes - zodbpickle.binary - której aplikacje Pythona 2
  mogą używać do wykonywania pickle wartości binarnych tak, że pod
  Py3k zostaną one zdekodowane do bytes.

%package -n python3-%{module}
Summary:	Fork of Python 3 pickle module
Summary(pl.UTF-8):	Alternatywna implementacja modułu pickle z Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
This package presents a uniform pickling interface for ZODB:
- Under Py3k, this package forks the pickle module (and the supporting
  C extension) from both Python 3.2 and Python 3.3. The fork add
  support for the noload operations used by ZODB.

%description -n python3-%{module} -l pl.UTF-8
Ten pakiet udostępnia ujednolicony interfejs pickle dla ZODB:
- dla Py3k jest to zmodyfikowany moduł pickle (wraz ze wspierającym
  rozszerzeniem w C) z Pythona 3.2 i 3.3. Modyfikacja dodaje obsługę
  operacji noload, używanych przez ZODB.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/zodbpickle/*.c
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/zodbpickle/pickle*_3.py*
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/zodbpickle/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zodbpickle/*.c
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zodbpickle/pickle*_2.py
%{__rm} -f $RPM_BUILD_ROOT%{py3_sitedir}/zodbpickle/__pycache__/pickle*_2.*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zodbpickle/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_pickle.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/_pickle.cpython-*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif
