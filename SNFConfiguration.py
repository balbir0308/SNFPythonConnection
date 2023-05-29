import configparser
import os

class SNFConfiguration:

    def __init__(self):
       self.__config = configparser.ConfigParser()
       self.__config.read('resources/config.ini')

    def getSNFAccountName(self, env):
        return self.__config[env]["snowflake_account"]

    def getSNFUserName(self, env):
        return self.__config[env]["snowflake_user_name"]

    def getSNFPrivateKeyPath(self, env):
        if self.__config[env]["snowflake_connection_type"].lower()=="KEY".lower():
            return os.getenv(self.__config[env]["snowflake_private_key_path_env_var"])
        else:
            return None

    def getSNFConnectionSecret(self, env):
        if (self.__config[env]["snowflake_connection_type"].lower()=="KEY".lower() or
            self.__config[env]["snowflake_connection_type"].lower()=="BASIC".lower()) :
            return os.getenv(self.__config[env]["snowflake_connection_secret_env_var"])
        else:
            return None

    def getSNFWarehouse(self, env):
        return self.__config[env]["snowflake_warehouse"]

    def getSNFRole(self, env):
        return self.__config[env]["snowflake_role"]

    def getSNFConnectionType(self, env):
        return self.__config[env]["snowflake_connection_type"]