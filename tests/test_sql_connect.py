import unittest


class MyTestCase(unittest.TestCase):
    def test_sqlalchemy(self):
        import sqlalchemy as sa

        engine = sa.create_engine('mysql+pymysql://bidding_select:qweqwe123@47.119.179.158/bidding')
        with engine.connect() as connect:
            while True:
                exc = connect.execute(sa.select("*").select_from(sa.table("data_2023_06")))
                data = exc.fetchmany(200)
                self.assertIsNotNone(data)

    def test_pymysql(self):
        import pymysql.cursors

        # Connect to the database
        connection = pymysql.connect(host='47.119.179.158',
                                     user='bidding_select',
                                     password='qweqwe123',
                                     database='bidding',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                query = "SELECT * FROM data_2023_09 limit 1"
                cursor.execute(query)
                print(cursor.fetchone())


if __name__ == '__main__':
    unittest.main()
