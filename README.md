# SNFPythonConnection
Python class to connect to snowflake using Basic, SSO or RSA authentication mechanism.

## Configuration File

Code maintains a configuration file which defines Snowflake Connection attributes.

| File | Note  |
|--|--|
|./resources/config.ini  |Snowflake Connection configuration is defined in this file. We can have more than one environment defined in this file as Group.  |

### config.ini
| Attribute | Required | Note|
|--|--|--|
|  snowflake_account| * | Snowflake Account Name |
|  snowflake_user_name| * | Snowflake User Name |
|  snowflake_role|  | Snowflake Role, not defined use profile default_role |
|  snowflake_warehouse|  | Snowflake Warehouse, not defined use profile default_warehouse |
|  snowflake_connection_type| * | KEY / SSO /BASIC |
|  snowflake_private_key_path_env_var|  | Environment variable defining path to Private Key. Required for snowflake_connection_type=key |
|  snowflake_connection_secret_env_var| * | Environment variable defining password for Basic connection or connection using Private Key Passphrase. |

## Code Setup

Prerequisites:  `python, pip, virtualenv`

    $ pip install virtualenv 
    $ virtualenv penv 
    $ source penv/bin/activate 
    $ pip install -r requirements.txt

### Execute Command
    python main.py