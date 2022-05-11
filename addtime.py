import datetime
import piexif
import math
import os

def degToDmsRational(degFloat):
    minFloat = degFloat % 1 * 60
    secFloat = minFloat % 1 * 60
    deg = math.floor(degFloat)
    min = math.floor(minFloat)
    sec = round(secFloat * 100)

    deg = abs(deg) 
    min = abs(min) 
    sec = abs(sec)   
    return [(deg, 1), (min, 1), (sec, 100)]



lat = 40.425351361781395
lng = 86.91115928080822
jpgFolder = r"./"

## count number of photos found
listOfFiles = os.listdir(jpgFolder)
fileCount = len(listOfFiles)

## create datetimeString from JPG filename
for jpg in os.listdir(jpgFolder):
    if jpg.split('.')[-1] not in ['jpg', 'JPG', 'jpeg', 'JPEG']:
        continue
    filepath = jpgFolder + "\\" + jpg
    print(filepath)
## change exif datetimestamp for "Date Taken"
    exif_dict = piexif.load(filepath)
    newExifDate=datetime.datetime.strptime("2019-04-23-11-45-00", "%Y-%m-%d-%H-%M-%S").strftime("%Y:%m:%d %H:%M:%S")
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]=newExifDate
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]=newExifDate
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = degToDmsRational(lng)
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = degToDmsRational(lat)
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = "W"
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = "N"
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filepath)