import db_admin as db
import os
from scipy.io import loadmat, savemat

### Create object, connection ###
database = db.Database()
database.open_connection()

### Drop table if exists ###
database.drop_table_if_exists("cam1")

### Create table ###
database.create_table("cam1")

fpath = '/data/yilong/20180612/10F 721_192.168.1.180--20180612-111849/'
fname1 = '000154_000001_000002.mat' # everything
fname2 = '000154_000002_000003.mat' # No face

### Test case 1 ###
print("======Test case 1======")
print("Insert: new detection with full feature information")
detection = loadmat(fpath + fname1)
database.save_records("cam1", detection, datalog=True)
print("Query:")
print(database.query_records("cam1", 2))

### Test case 2 ###
print("======Test case 2======")
print("Insert: new detection with face features missing")
detection = loadmat(fpath + fname2)
database.save_records("cam1", detection, datalog=True)
print("Query:")
print(database.query_records("cam1", 3))

### Test case 3 ###
print("======Test case 3======")
print("Update: existing detection with full feature information")
detection = loadmat(fpath + fname1)
database.save_records("cam1", detection, datalog=True)
print("Query:")
print(database.query_records("cam1", 2))

### Test case 4 ###
print("======Test case 4======")
print("Update: existing detection with face features missing")
detection = loadmat(fpath + fname2)
database.save_records("cam1", detection, datalog=True)
print("Query:")
print(database.query_records("cam1", 3))

### Close connection ###
database.close_connection()
