import snowflake.connector
import snowflake.connector.cursor
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import logging
import sys

from SNFConfiguration import SNFConfiguration

class SNFConnectionManager:

    def __init__(self, conf:SNFConfiguration, env):
        self.__account            = conf.getSNFAccountName(env)
        self.__privateKey         = conf.getSNFPrivateKeyPath(env)
        self.__connSecret           = conf.getSNFConnectionSecret(env)
        self.__roleName           = conf.getSNFRole(env)
        self.__userID             = conf.getSNFUserName(env)
        self.__con                = None
        self.__warehouse          = conf.getSNFWarehouse(env)
        self.__connType           = conf.getSNFConnectionType(env)
        self.__initializeLogger()
        self.__initializeConnection()

    def __initializeLogger(self):
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(screen_handler)

    def __initializeConnection(self):
        try:
            if self.__connType.lower()=="Basic".lower():
                if self.__connSecret is None and self.__userID is None:
                    raise Exception("Either USERID or PASSWORD is not provided.")

                self.__con = snowflake.connector.connect(
                    user= self.__userID,
                    password= self.__connSecret,
                    account= self.__account,
                    role = self.__roleName,
                    warehouse = self.__warehouse
                )

            elif self.__connType.lower()=="SSO".lower():
                self.__con = snowflake.connector.connect(
                    user= self.__userID,
                    authenticator='externalbrowser',
                    account= self.__account,
                    role = self.__roleName,
                    warehouse = self.__warehouse
                )

            elif self.__connType.lower()=="KEY".lower():
                if self.__connSecret is None or self.__privateKey is None:
                    raise Exception("Either PRIVATE_KEY or PRIVATE_KEY_PASSPHRASE is not provided.")

                with open(self.__privateKey, "rb") as key:
                    p_key= serialization.load_pem_private_key(
                        key.read(),
                        password=self.__connSecret.encode(),
                        backend=default_backend()
                    )

                pkb = p_key.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption())

                self.__con = snowflake.connector.connect(
                    user=self.__userID,
                    account=self.__account,
                    private_key=pkb,
                    role = self.__roleName,
                    warehouse = self.__warehouse
                )
                self.logger.info("Connection opened to Snowflake account: %s" %self.__account)
        except Exception:
            raise

    def getConnection(self):
        return self.__con

    def releaseResource(self):
        if self.__con is not None:
            self.logger.info("Connection to snowflake is closed")
            self.__con.close()