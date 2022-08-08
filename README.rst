###################
ts_IntegrationTests
###################


## Description

This repository contains the infrastucture necessary to automate the integration test scripts. The scripts themselves are defined as Python Classes, starting from the BaseScript Class and moving to either an AuxTelVisit class or a MainTelVisit class.  The BaseScript Class connects to the SalObj Domain the ScriptQueue Remote, ensures the ScriptQueue is running by waiting for the heartbeat, and then pauses the ScriptQueue, loads the scripts and the associated configurations and then resumes the ScriptQueue to execute the scripts.

* https://github.com/lsst-ts/ts_IntegrationTests)

### Installation and Usage

TBD - Conda installation and package execution instructions.

To properly install and setup this package, start by issuing

```
pip install .
```

This will minimally install the package and the required dependencies. It also loads the scripts as command-line executable processes.

### Testing

To install and setup this package for testing and development, start by issuing

```
pip install .[test]
```

This will install the parameterized and yamllint modules used to verify the integration test scrips and Yaml-formatted configurations are correct. It also loads the scripts as command-line executable processes.

NOTE: This installation requires a TSSW environment (ts_salobj, ts_ddsconfig, etc). Most likely, this comes from using one of the TSSW-supplied Docker images, e.g. lsstts/develop-env:develop.

To test, execute:

```
pytest -ra
```

#### Test Utilities

The testutils.py file, located in python/lsst/ts/IntegrationTests, contains functions and variables used throughout the testing. This is where the assert_yaml_formatted function is defined.  It verifies the configuration modules are storing the strings as properly Yaml-formatted.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/lsst-ts/ts_xml/tags).

## Contact Information

Please contact <rbovill@lsst.org> with any questions or concerns.
