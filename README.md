Magento Version Manager
=======================

Set of self contained scripts to manage the release of new Magento versions to a server.

The idea is to have a configuration file named `Magefile` which will sit within
the top level directory of a server and will configure how new versions of
Magento are released.

Example Directory Structure
---------------------------

    Site
    |-- Magefile - Configuration file
    |-- mvm.py   - Main executable
    |-- .mvm-env - Virtual environment for mvm.py
    |   `-- ...
    |-- Live     - Symlink to the current live version
    |-- v1.7.0.0 - Magento release v1.7.0.0
    |   |-- app
    |   |-- downloader
    |   |-- errors
    |   |-- includes
    |   |-- js
    |   |-- lib
    |   |-- mage
    |   |-- media
    |   |   |-- catalog - Symlinked to global image directory
    |   |   `-- ....
    |   |-- shell
    |   |-- skin
    |   |-- var
    |   `-- index.php
    |-- v1.8.0.0 - Magento release v1.8.0.0
    |   `-- ...
    |-- v1.8.1.0 - Magento release v1.8.1.0
    |   `-- ...
    |-- v1.8.1.1 - Custom change bumps minor version number
    |   `-- ...
    `-- catalog - Global store for images

Example Magefile
----------------
The Magefile is in YAML format.

    # Pointer to the live symlink
    live-symlink: Live
    # Symlink to create to the old version to aid rollback
    old-symlink: Live
    # Set if the user should be prompted before doing anything, defaults to True
    confirm: True

    # Database host or socket to connect to
    mysql-database: 192.168.2.160

    # Where the catalog images are stored
    catalog-images: catalog

    modes:
        # New install where we have a database already setup
        new:
            - MaintenanceMode
                magento-directory: release-directory
            - LocalXml
                magento-directory: release-directory
                db-host: mysql-database
                db-name: db-name
                db-pass: db-pass
                template: local-xml-template # Command line argument
            - RunIndex
                magento-directory: release-directory
            - Symlink
                live-symlink: live-symlink
                magento-directory: release-directory
            - LiveMode
                magento-directory: release-directory
        # Minor update that features no database changes
        minor:
            - MaintenanceMode
                magento-directory: live-symlink
            - MaintenanceMode
                magento-directory: release-directory
            - Copy
                old-magento: live-symlink
                new-magento: release-directory
                file: app/etc/local.xml
            - RunIndex
                magento-directory: release-directory
            - Symlink
                live-symlink: old-symlink
                magento-directory: live-release
            - Symlink
                live-symlink: live-symlink
                magento-directory: release-directory
            - LiveMode
                magento-directory: release-directory
        # Minor update that has database changes and we need to copy the database
        major:
            - MaintenanceMode
                magento-directory: live-symlink
            - MaintenanceMode
                magento-directory: release-directory
            - LocalXml
                magento-directory: release-directory
                db-host: mysql-database
                db-name: db-name
                db-pass: db-pass
            - DatabaseCopy
                db-host: mysql-database
                current-db-name: live-db-name
                current-db-user: live-db-user
                current-db-pass: live-db-pass
                new-db-name: db-name
                new-db-user: db-user
                new-db-pass: db-pass
            - RunIndex
                magento-directory: release-directory
            - Symlink
                live-symlink: old-symlink
                magento-directory: live-release
            - Symlink
                live-symlink: live-symlink
                magento-directory: release-directory
            - LiveMode
                magento-directory: release-directory


Defined steps
-------------
 - DatabaseCopy(db-host, current-db-name, current-db-user, current-db-pass, new-db-name, new-db-user, new-db-pass)
    - Copy the current live database to a new database to point the new install
      at. Only required if the update performs database changes.
 - MaintenanceMode(magento-directory)
    - Set the maintenance.flag file within the magento-directory to take
      the site temporarily offline.
 - LiveMode(magento-directory)
    - Remove the maintenance.flag file within the magento-directory to take
      the site live.
 - LocalXml(magento-directory, db-host, db-name, db-user, db-password, template=live-symlink + '/app/etc/local.xml')
    - Modify app/etc/local.xml with the new new database details. 
 - Copy(old-magento, new-magento, file)
    - Modify app/etc/local.xml with the new new database details. 
 - RunIndex(magento-directory)
    - Run index.php from the command line to force the database upgrade.
      **Requires that index.php is modified to allow command line access within maintenance mode**
 - Symlink(live-symlink, magento-directory)
    - Symlink live-symlink to the new release directory.

Avaliable variables
-------------------
 - release-directory - Directory of the current release
 - mysql-database - Database hostname
 - live-release - Pointer to the current live release - processes all symlinks from live-symlink
