from app.communication.query import DataQueries


class txtNode:
    def __init__(self, root, sentence, items=None):
        self.root = root
        self.sentence = sentence
        if items is None:
            items = []
        self.items = items
        if self.items:
            self.items.sort()
        self.next = None


class AUTO_complete:
    def __init__(self):
        self.prev = None
        self._init(DataQueries('his_project').SymptomsTrie.root)
        self.forwardCounter = 0
        self.backwardCounter = 0

    def _init(self, root):
        sentence_list = []
        self._walk(root, [''], sentence_list)
        self.prev = txtNode(root, [''], sentence_list)
        return

    def space(self, word):
        node = self.prev.root
        sentence_list = []
        word = list(word.lower().split())
        if not word:
            return
        word = word[-1]
        if word in node.children:
            node = node.children[word]
        else:
            return
        if node.end:
            sentence_new = self.prev.sentence + [word]
            return [' '.join(sentence_new[1:])]
        self._walk(node, self.prev.sentence + [word], sentence_list)
        temp = self.prev
        self.prev = txtNode(node, self.prev.sentence + [word], sentence_list)
        self.prev.next = temp
        self.backwardCounter = 0
        self.forwardCounter = 0
        return

    def backSpace(self):
        if self.backwardCounter == len(self.prev.sentence[-1]) and len(self.prev.sentence[-1]) != 0:
            self.prev = self.prev.next
            self.backwardCounter = 0
            return
        self.backwardCounter += 1
        return

    def keyRelease(self, sentence):
        if not sentence:
            return []

        def mapFunc(e):
            if len(e) < len(sentence):
                return
            if e[:len(sentence)] == sentence:
                return True
            return False

        temp = list(filter(mapFunc, self.prev.items))
        return temp

    def _walk(self, node, sentence, sentence_list):
        if node.children:
            for word in node.children:
                sentence_new = sentence + [word]
                if node.children[word].end:
                    sentence_list.append(' '.join(sentence_new[1:]))
                self._walk(node.children[word], sentence_new, sentence_list)
