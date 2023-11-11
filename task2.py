import sqlite3
from sqlite3 import Error

# Establish a connection to the database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# Create a table
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Add a new entry
def create_entry(conn, entry):
    """
    Create a new entry into the solution table
    :param conn: the Connection object
    :param entry: the insert entry
    :return: project id
    """
    sql = ''' INSERT INTO solution(name,status,begin_date,end_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

# Retrieve data
def select_all_entries(conn, table):
    """
    Query all rows in the given table
    :param conn: the Connection object
    :param table: the table name to query in
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")

    rows = cur.fetchall()

    for row in rows:
        print(row)

# Update data
def update_entry(conn, data):
    """
    update status, begin_date, and end date of an entry
    :param conn:
    :param data:
    :return: number of rows affected
    """
    sql = ''' UPDATE solution
              SET name = ? ,
                  status = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.rowcount

# Delete data
def delete_entry(conn, id):
    """
    Delete an entry by entry id
    :param conn: Connection to the SQLite database
    :param id: id of the entry
    :return:
    """
    sql = 'DELETE FROM solution WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    return cur.rowcount

# Database file
database = "pythonsqlite.db"

# SQL for creating table
sql_create_solution_table = """ CREATE TABLE IF NOT EXISTS solution (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status text,
                                        begin_date text,
                                        end_date text
                                    ); """

# Create a database connection
conn = create_connection(database)

# Create table
if conn is not None:
    # create solution table
    create_table(conn, sql_create_solution_table)
else:
    print("Error! cannot create the database connection.")

with conn:
    # Create a new entry
    entry = ('Task 2 begin', 'In progress', '2023-11-08', '2023-11-11');
    entry_id = create_entry(conn, entry)
    
    # Update an entry
    update_entry(conn, ('Task 2 solution', 'Completed', '2023-11-09', '2023-11-09', entry_id))
    
    # Retrieve all entries
    select_all_entries(conn, "solution")
    
    # Delete an entry
    delete_entry(conn, entry_id)
