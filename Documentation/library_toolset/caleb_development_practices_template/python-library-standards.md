# Python Library Development Standards

This document describes the practices and tools we prefer to use when building Python libraries.

## Project Layout and Tools

### Inspiration

Our Python project layout and tools are inspired by Ben Kehoe's [blog post on hygienic Python setup](https://ben11kehoe.medium.com/my-python-setup-77c57a2fc4b6).

Ben's post gives us a few key takeaways:

    1. Never install anything in system python installs
    2. Always use a virtualenv
    3. virtualenvs are better when their state is managed (vs. direct pip installs into them), because then you can recreate them at will
    4. CLI tools written in python shouldn’t be treated like python packages
    5. Don’t pip-install tools that work across python versions into a specific python version (give them their own isolated install)

To sum up his advice, we want each Python library project to be as isolated as possible in terms of Python version, virtual environment, and dependencies.
It should be trivial for a developer to have many Python projects checked out and functioning in their local environment.

### Managing Python Versions

There are many versions of Python in use at XYZ_Company.
Data Platform projects might use version 3.7, in order to maintain compatibility with the AWS Glue environment.
Other projects might use newer versions of Python, to better reflect their runtime environments or to desired capabilities.

In general, projects should use the newest version of Python that is compatible with their runtime environment.
In almost all cases, that should be Python version 3 or higher.
Python version 2 is deprecated and unsupported.

#### `pyenv`

[`pyenv`](https://github.com/pyenv/pyenv) is a tool to manage the active Python version on a project-by-project basis.
Each project has a `.python-version` file, which specifies the specific version of Python to use for that project.
`.python-version`  files should *not* be checked into version control, as some specific versions of Python may not be available on all platforms.
For non-developer platforms (e.g. CircleCI or CodeBuild), we control the version of Python by using a specific container image.

### Managing Python Dependencies

#### `pipenv`

[`pipenv`](https://github.com/pypa/pipenv) is a tool used to manage Python projects in general.
It handles virtual environments (e.g., "virtualenvs"), dependencies, and other aspects of the development environment.
`Pipenv` is configured using a file named `Pipfile`, which lives in the root of a project.

Here's an example `Pipfile` file:

```toml
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[requires]
python_version = "3.7"

[packages]
boto3 = "==1.16.47"

[dev-packages]
pipenv-setup = "==3.1.2"
pyspark = "==3.1.1"
pytest = "==6.2.2"
setuptools_scm = "==6.3.2"
twine = "==3.4.1"
```

The `Pipfile` file contains different sections, the most important of which are `[packages]` and `[dev-packages]`.
`[packages]` contains dependency specifications for other Python libraries that a project depends on.
When our project is installed using `pip`, any dependency listed in the `[packages]` section will also be installed.

The `[dev-packages]` section contains dependency specifications for Python libraries that are useful when developing a Python project, but which are not necessary otherwise.
In this example, we see that the `pytest` is listed in `[dev-packages]`.
`pytest` is a library used for unit testing, which is useful during development but which shouldn't be installed when our project is used elsewhere.
When our project is installed using `pip`, dependencies listed in the `[dev-packages]` section will not be installed.

We can also use the `[dev-packages]` section to track dependencies that are needed during development but that are provided in some other way at runtime.
For example, XYZ_Company data platform projects depend on the `pyspark` library.
That library might be listed in the `[dev-packages]` section, so that it can be used during development.
However, it is already provided by the AWS Glue runtime, so it doesn't need to be installed when our project is used there.

#### `setuptools`

[`setuptools`](https://github.com/pypa/setuptools) is another Python packaging and dependency management tool.
We don't use `setuptools` in XYZ_Company projects except to package libraries before uploading them to a package repository.
`setuptools` is configured using a `setup.py` file, which lives in the root of a project.

#### `pipenv-setup`

We never alter the `setup.py` file directly.
Instead, the `setup.py` file is managed using `pipenv-setup`, which synchronizes various parts of the `Pipfile` file to the `setup.py` file.
`pipenv-setup` and other development utility libraries are listed in the `[dev-packages]` section of the `Pipfile`.

### Using XYZ_Company Python Packages

XYZ_Company Python packages are referenced using Git URLs in the `[dev-packages]` section of a `Pipfile`.
For example, if a project depends on the `XYZ_Company-glue` Python package, it should reference that package like this:

```toml
[dev-packages]
XYZ_Company-glue = { git = "ssh://git@github.com/XYZ_Company/XYZ_Company_glue.git", ref = "v1.0.0" }
```

This style of dependency specification is only relevant in development environment.
Git URLs are used because the primary XYZ_Company Python package repository is hosted in CodeArtifact, which is not easily accessible from some development environments.

In runtime environments, any packages that are referenced using Git URLs will *not* be automatically installed.
Instead, those packages should be installed separately using `pip` or another tool.
For example, to install the `XYZ_Company-glue` package referenced by the above Git URL, the following `pip` command should be used:

```shell
$ pip install "XYZ_Company-glue==1.0.0"
```

Glue runtime environments can install packages via `pip` automatically.
Other environments may have different mechanisms for installing packages.

Note that in the future, we hope to be able to use standard non-Git package specifications for runtime dependencies, in all environments.

## Code Formatting

XYZ_Company Python projects should make use of tools like `pycodestyle` (formerly `pep8`) to assist with standards-based formatting.

## Testing

XYZ_Company Python projects currently use `pytest`, or in a few cases the built-in `unittest` framework.

Tests should be in a top-level `tests` directory.
The structure of that directory should generally match the structure of the modules being tested.

For example, here's a set of modules and the associated test directory:

```
├── data_platform_devtools
│   ├── __init__.py
│   ├── cli
│   │   ├── __init__.py
│   │   ├── get_package_versions
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   └── args.py
│   │   └── run_glue_job
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       └── args.py
│   └── common
│       ├── __init__.py
│       ├── boto.py
│       ├── discovery.py
│       ├── git.py
│       └── waiters
│           ├── __init__.py
│           └── step_functions_execution.py
└── tests
    ├── __init__.py
    └── data_platform_devtools
        ├── __init__.py
        ├── cli
        │   ├── __init__.py
        │   ├── get_package_versions
        │   │   ├── __init__.py
        │   │   └── test_main.py
        │   └── run_glue_job
        │       ├── __init__.py
        │       └── test_main.py
        └── common
            ├── __init__.py
            └── test_git.py
```
