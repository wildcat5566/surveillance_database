import pymysql
import numpy as np
import sql_encode as encode

import os
from scipy.io import savemat, loadmat

# Global variable setup
dimensions = {'face_bbox':         4,
              'face_confidence':   1,
              'face_embed':        2,
              'face_keypoint':     3,
              'person_bbox':       4,
              'person_confidence': 1,
              'person_embed':      2
             }

# Create table
def create_table(cam_name):
    sql = "create table " + cam_name \
        + " (s_tracklet_num int primary key not null, s_elan_id int, "

    for key in sorted(dimensions.keys()):
        for dim in range(dimensions[key]):
            sql += (key + str(dim) + " varchar(10), ")

    sql += "timestamp datetime)"

    cursor.execute(sql)
    cnx.commit()

# Insert data
def insert_data(cam_name, fname):
    tracklet = loadmat(fname)
    s_tracklet_num = tracklet['s_tracklet_num'].ravel()[0]

    cursor.execute("select*from "+ cam_name +" where s_Tracklet_num=" + str(s_tracklet_num))
    res = cursor.fetchone()

    # Execute update if s_tracklet_num exists
    if res!=None:
        print("Track number exists")
        sql = "update " + cam_name + " set "

        for key in sorted(dimensions.keys()):
            if len(tracklet[key]) != 0:
                values = tracklet[key].ravel()
                for dim in range(dimensions[key]):
                    sql += (key + str(dim) + "= \'" + encode.dec2hex(float(values[dim])) + "\', ")
        sql += ("time='" + encode.datetime_format(2018, 10, 3, 21, 34, 27))
        sql += ("' where s_tracklet_num = "+str(s_tracklet_num))

        cursor.execute(sql)
        cnx.commit()

    # Else insert new row
    else:
        print("Assigned new track number")
        sql = "insert into `" + cam_name + "` (s_tracklet_num, "

        for key in sorted(dimensions.keys()):
            if len(tracklet[key]) != 0:
                for dim in range(dimensions[key]):
                    sql += (key + str(dim)+",")

        sql += ("time) values(" + str(s_tracklet_num) + ",")
        for key in sorted(dimensions.keys()):
            if len(tracklet[key]) != 0:
                values = tracklet[key].ravel()
                for dim in range(dimensions[key]):
                   sql += ("\'" + encode.dec2hex(float(values[dim])) + "\', ")
        sql += "\'" + encode.datetime_format(2018, 11, 21, 05, 16, 2) + "\')"

        cursor.execute(sql)
        cnx.commit()

#################################################################################
config = {
    'user': 'root',
    'password': 'asdfghjkl',
    'host': '127.0.0.1',
    'database': 'surveillance'
}

# Create connection object 'cnx' and cursor
cnx = pymysql.connect(**config)
cursor = cnx.cursor()


fpath = '/data/yilong/20180612/10F 721_192.168.1.180--20180612-111849/'
fname = '000154_000001_000002.mat'
insert_data("cam1", fpath+fname)

cursor.close()
cnx.close()
