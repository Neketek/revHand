from models import Localization,Label

en = Localization()
en.name = "EN"
en.save()

labels = {
    "read":"Read",
    "search":"Search",
    "delete":"Delete",
    "delete_ask":"Do you want to delete",
    "add":"Add",
    "edit":"Edit",
    "rating":"Rating",
    "date":"Date",
    "more":"More",
    "less":"Less",
    "cancel":"Cancel",
    "save":"Save",
    "title":"Title",
    "keyword":"Keywords"
}
label = None
for key in labels:
    label = Label()
    label.name = key
    label.text = labels[key]
    label.localization = en
    label.save()