import pymysql
import numpy as np
import sql_encode as encode
import os
from scipy.io import savemat, loadmat

# Global variable setup
"""
dimensions = {
    'face_bbox':         4,
    'face_confidence':   1,
    'face_embed':        512,
    'face_keypoint':     10,
    'person_bbox':       4,
    'person_confidence': 1,
    'person_embed':      128
}
"""
dimensions = {
    'face_bbox':         4,
    'face_confidence':   1,
    'face_embed':        2,
    'face_keypoint':     3,
    'person_bbox':       4,
    'person_confidence': 1,
    'person_embed':      2
}

# Create table
def create_table(cam_name, max_track_length=100):
    sql = "create table " + cam_name \
        + " (s_tracklet_num int primary key not null, s_elan_id int, "

    for key in sorted(dimensions.keys()):
        for dim in range(dimensions[key]):
            #sql += (key + str(dim) + " blob, ")
            sql += (key + str(dim) + " varchar(" + str(8*max_track_length) + "), ")

    sql += "timestamp datetime)"

    cursor.execute(sql)
    cnx.commit()
    print("Created table " + cam_name)

# Insert data
def insert_records(cam_name, det, datalog=False):
    s_tracklet_num = det['s_tracklet_num'].ravel()[0]
    cursor.execute("select*from "+ cam_name +" where s_Tracklet_num=" + str(s_tracklet_num))
    res = cursor.fetchone()

    # Execute update if s_tracklet_num exists
    if res!=None:
        print("Track number exists")
        sql = "update " + cam_name + " set "

        for key in sorted(dimensions.keys()):
            if len(det[key]) != 0:
                values = det[key].ravel()
            else:
                values = np.zeros(dimensions[key],dtype=float)

            if datalog==True:
                print(key)
                print(values[0:dimensions[key]])

            for dim in range(dimensions[key]):
                sql += (key + str(dim) + "=concat(" + key + str(dim) + ",")
                sql += ("\'" + encode.dec2hex(float(values[dim])) + "\'),")

        sql += ("timestamp='" + encode.datetime_format(2018, 10, 3, 21, 55, 28))
        sql += ("' where s_tracklet_num = "+str(s_tracklet_num))

        cursor.execute(sql)
        cnx.commit()

    # Else insert new row
    else:
        print("Assigned new track number")
        sql = "insert into `" + cam_name + "` (s_tracklet_num, "

        for key in sorted(dimensions.keys()):
            for dim in range(dimensions[key]):
                sql += (key + str(dim)+",")

        sql += ("timestamp) values(" + str(s_tracklet_num) + ",")
        for key in sorted(dimensions.keys()):
            if len(det[key]) != 0:
                values = det[key].ravel()
            else:
                values = np.zeros(dimensions[key],dtype=float)

            if datalog==True:
                print(key)
                print(values[0:dimensions[key]])

            for dim in range(dimensions[key]):
                sql += ("\'" + encode.dec2hex(float(values[dim])) + "\', ")

        sql += "\'" + encode.datetime_format(2018, 11, 21, 05, 16, 2) + "\')"
        cursor.execute(sql)
        cnx.commit()

    return s_tracklet_num

def query_records(cam_name, s_tracklet_num):
    sql = "select*from " + cam_name + " where s_tracklet_num=" + str(s_tracklet_num)
    if(cursor.execute(sql))==0:
        print("Track not found")
        return
    else:
        for(f_data) in cursor:
            records = {
                       's_tracklet_num': s_tracklet_num,
                       's_elan_id':      f_data[1]
                      }
            index = 2
            for key in sorted(dimensions.keys()):
                records[key] = encode.hex2dec(list(f_data[index:(index + dimensions[key])]))
                index += dimensions[key]

            return records

#################################################################################

def insert(test_case):
    fpath = '/data/yilong/20180612/10F 721_192.168.1.180--20180612-111849/'
    if test_case==1:
        fname = '000154_000001_000002.mat' # everything
    elif test_case==2:
        fname = '000154_000002_000003.mat' # No face

    detection = loadmat(fpath+fname)
    tracklet_num = insert_records("cam1", detection, datalog=True)

def query(test_case):
    if test_case==1:
        tracklet_num = 2
    elif test_case==2:
        tracklet_num = 3
    print("{Query results}")
    print(query_records("cam1", tracklet_num))

###############################################################################

config = {
    'user': 'root',
    'password': 'asdfghjkl',
    'host': '127.0.0.1',
    'database': 'surveillance'
}
# Create connection object 'cnx' and cursor
cnx = pymysql.connect(**config)
cursor = cnx.cursor()

# Create table
create_table("cam1", max_track_length=10)
insert(test_case=1)
query(test_case=1)

cursor.close()
cnx.close()
