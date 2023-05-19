class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False
        self.disID = []

    def __len__(self):
        return len(self.children)


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.maxDep = 0

    def build_trie(self, sentences):
        for disId, sent in sentences:
            self.insert_node(sent.split(), disId)

    def insert_node(self, sentence, disId):
        node = self.root
        if len(sentence) > self.maxDep:
            self.maxDep = len(sentence)
        for i, word in enumerate(sentence):
            if i == 0 and len(word) == 1:
                continue
            if word not in node.children:
                node.children[word] = TrieNode()
            node = node.children[word]
        node.end = True
        node.disID.append(disId)

    def get_disID(self, sentence):
        node = self.root
        limit = 2
        prev_node = []
        for i, word in enumerate(sentence):
            if i == 0 and len(word) == 1:
                continue
            if len(prev_node) == limit:
                prev_node.pop(0)
            if word in node.children:
                prev_node.append(node)
                node = node.children[word]
                continue
            carry = []
            self._find_forward_path(node, word, [], limit, carry)
            if carry:
                prev_node.append(node)
            else:
                self._find_backward_path(prev_node, word, [], carry)
            if carry:
                _, node = carry[0]
        return node.disID

    def _walk(self, node, sentence, sentence_list, disId=True):
        if node.children:
            for word in node.children:
                sentence_new = sentence + [word]
                if node.children[word].end:
                    if disId:
                        sentence_list.append((' '.join(sentence_new), node.children[word].disID))
                    else:
                        sentence_list.append(' '.join(sentence_new))
                self._walk(node.children[word], sentence_new, sentence_list, disId)

    def _find_forward_path(self, node, word, curr_sentence, limit, carry):
        if node.children and limit > 0:
            for prev_word, child_node in node.children.items():
                if word in child_node.children:
                    carry.append((curr_sentence + [prev_word, word], child_node.children[word]))
                    return
                self._find_forward_path(child_node, word, curr_sentence + [prev_word], limit - 1, carry)

    def _find_backward_path(self, node_list, word, curr_sentence, carry):
        if node_list:
            node = node_list.pop()
            if word in node.children:
                carry.append((curr_sentence + [word], node.children[word]))
                return
            self._find_backward_path(node_list, word, curr_sentence, carry)
