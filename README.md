# surveillance_database
IIS, Academia Sinica

## Introduction
MySQL feature database associative with multi-camera pedestrian tracking & reidentifying system, implemented with YOLO v3. <br />
Purpose is to store & match features of each distinct employee or recorded guests. <br />

## Input data
Each received "detection" contains the following pedestrian feature sets and their dimensions: <br />
> face_bbox         : 4  <br />
> face_confidence   : 1  <br />
> face_embedded     : 512<br />
> face_keypoints    : 10 <br />
> person_bbox       : 4  <br />
> person_confidence : 1  <br />
> person_embedded   : 128<br />

"Bounding boxes" and "confidences" must be stored in the form of a sequence, since objects are tracked through a sequential video. <br />
In all detections, "person" related features always exist, while "face" related features doesn't necessarily do <br />
(for example when captured person is facing away from the camera.) <br />

## Functionalities
All functions are in object-oriented class form. <br />
Usage of basic functions provided in "db_testscript.py" file. <br />

### class object
Class object is initialized with attribution "dimensions" in dictionary form, carrying feature set names as keys and corresponding dimensions as values. <br />
There is also a "config" attribution for database connection settings, along with empty connection and cursor objects. <br />

### create_table()
Create table with given name. <br />
Columns are generated automatically, referring to pre-defined dimensions and datatypes in the dictionary attribution. <br />
Non-extending features including embedded and keypoint features are stored in single column, single value. <br />
Extending (through sequence) features including bboxes and confidence scores are encoded as fix-lengthed strings. <br />

### save_records()
Manage new detection input. <br />
The detection is already assigned with a tracking ID from the YOLO algorithm. The assigned tracking ID is matched against all stored records. <br />
(1) A tracking ID match indicates that detected person should be someone familiar (either filed employee or guest). Features are to be updated <br /> 
(2) A new tracking ID indicates detected person to be a stranger. His or her information and features will be added to the database. <br />

### insert_records()
When stranger detected, file new tracking ID, corresponding features and timestamp into database. <br />

### update_records()
When received detection with duplicated tracking ID, the features are updated corresponding to new detection. <br />
(1) Embedded and keypoint features: new values replace old ones. <br />
(2) Consequential bounding box coordinates and confidence scores: are encoded as fix-lengthed string segments per frame. <br />
New values (floats) are converted to 8-digit length hexadecimal strings and concatenated to that of previous records. <br />
Entire sequence is stored as an extending string form. <br />
Finally add time stamp to record. <br />

### query_records()
Query stored feature information from database. <br />
(1) Embedded and keypoint features: can be directly obtained. <br />
(2) Consequential features: Stored concatenated hexadecimal strings are parsed into 8-digit length segments and reversed to original float values. <br />
