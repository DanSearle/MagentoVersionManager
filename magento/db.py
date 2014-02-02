""" Module with common database commands for Magento """


class UpdateUrls(object):
    """ Update the web/unsecure/base_url and web/secure/baseurl configuration
        variables. Provided to change an imported production database to a
        different url. E.g. to create a development server.
    """
    def __init__(self, command):
        self._command = command

    def update(self, unsecure, secure):
        """ Update the unsecure and secure urls in configuration.
            Note that both URLs should end with a slash ('/')
        """
        if unsecure[-1:] != "/":
            raise ValueError("unsecure url does not end with a slash('/')")
        if secure[-1:] != "/":
            raise ValueError("secure url does not end with a slash('/')")

        sql = "UPDATE core_config_data SET value='{0}' WHERE path='{1}'"
        unsecure_sql = sql.format(unsecure, "web/unsecure/base_url")
        secure_sql = sql.format(secure, "web/secure/base_url")
        self._command.execute(unsecure_sql)
        self._command.execute(secure_sql)


class DeleteLogTables(object):
    """ Delete old data from the log_* tables in order to shrink the Magento
        database down to size. This will also make the sales_flat_quote table
        smaller.

        Recommend you take an entire database backup before running this
        command.
    """
    script = """
SET @cutoff_date = DATE_SUB(Now(),INTERVAL {0} DAY);

DELETE log_visitor_info FROM `log_url`,`log_visitor_info` WHERE
    `log_visitor_info`.visitor_id=`log_url`.visitor_id AND
    visit_time < @cutoff_date;

DELETE log_url_info FROM `log_url`,`log_url_info` WHERE
    `log_url_info`.url_id=`log_url`.url_id AND visit_time < @cutoff_date;

DELETE log_url FROM `log_url` WHERE visit_time < @cutoff_date;

DELETE log_visitor FROM `log_visitor` WHERE last_visit_at < @cutoff_date;
DELETE FROM `log_quote` WHERE created_at < @cutoff_date;
DELETE FROM `sales_flat_quote` WHERE updated_at < @cutoff_date;
"""

    def __init__(self, command):
        self._command = command

    def delete(self, n_days):
        """ Run the delete command from the database.

            :param n_days: Number of days to keep
            :type n_days: integer
        """
        if n_days < 0:
            raise ValueError("n_days cannot be negative")

        self._command.execute(DeleteLogTables.script.format(n_days))


class DbSize(object):
    """ Get the current size of the entire Magento database """
    ## FIXME: Currently this just prints to the command line
    script = """
SELECT CONCAT( SUM(ROUND((data_length + index_length)/(1024*1024*1024),2)),"G")
FROM information_schema.TABLES
ORDER BY data_length + index_length DESC
"""

    def __init__(self, command):
        self._command = command

    def get_size(self, database):
        """ Run the database size query at the database.

            :param database: Database name to get the size of
            :type n_days: str
        """

        self._command.execute(DbSize.script.format(database))
