import dask
import dask.dataframe as dd
import settings


if __name__ == '__main__':
    from dask.distributed import Client

    client = Client("192.168.1.13:8786")

    conn = settings.PYMYSQL_URL
    columns = ["id", "hash", "source_id", "type", "category", "title", "industry", "province_id", "city_id",
               "source_url", "section", "snapshot", "extend", "archives", "version", "create_time"]
    df = dd.read_sql_table("data_2015_01", conn, index_col="public_time", columns=columns, npartitions=100,
                            limits=(1422346140, 1422423565))

    df.compute()