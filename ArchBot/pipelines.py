# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import charset



class MySQLPipeline(object):
    # 构造函数
    def __init__(self, host, database, port, user, password):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        try:
            # 查重
            self.cursor.execute("""select * from gdcl.news where title=%s""", item['title'])
            repetition = self.cursor.fetchone()

            if repetition:
                pass
            else:
                # 插入数据
                self.cursor.execute(
                    """insert into gdcl.news(title, article, date) VALUES (%s,%s,%s)""",(item['title'], item['content'], item['date'])
                )

            self.db.commit()

        except Exception as error:
            print(error)

        return item
