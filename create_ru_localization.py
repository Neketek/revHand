from models import Localization,Label

en = Localization()
en.name = "RU"
en.save()

labels = {
    "read":"Читать",
    "search":"Поиск",
    "delete":"Удалить",
    "delete_ask":"Вы хотите удалить",
    "add":"Добавить",
    "edit":"Редактировать",
    "rating":"Рейтинг",
    "date":"Дата",
    "more":"Больше",
    "less":"Меньше",
    "cancel":"Отмена",
    "save":"Сохранить",
    "title":"Название",
    "keyword":"Ключевые слова"
}
label = None
for key in labels:
    label = Label()
    label.name = key
    label.text = labels[key]
    label.localization = en
    label.save()