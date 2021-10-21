import tornado.ioloop
import tornado.web
import datetime
import json

import os
import MySQLdb

class MySQLClient:
    def get_gif(self, keyword):
        connection = MySQLdb.connect(
                host=os.environ.get('MYSQL_HOST'),
                user=os.environ.get('MYSQL_USER'),
                passwd=os.environ.get('MYSQL_PASSWORD'),
                db=os.environ.get('MYSQL_DBNAME'),
                charset='utf8')
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT *
            FROM gifs
            WHERE keyword = "%s"
            """ % (keyword)
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            return res.get("file_path")
        else:
            return None
        connection.close()


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class GifHandler(BaseHandler):
    def get(self, keyword):
        filepath = self.db.get_gif(keyword)
        if (filepath is None):
            self.clear()
            self.send_error(404)
        else:
            response_body = {"file_name": '{}?{}'.format(filepath, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))}
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(response_body))
            self.flush()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r'/gif/(.*)', GifHandler),
                (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/var/lib/aion/Data/gifs"}),
                ]
        tornado.web.Application.__init__(self, handlers)
        self.db = MySQLClient()


if __name__ == "__main__":
    app = Application()
    app.listen(os.environ.get('SERVER_PORT'))
    tornado.ioloop.IOLoop.current().start()
