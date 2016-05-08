from models import Review,Localization,Label
from tkinter import IntVar,StringVar
import peewee as orm
import config
import datetime

class RevHandController:
    localization = {}
    def __loadLocalization(self):
        local = None
        try:
            local = Localization.get(Localization.name==config.LOCALIZATION)
        except orm.DoesNotExist:
            local = Localization.get(Localization.name == config.DEFAULT_LOCALIZATION)
        labels = Label.select().where(Label.localization==local)
        for label in labels:
            self.localization[label.name]=label.text

    def filterReviews(self,config=None,**kwargs):
        if(config is not None):
            kwargs = config
        if "id" in kwargs:
            return Review.get(Review.id == kwargs["id"])

        query = Review.select()
        if "title" in kwargs:
            query = query.where(Review.title.contains(kwargs["title"]))
        if "text" in kwargs:
            for item in kwargs["text"]:
                query = query.where(Review.text.contains(item))
        if "rating" in kwargs:
            if kwargs["rating"][0] == "less":
                query = query.where(Review.rating<kwargs["rating"][1])
            else:
                query = query.where(Review.rating>kwargs["rating"][1])

        return query

    def addNewReview(self,title,text,rating):
        new = Review()
        new.title = title
        new.text = text
        new.rating = rating
        new.date = datetime.datetime.now().date()
        new.save()

    def getIdFromString(self,string=str):
        return int(string.split(" ")[0])

    def __init__(self):
        RevHandController.__loadLocalization(self)
