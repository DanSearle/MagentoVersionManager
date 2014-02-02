from fabric.api import run, put
from magento.fabric.files import readlink
from StringIO import StringIO
import time


class Connection(object):
    """ Wrapper around the mysql shell command to execute ad-hoc SQL statements
    """
    def __init__(self, database, username, password, host="",
                 mysqlbin="/usr/bin/mysql", verbose=True,
                 removecmd="/bin/rm"):
        self._db = database
        self._username = username
        self._password = password
        self._host = host
        self._mysqlbin = mysqlbin
        self._verbose = verbose
        self._removecmd = removecmd

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

    def _command(self):
        return "{0} {5} -u {1} -p{2} {3} {4}".format(self._mysqlbin,
                                                     self._username,
                                                     self._password,
                                                     self._get_host(),
                                                     self._db,
                                                     self._get_verbose())

    def run(self, sql, sqlfile=None):
        """ Run the given SQL statements through the mysql shell command. The
            sqlfile variable gives a filename to temporarily store the SQL
            command in, if this is null the current date and time is used
            as a filename.
        """
        if not sqlfile:
            sqlfile = time.strftime("%Y%m%d_%H:%M:%S.sql")
        cmd = self._command()
        sql_io = StringIO(sql)
        put(sql_io, sqlfile)
        run("{0} < {1}".format(cmd, sqlfile))
        run("{0} {1}".format(self._removecmd, sqlfile))

class Copy(object):
    """ Wrapper around mysqldump and mysql to copy a database """
    def __init__(self, from_connection, to_connection):
        self._from = from_connection
        self._to = to_connection

    def run(self):
        dumpcmd = "mysqldump --opt --single-transaction " + \
                  "{3} -u{0} -p{1} {2}".format(self._from._username,
                                               self._from._password,
                                               self._from._db,
                                               self._from._get_host())
        run("{0} | {1}".format(dumpcmd, self._to._command()))

