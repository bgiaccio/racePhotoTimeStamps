# Utility for adding missing timestamps to images

## Why

I often participate in race events where you can download images afterwards, but for some strange reason the downloads
come with the image tags stripped. Both timestamps and locations.

Fortunately I know the race start time and the approximate time the photo was taken on the course.

## Solution

Using [pyexiv2](https://github.com/LeoHsiao1/pyexiv2) I created a utility that takes an optional timestamp (with
timezone) and uses the file modifications times to create a time stamp.

So for example if I download race photos I only have my local computers modification time for the files

| FileName | Download/Modification Time |
|----------|----------------------------|
| 1.jpg    | 2022-09-03 12:00:00-0400   |
| 2.jpg    | 2022-09-03 12:00:01-0400   |
| 3.jpg    | 2022-09-03 12:00:10-0400   |

But the race was actually on 2022-08-21 08:00:00-0400
So I run

```shell
python3 adjustPhotos.py --relative '2022-08-21 08:00:00-0400' ~/Downloads/{1,2,3}.jpg
```

This will create an Exif.Photo.DateTimeOriginal tag for each file with a time of 08:00:00, 08:00:01, and 08:00:10 

## ToDo
Need to determine how to properly pass Latitude and Longitude to set coordinates