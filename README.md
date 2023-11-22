### About the project

![Airflow Helper logo](docs/img/airflow_helper_logo_small.png "Airflow Helper"){ align=left }
**Airflow Helper** is a tool that currently allows to set up Airflow Variables & Connections & Pools from yaml config file.

But possible in future it can be extended by other helpful features - I'm open for any purposes & rfeature requests. Just open the issue & describe that you want.


### Airflow Versions Supports

You can see the github pipeline, that test library opposite each Airflow Version.
I can only guarantee that 100% library works with Apache Airflow versions that are added on the CI/CD pipeline, but with big chance it works with all 2.x Apache Airflow versions.


### How to use

1. Define airflow_settings.yaml file. You can check examples as a files in example/ folder in this git repo
(check 'Config keys' to see that keys are allowed - or check example/ folder)
```yaml

    

```

2. Run Airflow Helper
   
   Required settings: 

    - path to config file (by default it search `airflow_settings.yaml` file)
    - Airflow Server address (by default it tries to connect to localhost:8080)
    - Airflow user login (with admin rights that allowed to set up Pools, Variables, Connections)
    - Airflow user password (for login upper)


   2.1 Run Airflow Helper from cli

   2.2. Run Airflow Helper from Python Code




### Inheritance (include one config in another)

I love inheritance. So you can use it too. If you have some base vars/pools/connections for all environments and you don't want copy-paste same settings in multiple files - just use `include:` property at the start of your config. 

Note, that `include` allows you to include a list of files, they will be inherit one-by-one in order that you define under `include` arg from the top to the bootom.

Example:
1. Define your 'base' config, for example: airflow_settings_base.yaml
   
```yaml

    

```

2. Now create your dev-env config : airflow_settings_dev.yaml (names can be any that you want) and use 'include:' property inside it

```yaml

include: 
  - "airflow_settings_base.yaml"
  # if in "airflow_settings_base_2.yaml" there is a keys that exist in 
  # airflow_settings_base.yaml - they will be overwritted
  - "airflow_settings_base_2.yaml"


# here put only dev-special variables/connections/pools
airflow:
    variables:
        pass
```

### Motivation

This project allows to set up Connections & Variables & Pools for Airflow from yaml config.

Yeah, I know, I know... secrets backend ...

But I want to have all variables on my local machine toooo without need to connect to any secrets backend. And on tests also!

So I want to have some tool with that I can define ones all needed connections & variables in config file & forget about them during init new environment on local machine or running tests in CI.


### Inspiration
By Astronomer airflow_settings.yaml https://forum.astronomer.io/t/what-is-the-new-airflow-settings-yaml-file-for/149/21 (that looks like depricated now)

And airflow-vars https://github.com/omerzamir/airflow-vars (but I want pure python tool)
