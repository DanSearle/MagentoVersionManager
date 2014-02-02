from magento.fabric import mysql
from fabric.api import task, env


@task
def test_mysql():
    env.host_string = "192.168.100.138"
    env.user = "vagrant"
    env.password = "vagrant"
    sql = mysql.Connection("information_schema", "root", "password")
    sql.run("SHOW TABLES", "showtables.sql")


@task
def test_copy():
    env.host_string = "192.168.100.138"
    env.user = "vagrant"
    env.password = "vagrant"
    sql = mysql.Connection("fromdb", "root", "password")
    sql.run("CREATE DATABASE test_copy", "createdb.sql")
    to = mysql.Connection("test", "root", "password")
    copy = mysql.Copy(sql, to)
    copy.run()
    sql.run("DROP DATABASE test_copy", "createdb.sql")
