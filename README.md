### About the Airflow Helper


![badge1](https://img.shields.io/pypi/v/airflow-helper) ![badge2](https://img.shields.io/pypi/l/airflow-helper) ![badge3](https://img.shields.io/pypi/pyversions/airflow-helper) ![workflow](https://github.com/xnuinside/airflow-helper/actions/workflows/ci-tests-runner.yml/badge.svg)


It's pretty fresh. Docs maybe not clear yet, keep calm ! I will update them soon :) 

<img align="left" width="150" height="150" src="docs/img/airflow_helper_middle_logo.png">

**Airflow Helper** is a tool that currently allows setting up Airflow Variables, Connections, and Pools from a YAML configuration file. Support yaml inheritance & can obtain all settings from existed Airflow Server!

In the future, it can be extended with other helpful features. I'm open to any suggestions and feature requests. Just open an issue and describe what you want.


### Motivation

This project allows to set up Connections & Variables & Pools for Airflow from yaml config. And export them to one config file.

Yeah, I know, I know... secrets backend ...

But I want to have all variables on my local machine toooo without need to connect to any secrets backend. And on tests also!

So I want to have some tool with that I can define ones all needed connections & variables in config file & forget about them during init new environment on local machine or running tests in CI.

Some of functionality looks like 'duplicated' airflow normal cli, but no.. 
I tried to use for, example, `airflow connections export` command, but it is export dozend of default connections, that I'm not interested in - and I don't want them, I want only those connections, that created by me.



### Airflow Versions Supports

You can see the github pipeline, that test library opposite each Airflow Version.
I can only guarantee that 100% library works with Apache Airflow versions that are added on the CI/CD pipeline, but with big chance it works with all 2.x Apache Airflow versions.


## How to use

#### Installation

1. With Python in virtualenv from PyPi: https://pypi.org/project/airflow-helper/

```console

    pip install airflow-helper

```

``` console

  airflow-helper --version

```

2. With docker image from Docker Hub: https://hub.docker.com/repository/docker/xnuinside/airflow-helper/

``` console

  # pull image
  docker pull xnuinside/airflow-helper:latest

  # sample how to run command

  docker run -it xnuinside/airflow-helper:latest --help
```

1. Example, how to use in docker-compose: example/docker-compose-example.yaml

#### Default settings

All arguments that required in cli or Python code have 'default' setting, you can check all of them in file 'airflow_helper/settings.py'


#### Variables overwriting

Note, that by default Airflow always overwrite variables, then you want to set up same that exists already in Airflow DB. 'overwrite' param that exists in Airflow Helper in config upload process relative only to Pools.


### What if I already have Airflow server with dozens of variables??

**Obtain current Variables, Connections, Pools from existed server**

Note: you should provide host url with protocol like: 'https://path-to-your-airflow-server.com' if protocol not in url, it will add 'http://' as default protocol

Generate config from existed Airflow Server - it is simple. Just provide creds with read access to existed Airflow Server like. We use Airflow REST API under the hood, so we need: 

    - server host & port or just url in format 'http://path-to-airflow:8080'
    - user login
    - user password

And use Airflow Helper:

1. From cli

```command
  
  # to get help
  airflow-helper create -h

  # to use command
  airflow-helper create path/where/to/save/airflow_settings.yaml --host https://your-airflow-host --port 8080 -u airflow-user -p airflow-password

```


2. From python code

```python

from airflow_helper import RemoteConfigObtainter

        
# by default it will save config in file airflow_settings.yaml
RemoteConfigObtainter(
  user='airflow_user', password='airflow_user_pass', url='https://path-to-airflow:8080').dump_config()
# but you can provide your own path like:

RemoteConfigObtainter(
  user='airflow_user', password='airflow_user_pass', url='https://path-to-airflow:8080').dump_config(
    file_path='any/path/to/future/airflow_config.yaml'
  )

```

It will create airflow_settings.yaml with all Variables, Pools & Connections inside!

**Define config from Scratch**
0. You can init empty config with cli

```console

  airflow-helper create new path/airflow_settings.yaml

```

It will create empty sample-file with pre-defined config values.

1. Define airflow_settings.yaml file. You can check examples as a files in example/ folder in this git repo
(check 'Config keys' to see that keys are allowed - or check example/ folder)

About connections:
Note that 'type' it is not Name of Connection type. It is type id check them here - https://github.com/search?q=repo%3Aapache%2Fairflow%20conn_type&type=code 

```yaml

    airflow:
      connections:
      - conn_type: fs
        connection_id: fs_default
        host: localhost
        login: fs_default
        port: null
      pools:
      - description: Default pool
        include_deferred: false
        name: default_pool
        slots: 120
      - description: ''
        include_deferred: true
        name: deferred
        slots: 0
      variables:
      - description: null
        key: variable-name
        value: "variable-value"
```

2. Run Airflow Helper to load config
   
   Required settings: 

    - path to config file (by default it search `airflow_settings.yaml` file)
    - Airflow Server address (by default it tries to connect to localhost:8080)
    - Airflow user login (with admin rights that allowed to set up Pools, Variables, Connections)
    - Airflow user password (for login upper)


   2.1 Run Airflow Helper from cli

```console

  # to get help

  airflow-helper load -h

  # to load config 
  airflow-helper load path/to/airflow_settings.yaml --host https://your-airflow-host --port 8080 -u airflow-user -p airflow-password

```

   2.2. Run Airflow Helper from Python Code

```python


  from airflow_helper import ConfigUploader


  # you can provide only url or host & port
  ConfigUploader(
    file_path=file_path, url=url, host=host, port=port, user=user, password=password
    ).upload_config_to_server()

``` 
 

### Inheritance (include one config in another)

I love inheritance. So you can use it too. If you have some base vars/pools/connections for all environments and you don't want copy-paste same settings in multiple files - just use `include:` property at the start of your config. 

Note, that `include` allows you to include a list of files, they will be inherit one-by-one in order that you define under `include` arg from the top to the bottom.

Example:
1. Define your 'base' config, for example: airflow_settings_base.yaml
   
```yaml

  connections:
  - conn_type: fs
    connection_id: fs_default
    host: localhost
    login: fs_default
    port: null
  pools:
  - description: Default pool
    include_deferred: false
    name: default_pool
    slots: 120
    

```

2. Now create your dev-env config : airflow_settings_dev.yaml (names can be any that you want) and use 'include:' property inside it

```yaml

include: 
  - "airflow_settings_base.yaml"

# here put only dev-special variables/connections/pools
airflow:
    variables:
        pass
```

This mean that final config that will be uploaded to server will contain base settings + settings that you defined directly in airflow_settings_dev.yaml config

### Library Configuration

Airflow Helper uses a bunch of 'default' settings under the hood. Because library uses pydantic-settings, you can also overwrite those configurations settings with environment variables or with monkey patch python code. 

To get full list of possible default settings - check file airflow_helper/settings.py.

If you never heard about pydantic-settings - check https://docs.pydantic.dev/latest/concepts/pydantic_settings/.

Example, to overwrite default airflow host you should provide environment variable with prefix `AIRFLOW_HELPER_` and name `HOST`, so variable name should looks like `AIRFLOW_HELPER_HOST`


### TODO 

1. Documentation website
2. Getting Variables, Pools, Connections directly from Airflow DB (currently available only with Airflow REST API)
3. Load configs from S3 and other cloud object storages
4. Load configs from git
5. Create overwrite mode for settings upload


### Inspiration
By Astronomer airflow_settings.yaml https://forum.astronomer.io/t/what-is-the-new-airflow-settings-yaml-file-for/149/21 (that looks like deprecated now)

And airflow-vars https://github.com/omerzamir/airflow-vars (but I want pure python tool)
*0.1.1*

1. Overwrite oprion added to `airflow-helper load` command