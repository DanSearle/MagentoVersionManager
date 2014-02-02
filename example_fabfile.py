from mage_fab import mysql
from fabric.api import task, env

mysqlu = "root"
mysqlp = "root"
fromdb = "fromdb"


@task
def test_mysql():
    env.host_string = "192.168.100.138"
    env.user = "vagrant"
    env.password = "vagrant"
    conn = mysql.Connection("information_schema", mysqlu, mysqlp)
    cmd = mysql.Command(conn)
    cmd.execute("SHOW TABLES", "showtables.sql")


@task
def test_copy():
    env.host_string = "192.168.100.138"
    env.user = "vagrant"
    env.password = "vagrant"
    conn = mysql.Connection(fromdb, mysqlu, mysqlp, verbose=False)
    cmd = mysql.Command(conn)
    cmd.execute("CREATE DATABASE IF NOT EXISTS test_copy", "createdb.sql")
    to = mysql.Connection("test", mysqlu, mysqlp, verbose=False)
    copy = mysql.Copy(conn, to)
    copy.run()
    cmd.execute("DROP DATABASE test_copy", "dropdb.sql")
