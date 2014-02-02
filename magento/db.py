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
        if unsecure[1:] != "/":
            raise ValueError("unsecure url does not end with a slash('/')")
        if secure[1:] != "/":
            raise ValueError("secure url does not end with a slash('/')")

        sql = "UPDATE core_config_data SET value='{0}' WHERE path='{1}'"
        unsecure_sql = sql.format(unsecure, "web/unsecure/base_url")
        secure_sql = sql.format(secure, "web/secure/base_url")
        self._command.execute(unsecure_sql)
        self._command.execute(secure_sql)
