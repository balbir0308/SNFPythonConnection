from SNFConfiguration import SNFConfiguration
from SNFConnectionMannager import SNFConnectionManager

if __name__ == '__main__':
    # Read snowflake configuration from resources/config.ini
    snfConfiguration = SNFConfiguration()

    # Establish a connection with Snowflake
    snfConnectionManager = SNFConnectionManager(snfConfiguration, 'dev')
    try:
        cur = snfConnectionManager.getConnection().cursor()
        cur.close()
    finally:
        snfConnectionManager.releaseResource()
