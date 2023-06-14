import tkinter as tk


class RoundedButton(tk.Canvas):
    # Reference to : https://stackoverflow.com/questions/42579927/how-to-make-a-rounded-button-tkinter
    def __init__(self, master=None, text="", radius=25, btnforeground="white", btnbackground="black",
                 clicked=None, font=("Helvetica", 14, "bold"), masterBackground="white", *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=masterBackground)
        self.btnbackground = btnbackground
        self.clicked = clicked
        self.radius = radius

        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=text, tags="button", fill=btnforeground, font=font,
                                     justify="center")

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)

        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2] - text_rect[0]:
            self["width"] = (text_rect[2] - text_rect[0]) + 10

        if int(self["height"]) < text_rect[3] - text_rect[1]:
            self["height"] = (text_rect[3] - text_rect[1]) + 10

    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)

        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2] - text_bbox[0]:
            width = text_bbox[2] - text_bbox[0] + 30

        if event.height < text_bbox[3] - text_bbox[1]:
            height = text_bbox[3] - text_bbox[1] + 30

        self.round_rectangle(5, 5, width - 5, height - 5, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2] - bbox[0]) / 2) - ((text_bbox[2] - text_bbox[0]) / 2)
        y = ((bbox[3] - bbox[1]) / 2) - ((text_bbox[3] - text_bbox[1]) / 2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill="#d2d6d3")
            if self.clicked is not None:
                self.clicked()

        else:
            self.itemconfig(self.rect, fill=self.btnbackground)


class latNode:
    def __init__(self, sentence='', items=None):
        if items is None:
            items = []
        self.items = items
        self.sentence = sentence
        self.next = None


class wordNode:
    def __init__(self, TierRoot, sentence):
        self.TierRoot = TierRoot
        self.sentence = sentence
        items = []
        self._walkTier(self.TierRoot, [self.sentence], items)
        if items:
            items.sort()
        self.next = None
        self.root = latNode(sentence, items)
        self.backSpaceBool = False

    def _walkBack(self):
        if not self.root.next:
            return
        self.root = self.root.next
        return self._walkBack()

    def _walkTier(self, node, sentence, sentence_list):
        if node.children:
            for word in node.children:
                if not sentence[0]:
                    sentence_new = [word]
                else:
                    sentence_new = sentence + [word]
                if node.children[word].end:
                    sentence_list.append(' '.join(sentence_new))
                self._walkTier(node.children[word], sentence_new, sentence_list)

    def restart(self):
        return self._walkBack()

    def keyRelease(self, txt):
        if not txt:
            self._walkBack()
            return self.root.items
        if self.backSpaceBool:
            self.backSpaceBool = False
            return self.root.items

        if len(txt) == len(self.sentence):
            return self.root.items

        txt = txt.lower()
        self.sentence = txt

        def mapFunc(e):
            if len(e) < len(txt):
                return
            if e[:len(txt)] == txt:
                return True
            return False

        temp = list(filter(mapFunc, self.root.items))
        prevNode = self.root
        self.root = latNode(txt, temp)
        self.root.next = prevNode
        return self.root.items

    def backSpace(self):
        if not self.root.next:
            return False
        self.root = self.root.next
        self.sentence = self.root.sentence
        self.backSpaceBool = True
        return True


class AUTO_complete:
    def __init__(self, SymptomsTrieRoot, entry, listbox, treeview=None, select=None, deleteSelect=None,
                 initSymptoms=None):
        if initSymptoms is None:
            initSymptoms = []
        self.root = wordNode(SymptomsTrieRoot, '')
        self.entry = entry
        self.listbox = listbox
        self.treeview = treeview
        self.select = select
        if self.select:
            self.select.bind('<Button-1>', lambda e: self.updateSelectSymptoms())
        self.deleteSelect = deleteSelect
        if self.deleteSelect:
            self.deleteSelect.bind('<Button-1>', lambda e: self.deleteSelectSymptoms())
        self.tableIndex = 0
        self.entry.insert(0, 'Enter your common symptoms...')
        self.entry.bind("<space>", lambda e: self.handelKey(key='space'))
        self.entry.bind("<BackSpace>", lambda e: self.handelKey(key='BackSpace'))
        self.entry.bind("<KeyRelease>", lambda e: self.handelKey(key='KeyRelease'))
        self.entry.bind("<Button-1>", lambda e: self.entryButton1())
        self.entry.bind("<FocusOut>", lambda e: self.entryFocusOut())
        self.spaceBoll = False
        self.listbox.config(listvariable=tk.Variable(value=self.initValues()))
        self._initTable(initSymptoms)

    def _initTable(self, initSymptoms):
        if not self.treeview:
            return
        if initSymptoms:
            for row, smp in enumerate(initSymptoms):
                self.tableIndex += 1
                if row % 2:
                    self.treeview.insert(parent='', index='end', iid=int(row), text='',
                                         values=[smp], tags=('even',))
                else:
                    self.treeview.insert(parent='', index='end', iid=int(row), text='',
                                         values=[smp], tags=('odd',))
        return

    def _walkBack(self):
        if not self.root.next:
            return self.root.restart()
        self.root = self.root.next
        return self._walkBack()

    def initFrom(self, txt):
        if not txt:
            return
        self._walkBack()

        wordList = list(txt)
        prev = ''
        while wordList:
            curr = wordList.pop(0)
            if curr == ' ':
                self.space()
            prev += curr
            self.root.keyRelease(prev)
        return

    def initValues(self):
        if self.root.next:
            self._walkBack()
        return self.root.root.items

    def keyRelease(self, txt):
        if not txt:
            self._walkBack()
            return self.root.root.items
        if not self.root.sentence and txt:
            self.initFrom(txt)
        if self.spaceBoll:
            self.spaceBoll = False
            return self.root.root.items

        ret = self.root.keyRelease(txt)
        return ret

    def space(self):
        node = self.root.TierRoot
        word = list(self.root.sentence.split())
        if not word:
            return
        word = word[-1]
        if word in node.children:
            node = node.children[word]
        else:
            return
        tempNode = self.root
        self.root = wordNode(node, self.root.sentence.lower())
        self.root.next = tempNode
        self.spaceBoll = True
        return

    def backSpace(self):
        if self.root.backSpace():
            return
        if not self.root.next:
            return
        self.root = self.root.next
        return

    def entryButton1(self):
        if self.entry.get() == 'Enter your common symptoms...':
            self.entry.delete(0, "end")
        return

    def entryFocusOut(self):
        if not self.entry.get():
            self.entry.insert(0, 'Enter your common symptoms...')
        return

    def handelKey(self, key):
        if key == 'space':
            return self.space()
        if key == 'BackSpace':
            return self.backSpace()
        if key != 'KeyRelease':
            return
        sentence = self.entry.get()
        sentence_list = self.keyRelease(sentence)
        self.listbox.config(listvariable=tk.Variable(value=sentence_list))
        return

    def updateSelectSymptoms(self, symptom=''):
        if not self.treeview:
            return
        if symptom:
            txt = symptom
        else:
            selected = self.listbox.curselection()
            if not selected:
                return
            txt = self.listbox.get(selected[0])
        for each in self.treeview.get_children():
            if self.treeview.item(each)['values'][0] == txt:
                return
        if int(self.tableIndex) % 2:
            self.treeview.insert(parent='', index='end', iid=int(self.tableIndex), text='',
                                 values=[txt], tags=('even',))
        else:
            self.treeview.insert(parent='', index='end', iid=int(self.tableIndex), text='',
                                 values=[txt], tags=('odd',))
        self.tableIndex += 1
        return

    def deleteSelectSymptoms(self):
        if not self.treeview:
            return
        textList = self.treeview.item(self.treeview.focus())["values"]
        if not textList:
            return
        self.treeview.delete(self.treeview.selection()[0])
        self.tableIndex -= 1
        return
