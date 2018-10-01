import pymysql
import numpy as np

# Global variable setup
features_dim = 4

# Utility
def digit_format(number):
    if number < 10:
        return '0'+str(number)
    else:
       return str(number)

def date_format(YYYY, MM, DD, hh, mm, ss):
    formatted = str(YYYY) + '-' + digit_format(MM) + '-' + digit_format(DD) \
    + ' ' + digit_format(hh) + ":" + digit_format(mm) + ":" + digit_format(ss)
    return formatted

# Populate STAFF database DO NOT USE EXCEPT INITIALIZAION
def populate_staff():
    id = [1,2,3,4]
    name = ['James', 'Tiffany', 'Angela', 'Albert']
    features = np.random.rand(4,4)
    for i in range(4):
        timestamp = date_format(2018, 10, 1, \
                    np.random.randint(0, 24), np.random.randint(0, 60), np.random.randint(0, 60))

        add_sql = ("insert into `STAFF`" \
                   "(id, name, face_feature0, face_feature1," \
                   "person_feature0, person_feature1, timestamp)" \
                   "values(%s, %s, %s, %s, %s, %s, %s)")
        sql = (id[i], name[i], float(features[i][0]), float(features[i][1]), \
               float(features[i][2]), float(features[i][3]), timestamp)
        cursor.execute(add_sql, sql)
        cnx.commit()

# Populate GUEST database DO NOT USE EXCEPT INITIALIZATION
def populate_guest():
    id = [1]
    name = ['Wild']
    features = np.random.rand(1,4)
    for i in range(1):
        timestamp = date_format(2018, 10, 1, \
                    np.random.randint(0, 24), np.random.randint(0, 60), np.random.randint(0, 60))

        add_sql = ("insert into `GUEST`" \
                   "(id, name, face_feature0, face_feature1," \
                   "person_feature0, person_feature1, timestamp)" \
                   "values(%s, %s, %s, %s, %s, %s, %s)")
        sql = (id[i], name[i], float(features[i][0]), float(features[i][1]), \
               float(features[i][2]), float(features[i][3]), timestamp)
        cursor.execute(add_sql, sql)
        cnx.commit()

# New guest
def new_guest(name, features):
    cursor.execute("select max(id) from GUEST")
    id = cursor.fetchone()[0] + 1
    timestamp = date_format(2018, 10, 1, \
                np.random.randint(0, 24), np.random.randint(0, 60), np.random.randint(0, 60))
    sql = ("insert into `GUEST`" \
           "(id, name, face_feature0, face_feature1," \
           "person_feature0, person_feature1, timestamp)" \
           "values(%s, %s, %s, %s, %s, %s, %s)")
    content = (id, name, float(features[0]), float(features[1]), \
               float(features[2]), float(features[3]), timestamp)
    cursor.execute(sql, content)
    cnx.commit()
    return id

# Update features
def feature_update(id, features, database):
    query = ("select `face_feature0`, `face_feature1`, "\
             "`person_feature0`, `person_feature1` from `" + database + "` where id = %s")
    cursor.execute(query, id)
    for (f_data) in cursor:
        print("filed features: ")
        print(f_data)
        print("New features: ")
        print(features)

    sql = ("update " + database + " set face_feature0 = %s, face_feature1 = %s, "\
             "person_feature0 = %s, person_feature1 = %s where id=%s")
    content = (float(features[0]), float(features[1]), float(features[2]), float(features[3]), id)
    cursor.execute(sql, content)
    cnx.commit()

# Matching process
def database_match(features, database):
    assert database == "STAFF" or database == "GUEST"
    cursor.execute("select max(id) from " + database)
    people_count = cursor.fetchone()[0]

    match_id = None
    match_name = None
    match_threshold = 0.01 # Match threshold

    for i in range(people_count+1):
        distance = 0

        sql = ("select `face_feature0`, `face_feature1`, "\
               "`person_feature0`, `person_feature1`, `name` from `" + database + "` where id = %s")
        cursor.execute(sql, i)

        for (f_data) in cursor:
            for dim in range(features_dim):
                distance += (features[dim] - f_data[dim])*(features[dim] - f_data[dim])

            if distance < match_threshold:
                match_threshold = distance
                match_id = i
                match_name = f_data[4]

    return match_id, match_name, match_threshold

def person_match(features):

    match_id, match_name, match_threshold = database_match(features, "STAFF")
    if match_id:
        print ("Matching staff id: %s, Name: %s, distance: %s" % (match_id, match_name, match_threshold))
        return

    match_id, match_name, match_threshold = database_match(features, "GUEST")
    if match_id:
        print ("Matching guest id: %s, Name: %s, distance: %s" % (match_id, match_name, match_threshold))
        return

    new_name = "Invader"
    new_id = new_guest(new_name, features)
    print("New guest filed. Guest id: %s, Name: %s" % (new_id, new_name))
    return

#########################################################################################
# Database configurations
config = {
    'user': 'root',
    'password': 'asdfghjkl',
    'host': '127.0.0.1',
    'database': 'surveillance'
}

# Create connection object 'cnx' and cursor
cnx = pymysql.connect(**config)
cursor = cnx.cursor()

# People start to enter room
person_match([0.6299, 0.0149, 0.3027, 0.8854])
person_match([0.8266, 0.0789, 0.5635, 0.6624])
person_match([0.1363, 0.8288, 0.2416, 0.9224])
#person_match(np.random.rand(features_dim))

feature_update(3, [0.6299, 0.0149, 0.3027, 0.8854], "STAFF")

cursor.close()
cnx.close()
