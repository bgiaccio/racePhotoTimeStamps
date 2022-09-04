import argparse
import datetime
import os

from dateutil import tz
from dateutil.parser import isoparse
from pyexiv2 import Image as ImgMeta

DTO_KEY = 'Exif.Photo.DateTimeOriginal'
LAT_KEY = 'Exif.GPSInfo.GPSLatitude'
LAT_DIR = 'Exif.GPSInfo.GPSLatitudeRef'  # N or S
LON_KEY = 'Exif.GPSInfo.GPSLongitudeRef'
LON_DIR = 'Exif.GPSInfo.GPSLongitude'  # E or W


def file_modified(f):
    return datetime.datetime.fromtimestamp(os.path.getmtime(f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--relative', type=lambda s: isoparse(s), default=datetime.datetime.now(tz=tz.tzlocal()))
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    # Google photos seems to use your local timezone on photos so setting them to UTC leaves them offset
    if not args.relative.tzinfo:
        args.relative.replace(tzinfo=tz.tzlocal())

    start = file_modified(args.files[0])
    for filename in args.files:
        with ImgMeta(filename) as img_meta:
            exif = img_meta.read_exif()
            if DTO_KEY not in exif:
                timestamp = file_modified(filename)
                delta = timestamp - start
                image_date = args.relative + delta
                print(f"{filename} -- {image_date}")
                if not args.debug:
                    img_meta.modify_exif({DTO_KEY: str(image_date)})
            else:
                print(f"{filename} -- {exif[DTO_KEY]} -- already set")
