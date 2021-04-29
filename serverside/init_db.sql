create database theia;
use theia;
create table jsondata(
    uuid varchar(40),
    image_Location varchar(200),
    label_list text,
    detect_text text,
    sentence text,
    file_date varchar(30),
    audio_Location varchar(200)
);
