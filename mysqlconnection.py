""" Import Oracle's python connector for MySQL """
import mysql.connector
import collections

def _convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(_convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    else:
        return data

# Create a class that will give us an object that we can use to connect to a database
class MySQLConnection(object):
    # init method with configurations.
    def __init__(self, db):
        """ BEGIN DATABASE CONFIGURATIONS """
        self.config = {
            'user': 'root',
            'password': 'root', # Change this for windows users
            'database': db,
            'host': 'localhost',
            # comment out the line below for windows
            'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
        }
        self.conn = mysql.connector.connect(**self.config)
        self.conn.autocommit=True

    """ BELOW ARE THE CUSTOM FUNCTIONS WE BUILT FOR YOU TO USE """
    def query_db(self, query, data=None):

        if data:
            for key,value in data.items():
                # The Learning platform uses ":field", but the SQL driver required %(field)
                # So this swaps the corresponding keys in the query
                query = query.replace(':'+key, '%(' + key + ')s')

        cursor = self.conn.cursor(dictionary=True)
        result = cursor.execute(query, data)

        if query[0:6].upper() in ['UPDATE', 'DELETE']:
            # if the query was a update or delete... return the number of rows affected
            cursor.close()
            return result

        elif query[0:6].upper() == 'INSERT':
            # if the query is an insert, display the id of the inserted record
            insert_id = cursor.lastrowid
            cursor.close()
            return insert_id

        else:
            # for all other queries, e.g. SELECTS, just grab everything
            result = list(cursor.fetchall())
            cursor.close()
            return _convert(result)

# This is the module method to be called by the user in server.py. Make sure to provide the db name!
def MySQLConnector(db):
    return MySQLConnection(db)
