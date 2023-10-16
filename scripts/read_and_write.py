import dask
import dask.dataframe as dd
import pymongo
import settings
import parser


@dask.delayed
def clean_snapshot(df):
    df["snapshot"] = df["snapshot"].map(parser.clean_snapshot).astype("string")
    df["words"] = df["snapshot"].map(parser.extract_snapshot_text).astype("string")
    # df = df.drop_duplicates(subset='hash')
    return df


@dask.delayed
def save_to_mongo(df):
    if len(df) > 0:
        # 连接到 MongoDB
        client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
        try:
            db = client["bidding"]
            collection = db["data_2015_01"]
            data = df.to_dict(orient='records')
            # 使用 insert_many 方法批量插入数据
            result = collection.insert_many(data)
            # 打印插入的文档的 ObjectIds（可选）
            for object_id in result.inserted_ids:
                print(f"Inserted document with ObjectId: {object_id}")
        finally:
            client.close()


if __name__ == '__main__':
    from dask.distributed import Client, LocalCluster

    cluster = LocalCluster("dev", n_workers=4, memory_limit="512 MiB", dashboard_address=":8080")
    print(cluster)
    client = Client(cluster)
    print(client.dashboard_link)

    conn = settings.PYMYSQL_URL
    columns = ["id", "hash", "source_id", "type", "category", "title", "industry", "province_id", "city_id",
               "source_url", "section", "snapshot", "extend", "archives", "version", "create_time"]
    df = dd.read_sql_table("data_2015_01", conn, index_col="public_time", columns=columns, npartitions=100,
                           limits=(1422346140, 1422423565))
    # df2 = dd.read_sql_table("data_2015_01", conn, index_col="public_time", columns=columns, npartitions=100,
    #                         limits=(1422346140, 1422423565))
    # df3 = dd.read_sql_table("data_2015_01", conn, index_col="public_time", columns=columns, npartitions=100,
    #                         limits=(1422346140, 1422423565))
    # df4 = dd.read_sql_table("data_2015_01", conn, index_col="public_time", columns=columns, npartitions=100,
    #                         limits=(1422346140, 1422423565))
    # df = df1 + df2 + df3 + df4

    works = []
    ddf = df.drop_duplicates(subset="hash").repartition(npartitions=100)
    for _df in ddf.to_delayed():
        _df = clean_snapshot(_df)
        works.append(save_to_mongo(_df))

    dask.compute(*works)
