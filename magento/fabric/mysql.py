from fabric.api import run, put
from magento.fabric.files import readlink
from StringIO import StringIO
import time


class Connection(object):
    """ Class to specifiy the connection details for mysql and mysqldump
        commands
    """
    def __init__(self, database, username, password, host="", verbose=True):
        self._db = database
        self._username = username
        self._password = password
        self._host = host
        self._verbose = verbose

    def _is_socket(self):
        link = readlink(self._host)
        if link:
            filetype = run('file ' + link + '| awk \'{print $NF}\'')
            return filetype == "socket"
        return False

    def _get_host(self):
        if not self._host:
            return ""
        if self._is_socket():
            return "-S {0}".format(self._host)
        else:
            return "-h {0}".format(self._host)

    def _get_verbose(self):
        if self._verbose:
            return "--verbose"
        return ""

    @property
    def args(self):
        return "{4} -u {0} -p{1} {2} {3}".format(self._username,
                                                 self._password,
                                                 self._get_host(),
                                                 self._db,
                                                 self._get_verbose())


class Command(object):
    """ Wrapper around the mysql shell command to execute ad-hoc SQL statements
    """
    def __init__(self, connection, mysqlbin="/usr/bin/mysql",
                 removecmd="/bin/rm"):
        self._connection = connection
        self._removecmd = removecmd
        self._mysqlbin = mysqlbin

    @property
    def command(self):
        return "{0} {1}".format(self._mysqlbin, self._connection.args)

    def execute(self, sql, sqlfile=None):
        """ Run the given SQL statements through the mysql shell command. The
            sqlfile variable gives a filename to temporarily store the SQL
            command in, if this is null the current date and time is used
            as a filename.
        """
        if not sqlfile:
            sqlfile = time.strftime("%Y%m%d_%H:%M:%S.sql")
        cmd = self.command
        sql_io = StringIO(sql)
        put(sql_io, sqlfile)
        run("{0} < {1}".format(cmd, sqlfile))
        run("{0} {1}".format(self._removecmd, sqlfile))


class Copy(object):
    """ Wrapper around mysqldump and mysql to copy a database """
    def __init__(self, from_connection, to_connection):
        self._from = from_connection
        self._to = Command(to_connection)

    def run(self):
        dumpcmd = "mysqldump --opt --single-transaction " + self._from.args
        run("{0} | {1}".format(dumpcmd, self._to.command))
