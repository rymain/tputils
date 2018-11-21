import pandas as pd


class CategoryTree:

    def __init__(self):
        self.nodes = {
            -1: Category(cat_id=-1, name="Root", is_leaf=False, parent_id=None)
        }  # type: dict[int, Category]

    @staticmethod
    def load_csv(file):
        tree = CategoryTree()
        df = pd.read_csv(file)

        for index, row in df.iterrows():

            # if root
            if pd.isna(row["parent_id"]):
                row["parent_id"] = -1

            tree.nodes[row["id"]] = Category(row["id"], row["name"], row["is_leaf"], row["parent_id"])

        tree._fill_relationship()
        tree._test_leafs()

        return tree

    def get_category(self, cat_id):
        """
        :param int cat_id:
        :return Category:
        """
        return self.nodes[cat_id]

    def get_path_ids(self, cat_id):

        def iter_nodes(node):
            if node.cat_id == -1:
                return []
            return iter_nodes(node.parent) + [node.cat_id]

        return iter_nodes(self.nodes[cat_id])

    def get_path_names(self, cat_id):
        path_ids = self.get_path_ids(cat_id)
        return [self.nodes[cat_id].name for cat_id in path_ids]

    def get_cat_distance(self, cat_id1, cat_id2):
        path1 = self.get_path_ids(cat_id1)
        path2 = self.get_path_ids(cat_id2)

        path1_common = set(path1) - set(path2)
        path2_common = set(path2) - set(path1)

        return max(len(path1_common), len(path2_common))

    def iter(self, only_leafs, node=None, only_ids=False):
        """
        Iterates over all categories.
        :param bool only_leafs: Iterates only over leafs
        :param (None|Category) node: Node from which to start
        :param bool only_ids: If True return only ids, otherwise Categories
        :return:
        """
        if only_ids:
            for cat in self.iter(only_leafs, node, only_ids=False):
                yield cat.cat_id
            return

        if node is None:
            node = self.root

        if node != self.root:
            if not only_leafs or node.is_leaf:
                yield node

        for child in node.children:
            for grandchild in self.iter(only_leafs, child):
                yield grandchild

    def get_newick(self, labels, node=None):
        if node is None:
            node = self.root

        if labels == "ids":
            node_label = str(node.cat_id)
        elif labels == "names":
            node_label = "\"{}\"".format(node.name.replace("\"", "'"))

            "s".replace("\"", "'")
        else:
            raise ValueError("labels={} not valid, must be in ['ids', 'names']".format(labels))

        if len(node.children) > 0:
            newick_children = [self.get_newick(labels, child) for child in node.children]
            newick_node = "({}){}".format(", ".join(newick_children), node_label)

        else:
            newick_node = node_label

        if node == self.root:
            newick_node += ";"

        return newick_node

    def to_dict(self, node=None):
        if node is None:
            node = self.root

        d = {"name": node.name, "id": node.cat_id, }

        if len(node.children) > 0:
            d["children"] = [self.to_dict(child) for child in node.children]

        return d

    @property
    def root(self):
        return self.nodes[-1]

    def _fill_relationship(self):
        for cat_id, cat in self.nodes.items():
            if cat != self.root:  # Skip root
                cat.parent = self.nodes[cat.parent_id]
                cat.parent.children.append(cat)

    def _test_leafs(self):
        for cat_id, cat in self.nodes.items():
            if cat.is_leaf:
                assert len(cat.children) == 0, "cat_id={} , len(children)={}".format(cat_id, len(cat.children))
            else:
                assert len(cat.children) > 0, "cat_id={} , len(children)={}".format(cat_id, len(cat.children))


class Category:
    def __init__(self, cat_id, name, is_leaf, parent_id):
        self.parent_id = parent_id
        self.parent = None
        self.name = name
        self.cat_id = cat_id
        self.children = []

        # Not necessary, but it is in csv so I want to check it
        self.is_leaf = is_leaf
