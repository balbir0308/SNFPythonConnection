# SNFPythonConnection
We have frequently seen developers struggle to establish a connection to Snowflake in a first go using Snowflake Python Connector. This project uses Snowflake Python connector to establish a connection to Snowflake using Basic, SSO or RSA authentication mechanism.


The core logic to establish a connection to Snowflake is present in the class `SNFConnectionManager.py`

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
|  snowflake_private_key_path_env_var|  | Environment variable defining path to Private Key (`export ENV_SNF_DEV_PRIVATE_KEY=<location to private key>`). Required for snowflake_connection_type=key |
|  snowflake_connection_secret_env_var| * | Environment variable defining password for Basic connection or connection using Private Key Passphrase (`export ENV_SNF_DEV_CONN_SECRET=<your pass phrase>`). |

## Code Walkthrough
**Assumptions**: You have a Database, Schema and Table created and records inserted into them.
We will not cover the **Discretionary Access Control (DAC)** and **Role-based Access Control (RBAC)** around snowflake resources created it's expected you have a role which has sufficent permissions to operate on the storage and compute, following snowflake arcticle provide some good information around [Access Control](https://docs.snowflake.com/en/user-guide/security-access-control-overview).

Blow code allows you to establish a connection to snowflake and read a column value in a table. Snippet can be found in `main.py`

```
try:  
    cur = snfConnectionManager.getConnection().cursor()  
  
    logger.info("Lookup employees table.")  
    results = cur.execute('select first_name from user_balbir.employee_test.emp_basic')  
    for rec in results:  
        name = str(rec[0])  
        logger.info("Column value (name): %s"%name)  
  
    cur.close()  
finally:  
    snfConnectionManager.releaseResource()
```    

## Code Setup

Prerequisites:  `python, pip, virtualenv`

    $ pip install virtualenv 
    $ virtualenv penv 
    $ source penv/bin/activate 
    $ pip install -r requirements.txt

### Execute Command
    python main.py