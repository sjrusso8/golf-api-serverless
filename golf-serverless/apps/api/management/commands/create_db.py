from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import environ

env = environ.Env()

class Command(BaseCommand):
    help = 'Creates the initial database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting db creation'))

        rds_host = env.str('AURORA_ENDPOINT')
        db_name = env.str('AURORA_DB')
        user_name = env.str('AURORA_ADMIN')
        password = env.str('AURORA_PASSWORD')
        port = 5432

        con = None
        con = connect(dbname='postgres', user=user_name, host=rds_host, password=password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + db_name)
        cur.close()
        con.close()

        self.stdout.write(self.style.SUCCESS('All Done'))