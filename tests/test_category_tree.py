import io
import unittest

from tputils import CategoryTree


class TestCategoryTree(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        content = """
id,parent_id,is_leaf,name
17425,,0,Děti
144271,17425,0,Dětská obuv
144276,144271,1,Dětské holínky
144274,144271,1,"Dětské sandály, pantofle a žabky"
8532,,0,Dům a zahrada
8487,8532,0,Nábytek
17137,8487,1,"Nábytkové součásti, kování"
8482,8532,1,Nářadí
"""
        file = io.StringIO(content)

        self.tree = CategoryTree.load_csv(file)

    def test_get_category(self):
        cat = self.tree.get_category(17137)
        self.assertEqual(cat.name, "Nábytkové součásti, kování")
        self.assertTrue(cat.is_leaf)
        self.assertEqual(cat.parent.cat_id, 8487)
        self.assertListEqual(cat.children, [])

    def test_get_path_ids(self):
        output = self.tree.get_path_ids(17137)
        expected = [8532, 8487, 17137]
        self.assertListEqual(output, expected)

    def test_get_path_names(self):
        output = self.tree.get_path_names(17137)
        expected = [
            "Dům a zahrada",
            "Nábytek",
            "Nábytkové součásti, kování"
        ]
        self.assertListEqual(output, expected)

    def test_get_cat_distances(self):
        pairs_to_test = [
            ((8482, 8532), 1),
            ((8482, 17137), 2),
            ((8482, 8482), 0),
            ((17137, 144274), 3),
        ]

        for (cat1, cat2), expected in pairs_to_test:
            output = self.tree.get_cat_distance(cat1, cat2)
            self.assertEqual(output, expected)

            # Test if symmetric
            output = self.tree.get_cat_distance(cat2, cat1)
            self.assertEqual(output, expected)

    def test_iter(self):
        expected = {17425, 144271, 144276, 144274, 8532, 8487, 17137, 8482}
        cat_ids = {cat.cat_id for cat in self.tree.iter(only_leafs=False, only_ids=False)}
        self.assertSetEqual(cat_ids, expected)
        cat_ids = set(self.tree.iter(only_leafs=False, only_ids=True))
        self.assertSetEqual(cat_ids, expected)

        expected = {144276, 144274, 17137, 8482}
        cat_ids = {cat.cat_id for cat in self.tree.iter(only_leafs=True, only_ids=False)}
        self.assertSetEqual(cat_ids, expected)
        cat_ids = set(self.tree.iter(only_leafs=True, only_ids=True))
        self.assertSetEqual(cat_ids, expected)

    def test_get_newick(self):
        expected = "(((144276, 144274)144271)17425, ((17137)8487, 8482)8532)-1;"
        newick = self.tree.get_newick(labels="ids")
        self.assertEqual(newick, expected)


if __name__ == '__main__':
    unittest.main()
