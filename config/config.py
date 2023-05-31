import pymysql
def UpdateUserStatus():
    # Connecting to a MySQL database
    conn = pymysql.connect(
                user="root",
                password="xyz",
                database="finalproject"
            )

    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # Query User List
    select_users_query = "SELECT username FROM users"
    cursor.execute(select_users_query)
    users = cursor.fetchall()

    # Create tables for each user
    for user in users:
        username = user[0]

        # Create user table
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS `{username}` (
            id INT AUTO_INCREMENT,
            username varchar(10) DEFAULT '{username}',
            mask_time DATETIME,
            masked CHAR(1) DEFAULT 'n',
            PRIMARY KEY (id)
        );
        '''
        cursor.execute(create_table_query)

    # Submit Changes
    conn.commit()

    # Close the connection
    conn.close()



if __name__ == '__main__':

    UpdateUserStatus()