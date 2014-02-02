Magento Version Manager
=======================

Set of python modules for managing Magento versions and deployment using fabric.

*Note that this is very alpha software*

Adding to an existing project
-----------------------------

If you are using fabfile.py:
```
git submodule add git@github.com:DanSearle/MagentoVersionManager.git mvm
git submodule update  --init
```

If you are using fabfile directory:
```
git submodule add git@github.com:DanSearle/MagentoVersionManager.git fabfile/mvm
git submodule update  --init
```

Using this repository as a submodule you can then access the Python module
through standard Python imports. E.g.
```
import mvm.magento.fabric.mysql
import mvm.magento.db
```

To update to the latest master:
```
cd {fabfile}/mvm
git pull
cd ..
git commit -m 'Updated to latest MagentoVersionManager'
```
