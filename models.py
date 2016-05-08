import peewee as orm
import config as path


DATABASE_CONNECTION = orm.SqliteDatabase(path.DATABASE_PATH)


class BaseModel(orm.Model):
    class Meta:
        database = DATABASE_CONNECTION


class Review(BaseModel):
    title = orm.TextField(unique=True)
    text = orm.TextField()
    date = orm.DateField()
    rating = orm.IntegerField()

class Localization(BaseModel):
    name = orm.TextField(unique=True)


class Label(BaseModel):
    localization = orm.ForeignKeyField(Localization)
    name = orm.TextField()
    text = orm.TextField()