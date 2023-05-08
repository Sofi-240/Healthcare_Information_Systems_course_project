

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
    def __init__(self, SymptomsTrieRoot):
        self.root = wordNode(SymptomsTrieRoot, '')
        self.spaceBoll = False

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
        print(txt)
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

