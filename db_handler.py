import sqlite3
from custom_logger import *
from configuration import InfoForTables
from get_product import GetProductList

try:
    from tabulate import tabulate
except ImportError:
    logger.error("Must be installed module {}"
                 "\n Try 'python -m pip install tabulate'".format(__name__))
    quit()

DATABASE_NAME = "coffee_for_me.db"


class DataBaseConfiguration:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except Exception as exc:
            logger.error("'{}' When trying to connect to '{}'".format(exc, self.db_name))
            quit()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class DataBaseHandler(object):

    def __init__(self, database=DATABASE_NAME):
        self.database = database
        self.create_tables()

    def create_tables(self):
        with DataBaseConfiguration(self.database) as database:
            try:
                database.execute("""CREATE TABLE IF NOT EXISTS STAFF (NAME TEXT, POSITION TEXT)""")
                database.execute("""CREATE TABLE IF NOT EXISTS COFFEE_PRICE (COFFEE TEXT, PRICE INTEGER FLOAT)""")
                database.execute("""CREATE TABLE IF NOT EXISTS ADDITIVE_PRICE (ADDITIVE TEXT, PRICE INTEGER FLOAT)""")
                database.execute('''CREATE TABLE  IF NOT EXISTS SALES (NAME TEXT, 
                                                                       \"NUMBER OF SALES\" INTEGER FLOAT, 
                                                                       \"TOTAL VALUE\" REAL)''')
            except Exception as exc:
                logger.error("'{}' while executing the method 'create_tables'".format(exc))
                quit()

    def insert_table_staff(self, user_tuple):
        with DataBaseConfiguration(self.database) as database:
            try:
                if not self._user_exist(user_tuple):
                    database.execute("INSERT INTO STAFF VALUES (?,?)", user_tuple)
            except Exception as exc:
                logger.error("'{}' while executing the method 'update_table_staff'".format(exc))
                quit()

    def insert_table_coffee_price(self, coffee_price):
        with DataBaseConfiguration(self.database) as database:
            try:
                if not self._coffee_exist(coffee_price):
                    database.execute("INSERT INTO COFFEE_PRICE VALUES (?,?)", coffee_price)
            except Exception as exc:
                logger.error("'{}' while executing the method 'update_table_coffee_price'".format(exc))
                quit()

    def insert_table_additive_price(self, additive_price):
        with DataBaseConfiguration(self.database) as database:
            try:
                if not self._additive_exist(additive_price):
                    database.execute("INSERT INTO ADDITIVE_PRICE VALUES (?,?)", additive_price)
            except Exception as exc:
                logger.error("'{}' while executing the method 'update_table_additive_price'".format(exc))
                quit()

    def insert_table_sales(self, user_tuple):
        with DataBaseConfiguration(self.database) as database:
            try:
                name, position = user_tuple
                if not self._sales_exist(user_tuple) and position == 'SALESMAN':
                    database.execute("INSERT INTO SALES VALUES (?,?,?)", (name, 0, 0,))
            except Exception as exc:
                logger.error("'{}' while executing the method 'update_table_sales'".format(exc))
                quit()

    def update_table_sales(self, name, sale_list):
        with DataBaseConfiguration(self.database) as database:
            try:
                price = self.get_overall_price(sale_list)
                database.execute('SELECT \"NUMBER OF SALES\", \"TOTAL VALUE\" FROM SALES WHERE NAME = ?', (name,))
                number_of_sales, total_value = database.fetchone()
                if price != 0:
                    number_of_sales += 1
                    total_value += price
                    database.execute(
                        'UPDATE SALES SET \"NUMBER OF SALES\" = ?, \"TOTAL VALUE\" = ? WHERE NAME = ?',
                        (number_of_sales,
                         total_value,
                         name,))
            except Exception as exc:
                logger.error("'{}' while executing the method 'rewrite_table_sales'".format(exc))
                quit()

    def init_tables(self, info):
        self.create_tables()
        for user_tuple in info.staff_tuple():
            self.insert_table_staff(user_tuple)
            self.insert_table_sales(user_tuple)

        for coffee_price_tuple in info.coffee_price_tuple():
            self.insert_table_coffee_price(coffee_price_tuple)

        for additive_price_tuple in info.additive_price_tuple():
            self.insert_table_additive_price(additive_price_tuple)

    def _check_table(self, query, params):
        with DataBaseConfiguration(self.database) as database:
            try:
                database.execute(query, params)
                result = database.fetchall()
                return result
            except Exception as exc:
                logger.error("'{}' while executing query  '{}'".format(exc, query))
                quit()

    def check_table_staff(self, user_tuple):
        name, position = user_tuple
        return self._check_table('SELECT * FROM STAFF WHERE NAME = ? AND POSITION = ?', (name, position,))

    def check_table_coffee(self, coffee_price):
        coffee, price = coffee_price
        return self._check_table('SELECT * FROM COFFEE_PRICE WHERE COFFEE = ? AND PRICE = ?', (coffee, price,))

    def check_table_additive(self, additive_price):
        additive, price = additive_price
        return self._check_table('SELECT * FROM ADDITIVE_PRICE WHERE ADDITIVE = ? AND PRICE = ?', (additive, price,))

    def check_table_sales(self, user_tuple):
        name, position = user_tuple
        return self._check_table('SELECT * FROM SALES WHERE NAME = ?', (name,))

    def _user_exist(self, user_tuple):
        return bool(self.check_table_staff(user_tuple))

    def _coffee_exist(self, coffee_price):
        return bool(self.check_table_coffee(coffee_price))

    def _additive_exist(self, additive_price):
        return bool(self.check_table_additive(additive_price))

    def _sales_exist(self, user_tuple):
        return bool(self.check_table_sales(user_tuple))

    def add_user(self, user_tuple):
        if self._user_exist(user_tuple):
            print('Logging as a {} - {}'.format(user_tuple[0], user_tuple[1]))
        else:
            self.insert_table_staff(user_tuple)
            self.insert_table_sales(user_tuple)
            print('User {} added as {}'.format(user_tuple[0], user_tuple[1]))

    def _beverage_list(self, query):
        with DataBaseConfiguration(self.database) as database:
            try:
                database.execute(query)
                coffee_data = database.fetchall()
                return [GetProductList(rowid, name, price) for rowid, name, price in coffee_data]
            except Exception as exc:
                logger.error("'{}' while executing the method 'beverage_list'".format(exc, query))
                quit()

    def coffee_list(self):
        return self._beverage_list('SELECT ROWID,* FROM COFFEE_PRICE')

    def additive_list(self):
        return self._beverage_list('SELECT ROWID,* FROM ADDITIVE_PRICE')

    def view_coffee_list(self):
        try:
            coffee_source = self.coffee_list()
            coffee_menu = [beverage.get_tuple_to_product() for beverage in coffee_source]
            columns = ['POS', 'COFFEE', 'PRICE']
            return tabulate(coffee_menu, headers=columns, tablefmt="pipe", )
        except Exception as exc:
            logger.error("'{}' while executing the method 'view_coffee_list'".format(exc))
            quit()

    def view_additive_list(self):
        try:
            additive_source = self.additive_list()
            additive_menu = [beverage.get_tuple_to_product() for beverage in additive_source]
            columns = ['POS', 'ADDITIVE', 'PRICE']
            return tabulate(additive_menu, headers=columns, tablefmt="pipe", )
        except Exception as exc:
            logger.error("'{}' while executing the method 'view_additive_list'".format(exc))
            quit()

    def return_coffee_dict(self):
        return {str(coffee.rowid): coffee for coffee in self.coffee_list()}

    def return_additive_dict(self):
        return {str(additive.rowid): additive for additive in self.additive_list()}

    def return_statistic(self):
        with DataBaseConfiguration(self.database) as database:
            try:
                database.execute('SELECT * FROM SALES')
                columns = ['Seller name', 'Number of sales', 'Total value($)']
                print(tabulate(database.fetchall(), headers=columns, tablefmt="pipe", ) + '\n')
            except Exception as exc:
                logger.error("'{}' while executing the method 'return_statistic'".format(exc))
                quit()

    @staticmethod
    def get_overall_price(order):
        with open('bill.txt', 'w') as file:
            file.write(str(sum(product.price for product in order)))
            return round(sum(product.price for product in order), 2)


info_for_tables = InfoForTables()
data_base_handler = DataBaseHandler()
data_base_handler.init_tables(info_for_tables)
