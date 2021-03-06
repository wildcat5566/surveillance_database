import pymysql
import numpy as np
import sql_encode as encode
import os
from scipy.io import loadmat, savemat

class Database():
    def __init__(self):
        self.dimensions = {
            'face_bbox':         4,
            'face_confidence':   1,
            'face_embed':        512,
            'face_keypoint':     10,
            'person_bbox':       4,
            'person_confidence': 1,
            'person_embed':      128
        }
        """
        self.dimensions = {
            'face_bbox':         4,
            'face_confidence':   1,
            'face_embed':        2,
            'face_keypoint':     3,
            'person_bbox':       4,
            'person_confidence': 1,
            'person_embed':      2
        }
        """

        self.config = {
            'user': 'root',
            'password': 'asdfghjkl',
            'host': '127.0.0.1',
            'database': 'surveillance'
        }

        self.cnx = None
        self.cursor = None

    def open_connection(self):
        self.cnx = pymysql.connect(**self.config)
        self.cursor = self.cnx.cursor()

    def close_connection(self):
        self.cursor.close()
        self.cnx.close()

    # Create table
    def create_table(self, cam_name, max_track_length=10):
        sql = "create table " + cam_name \
            + " (s_tracklet_num int primary key not null, s_elan_id int, "

        for key in sorted(self.dimensions.keys()):
            for dim in range(self.dimensions[key]):
                if('bbox' in key) or ('confidence' in key):
                    sql += (key + str(dim) + " varchar(" + str(8*max_track_length) + "), ")
                else: # Embedded & keypoints
                    sql += (key + str(dim) + " float, ")

        sql += "timestamp datetime)"

        self.cursor.execute(sql)
        self.cnx.commit()
        print("Created table " + cam_name)

    # Drop duplicated table if needed
    def drop_table_if_exists(self, cam_name):
        sql = "drop table if exists " + cam_name
        self.cursor.execute(sql)
        self.cnx.commit()

    # Save new detection
    def save_records(self, cam_name, det, datalog=False):
        s_tracklet_num = det['s_tracklet_num'].ravel()[0]
        self.cursor.execute("select*from "+ cam_name +" where s_Tracklet_num=" + str(s_tracklet_num))
        res = self.cursor.fetchone()

        # Execute update if s_tracklet_num exists
        if res!=None:
            self.update_records(cam_name, det, s_tracklet_num, datalog)

        # Else insert new row
        else:
            self.insert_records(cam_name, det, s_tracklet_num, datalog)

    # Insert new records
    def insert_records(self, cam_name, det, s_tracklet_num, datalog):
        print("Assigned new track number")
        sql = "insert into `" + cam_name + "` (s_tracklet_num, "

        for key in sorted(self.dimensions.keys()):
            for dim in range(self.dimensions[key]):
                sql += (key + str(dim)+",")

        sql += ("timestamp) values(" + str(s_tracklet_num) + ",")
        for key in sorted(self.dimensions.keys()):
            if len(det[key]) != 0:
                values = det[key].ravel()
            else:
                values = np.zeros(self.dimensions[key],dtype=float)

            if datalog==True:
                print(key)
                print(values[0:self.dimensions[key]])

            for dim in range(self.dimensions[key]):
                if ('bbox' in key) or ('confidence' in key):
                    sql += ("\'" + encode.dec2hex(float(values[dim])) + "\', ")
                else:
                    sql += (str(values[dim]) + ", ")

        sql += "\'" + encode.datetime_format(2018, 11, 21, 5, 16, 2) + "\')"
        self.cursor.execute(sql)
        self.cnx.commit()

    # Update existing records
    def update_records(self, cam_name, det, s_tracklet_num, datalog):
        print("Track number exists")
        sql = "update " + cam_name + " set "

        for key in sorted(self.dimensions.keys()):
            if len(det[key]) != 0:
                values = det[key].ravel()
            else:
                values = np.zeros(self.dimensions[key],dtype=float)

            if datalog==True:
                print(key)
                print(values[0:self.dimensions[key]])

            for dim in range(self.dimensions[key]):
                if ('bbox' in key) or ('confidence' in key):
                    sql += (key + str(dim) + "=concat(" + key + str(dim) + ",")
                    sql += ("\'" + encode.dec2hex(float(values[dim])) + "\'),")

                else:
                    sql += (key + str(dim) + "=" + str(values[dim]) + ",")

        sql += ("timestamp='" + encode.datetime_format(2018, 10, 3, 21, 55, 28))
        sql += ("' where s_tracklet_num = "+str(s_tracklet_num))

        self.cursor.execute(sql)
        self.cnx.commit()

    # Query records
    def query_records(self, cam_name, s_tracklet_num):
        sql = "select*from " + cam_name + " where s_tracklet_num=" + str(s_tracklet_num)
        if(self.cursor.execute(sql))==0:
            print("Track not found")
            return
        else:
            for(f_data) in self.cursor:
                records = {
                    's_tracklet_num': s_tracklet_num,
                    's_elan_id':      f_data[1]
                }
                index = 2
                for key in sorted(self.dimensions.keys()):
                    if ('bbox' in key) or ('confidence' in key):
                        records[key] = encode.hex2dec(list(f_data[index:(index + self.dimensions[key])]))
                    else:
                        records[key] = f_data[index:(index + self.dimensions[key])]
                    index += self.dimensions[key]

                return records
