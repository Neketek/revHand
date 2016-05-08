import os
import pip
try:
    import peewee
except ImportError:
    pip.main(["install","peewee"])

DATABASE_PATH = os.getcwd()
LOCALIZATION="RU"
DEFAULT_LOCALIZATION= "EN"
START_WINDOW_SIZE = "640x480"
if os.name is "win32" or os.name is "win64":
    DATABASE_PATH+="\\revhand.db"
else:
    DATABASE_PATH += "/revhand.db"
