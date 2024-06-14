
import pandas as pd
import pymysql
import traceback,time
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from env import config
DB_USERNAME=config('DB_USERNAME',default=None)
DB_PASSWORD=config('DB_PASSWORD',default=None)
DB_HOSTNAME=config('DB_HOSTNAME',default=None)
DB_PORT=config('DB_PORT',default=None)
class DatabaseManager:
    def __init__(self):
        user = DB_USERNAME
        password = DB_PASSWORD
        host = DB_HOSTNAME
        db_port = DB_PORT
        database = 'contrat_q'

        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{db_port}/{database}')
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        try:
            self.session = self.Session()
            print("Database session created successfully.")
        except Exception as e:
            print(f"Error creating database session: {e}")

    def close_session(self):
        if hasattr(self, 'session') and self.session is not None:
            self.session.close()
            self.session = None
    def table_exists(self, table_name):
        inspector = inspect(self.engine)
        return inspector.has_table(table_name)
    def insert_data(self, data_list):
        print(f'INSERT {len(data_list)}')
        if len(data_list) == 0:
            return True
        
        while True:
            try:
                while self.get_proclist() >= 10:
                    try:
                        print('Too many in the queue...')
                        time.sleep(10)
                        self.kill_sleep()
                    except Exception as e:
                        print(f'{traceback.format_exc()}')
                        continue
                # Get a connection from the pool

                self.create_session()
                print('here')
                cols=pd.read_sql('SELECT * FROM contrat_q.list_int limit 1;',con=self.engine).columns
                data_frame = data_list
                data_frame.dropna(subset=['Id RDV'], inplace=True)
                data_frame = data_frame[data_frame['Id RDV'] != '']
                data_frame.drop_duplicates(subset='Id RDV', keep='first', inplace=True)
                
                data_frame = data_frame[~data_frame['Id RDV'].isin(self.get_records())]
                data_frame = data_frame[[col for col in cols if col in data_frame.columns]]
                # Insert data into the table 
                print(f'inserting {len(data_frame)} [BULK INSERT]')
                if self.table_exists('list_int'):
                    data_frame.to_sql('list_int', con=self.engine, if_exists='append', index=False, chunksize=10000)
                else:
                    data_frame.to_sql('list_int', con=self.engine, if_exists='replace', index=False, chunksize=10000)
                print('done')
                
            except AttributeError as e:
                print(f"An AttributeError occurred: {e}")
                print(f'{traceback.format_exc()}')
                time.sleep(60)
                continue
            except pymysql.err.OperationalError as e:
                error_code, error_message = e.args
                if error_code == 2003:
                    print("Can't connect to MySQL server. Please check the server configuration.")
                elif error_code == 1129:
                    print("IP address is blocked. Unblock the IP address using 'mariadb-admin flush-hosts'.")
                else:
                    print(f"OperationalError: {error_code}, {error_message}")
                time.sleep(200)
                continue
            except Exception as e:
                print(f'DATABASE **************** {traceback.format_exc()}')
                return False
            finally:
                # Release the connection back to the pool
                self.close_session()
                return True

    def get_records(self):
        try:
            if not self.table_exists('list_int'):
                return pd.DataFrame()
            self.create_session()
            id_list=pd.DataFrame()
            id_list = pd.read_sql(f'SELECT * FROM list_int', con=self.engine) 
            return id_list['Id RDV']
        except Exception as e:
            print(e)
            return pd.DataFrame()
        finally:
            self.close_session()

    def kill_sleep(self):
        self.create_session()
        query = "SELECT CONCAT('KILL ', id, ';') AS query FROM information_schema.processlist WHERE command = 'Sleep'"

        # Execute the query
        query = text(query)
        result_ = self.session.execute(query)
        # Fetch the results
        kill_queries = result_.fetchall()

        # Execute the KILL queries
        for kill_query in kill_queries:
            self.session.execute(text(kill_query[0]))
        self.close_session()

    def get_proclist(self):
        try:
            self.create_session()
            query = text("SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST;")
            result_proxy = self.session.execute(query)
            rows = result_proxy.fetchall()
            proclist = [row[0] for row in rows]
            print(len(proclist))
            return len(proclist) - 1
        except pymysql.err.InterfaceError as e:
            # Handle the InterfaceError here
            print(f"An InterfaceError occurred: {e}")
            time.sleep(200)
            return 11
        except Exception as e:
            traceback.print_exc()
            print(e)
            return 11
        finally:
            self.close_session()



db=DatabaseManager()


def create_engine_(db_name):

    engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{db_name}")
    return engine