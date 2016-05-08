from tkinter import *
from tkinter import simpledialog
from controller import RevHandController


CONTROLLER = RevHandController()
ELEMENTS_REGISTER = {}
MASTER = None
LOC = CONTROLLER.localization

def getSelectedElementString():
    revBox = ELEMENTS_REGISTER["review-box"]
    return str(revBox.get(revBox.curselection()[0]))

def refreshReviewList(query=None):
    if(query is None):
        query = CONTROLLER.filterReviews()
    revBox = ELEMENTS_REGISTER["review-box"]
    revBox.delete(0, END)
    index = 0
    for item in query:
        string = "{} {}:\"{}\" {}:[{}] {}:[{}]".format(str(item.id), LOC['title'],str(item.title),LOC['rating'],str(item.rating),LOC["date"],str(item.date))
        revBox.insert(index,string)
        index+=1


def createActionsPanel(locales,actions,master=None):
    panel = PanedWindow(master=master)
    buttonKeys = ["read","add","edit","delete","search"]
    layoutConfig = {"fill":BOTH,"expand":True}
    for key in buttonKeys:
        button = Button(master=panel,text=locales[key],command = actions[key])
        button.pack(layoutConfig)
        ELEMENTS_REGISTER["action-"+key]=button
    return panel


def createReviewListPanel(selectionVariable = None,master=None):
    panel = PanedWindow(master=master)
    revBox = Listbox(master=panel)
    scroll = Scrollbar(master=panel,orient = VERTICAL)
    revBox.pack(side=LEFT,expand=True,fill=BOTH)
    scroll.pack(side=RIGHT,expand=False,fill=Y)
    revBox.config(yscrollcommand=scroll.set)
    scroll.config(command=revBox.yview)
    revBox.insert(0,"SAFASFAF")
    ELEMENTS_REGISTER["review-box"] = revBox
    return panel


def createMainPanel(buttonLocales=None,buttonActions=None,onSelect=None,master = None):
    mainPanel = PanedWindow(master=master)
    layoutConfig = {"fill": BOTH, "expand": True}
    reviewListPanel = createReviewListPanel(None,master)
    actionsPanel = createActionsPanel(buttonLocales,buttonActions,master)
    reviewListPanel.master = mainPanel
    actionsPanel.master = mainPanel
    reviewListPanel.pack(layoutConfig)
    actionsPanel.pack(layoutConfig)
    return mainPanel


def createSearchPanel(locales=None,master = None):
    ratingCondition = StringVar(value="more")
    panel = PanedWindow(master=master)
    layoutConfig = {"fill": BOTH, "expand": True}
    fieldsKeys = ["title","keyword","rating"]
    labels = {}
    fields = {}
    for key in fieldsKeys:
        labels[key] = Label(master=panel,text=locales[key])
    fields["title"]=Entry(master=panel)
    fields["keyword"]=Entry(master=panel)
    fields["rating"]=Scale(master=panel,orient=HORIZONTAL)
    fields["search"]=Button(master=panel,text = locales["search"])
    ratingMoreLessPanel = PanedWindow(master=panel)
    moreRatingCond = Radiobutton(ratingMoreLessPanel,text=locales["more"],value = "more",variable=ratingCondition)
    lessRatingCond = Radiobutton(ratingMoreLessPanel,text=locales["less"],value = "less",variable=ratingCondition)
    ratingCondLayout = {"side":LEFT,"fill":BOTH,"expand":True}
    lessRatingCond.pack(ratingCondLayout)
    moreRatingCond.pack(ratingCondLayout)
    for key in fieldsKeys:
        labels[key].pack(layoutConfig)
        fields[key].pack(layoutConfig)
    ratingMoreLessPanel.pack(layoutConfig)
    fields["search"].pack(layoutConfig)
    def search():
        keys = str(fields["keyword"].get()).split(" ")
        title = fields["title"].get()
        rating = (ratingCondition.get(), fields["rating"].get())
        values = {}
        if(len(keys)>0):
            values["text"] = keys
        if(len(title)>0):
            values["title"] = title
        values["rating"]=rating
        query = CONTROLLER.filterReviews(values)
        refreshReviewList(query)
    fields["search"].config(command = search)
    return panel


def createSearchDialog(locales=None,actions = None,master = None):
    layoutConfig = {"fill": BOTH, "expand": True}
    top = Toplevel(master=master)
    top.wm_title(locales["search"])
    panel = createSearchPanel(locales=locales,master=top)
    panel.pack(layoutConfig)
    return top

def createReadPanel(locales=None,data=None,master=None):
    panel = PanedWindow(master=master)
    keys = ["title","rating","date"]
    textBox = Text(master=panel)
    scroll = Scrollbar(master=panel,orient=VERTICAL)
    for key in keys:
        textBox.insert(INSERT,"{}:{}\n".format(locales[key],data[key]))
    textBox.insert(INSERT,"\n\n")
    textBox.insert(INSERT,data["text"])
    textBox.config(state = DISABLED)
    textBox.pack(fill=BOTH,expand=True)
    textBox.config(yscrollcommand=scroll.set)
    scroll.config(command=textBox.yview)
    textBox.pack(fill=BOTH,expand = True,side = LEFT)
    scroll.pack(fill=BOTH,expand=False,side = RIGHT)
    return panel

def createReadWindow(locales=None,data=None,master=None):
    top = Toplevel(master=master)
    top.wm_title(locales["read"])
    panel = createReadPanel(locales,data,master=top)
    panel.pack(fill=BOTH,expand=True)
    return top

def createAddEditPanel(locales,data=None,master=None,actions=None):
    panel = PanedWindow(master=master)
    title = Entry(master=panel)
    rating = Scale(master=panel,orient=HORIZONTAL)
    titleLabel = Label(master=panel,text=locales["title"])
    ratingLabel = Label(master=panel,text=locales["rating"])
    buttonPanel = PanedWindow(master=panel)
    textPanel = PanedWindow(master=panel)
    textBox = Text(master=textPanel)
    scroll = Scrollbar(master=textPanel,orient=VERTICAL)
    textBox.config(yscrollcommand=scroll.set)
    scroll.config(command=textBox.yview)
    confirmButton = Button(master=buttonPanel)
    cancelButton = Button(master=buttonPanel)

    layoutConfig = {"fill": BOTH, "expand": True}
    cancelButton.pack(fill=BOTH, expand=True, side=LEFT)
    confirmButton.pack(fill=BOTH, expand=True, side=LEFT)
    textBox.pack(fill=BOTH, expand=True, side=LEFT)
    scroll.pack(fill=BOTH, expand=False, side=RIGHT)

    titleLabel.pack(layoutConfig)
    title.pack(layoutConfig)
    ratingLabel.pack(layoutConfig)
    rating.pack(layoutConfig)
    textPanel.pack(layoutConfig)
    buttonPanel.pack(layoutConfig)
    cancelButton.config(text=locales["cancel"])

    def add():
        CONTROLLER.addNewReview(title.get(), textBox.get("1.0",END), rating.get())
        refreshReviewList()
        panel.master.destroy()
    def save():
        review = data["model"]
        review.text = textBox.get("1.0",END)
        review.title = title.get()
        review.rating = rating.get()
        review.save()
        refreshReviewList()
        master.destroy()
    cancelButton.config(command = lambda :master.destroy())
    if data is not None:
        textBox.insert(INSERT,data["text"])
        title.insert(INSERT,data["title"])
        rating.set(data["rating"])
        confirmButton.config(text=locales["save"],command = save)
    else:
        confirmButton.config(text=locales["add"])
        confirmButton.config(command=add)

    return panel
def createDeleteDialog(locales=None,data = None,action=None):
    result = simpledialog.messagebox.askquestion(title=locales["delete"],message=("{} {}".format(locales["delete_ask"],data["item"])))
    if result=="yes":
        CONTROLLER.filterReviews(id = CONTROLLER.getIdFromString(data["item"])).delete_instance()
        refreshReviewList()

def createAddEditDialog(locales,data=None,master=None,actions=None):
    top = Toplevel(master=master)
    if data is None:
        top.wm_title(locales["add"])
    else:
        top.wm_title(locales["edit"])
    panel = createAddEditPanel(locales,data,top,actions)
    panel.pack(fill=BOTH,expand=True)
    return top

def openAddDialog(master):
    createAddEditDialog(LOC,None,master,actions=None)
    print(master)

def openDeleteDialog():
    data = {"item":getSelectedElementString()}
    createDeleteDialog(LOC,data,None)

def openEditDialog(master):
    rev = CONTROLLER.filterReviews(id=CONTROLLER.getIdFromString(getSelectedElementString()))
    data = {"text":str(rev.text),"title":str(rev.title),"id":rev.id,"date":str(rev.date),"rating":int(rev.rating),"model":rev}
    createAddEditDialog(LOC,data,master,actions=None)

def openReadDialog(master):
    rev = CONTROLLER.filterReviews(id=CONTROLLER.getIdFromString(getSelectedElementString()))
    data = {"text": str(rev.text), "title": str(rev.title), "id": rev.id, "date": str(rev.date),
            "rating": int(rev.rating), "model": rev}
    createReadWindow(LOC,data,master)

def openSearchDialog(master):
    createSearchDialog(LOC,None,master)

def createGUI(master):
    mainPanelActions = {"read":None,"add":None,"edit":None,"delete":None,"search":None}
    mainPanel = createMainPanel(LOC,mainPanelActions,None,master)
    mainPanel.pack(fill = BOTH,expand = False)

    ELEMENTS_REGISTER['action-add'].config(command=lambda:openAddDialog(master))
    ELEMENTS_REGISTER['action-delete'].config(command=lambda:openDeleteDialog())
    ELEMENTS_REGISTER['action-edit'].config(command=lambda:openEditDialog(master))
    ELEMENTS_REGISTER['action-read'].config(command=lambda:openReadDialog(master))
    ELEMENTS_REGISTER['action-search'].config(command=lambda: openSearchDialog(master))
    refreshReviewList()
