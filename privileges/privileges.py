import os
import sys
from dotenv import load_dotenv
import mysql.connector 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

mysql_root=os.environ.get('MYSQL_ROOT')
mysql_password=os.environ.get('MYSQL_ROOT_PASSWORD')
mysql_host=os.environ.get('MYSQL_HOST')

try:    
    mydb = mysql.connector.connect(
        user=mysql_root,
        password=mysql_password,
        host=mysql_host,
        port=3306
    )

    my_cursor = mydb.cursor()
    my_cursor.execute = f"GRANT ALL PRIVILEGES ON {os.environ.get('MYSQL_DATABASE')}.* TO '{os.environ.get('MYSQL_USER')}'@'%' IDENTIFIED BY 'password'"
    my_cursor.execute = "SHOW GRANTS FOR '{os.environ.get('MYSQL_USER')}'@'%'"
    result = my_cursor.fetchall()
    print(result)
    my_cursor.execute('FLUSH PRIVILEGES;')

    mydb.close()
    # create_user_query = f"""
    # GRANT ALL PRIVILEGES ON *.* TO '{os.environ.get('MYSQL_USER')}'@'%' WITH GRANT OPTION;

    # FLUSH PRIVILEGES;
    # """
    # my_cursor.execute(create_user_query)

    # my_cursor.close()
    # mydb.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
