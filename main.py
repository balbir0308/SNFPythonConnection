from SNFConfiguration import SNFConfiguration
from SNFConnectionMannager import SNFConnectionManager
import logging
import sys

if __name__ == '__main__':
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(screen_handler)

    # Read snowflake configuration from resources/config.ini
    logger.info("Reading snowflake configuration from resources/config.ini")
    snfConfiguration = SNFConfiguration()

    # Establish a connection with Snowflake
    logger.info("Establish a connection with Snowflake.")
    snfConnectionManager = SNFConnectionManager(snfConfiguration, 'dev')
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
