from typing import List, Tuple
import unittest


class TestOneHotEncoder(unittest.TestCase):
    def test_list_success(self):
        actual = fit_transform(['cat', 'dog', 'bird', 'bat', 'cat', 'bird'])
        expected = ('bat', [1, 0, 0, 0])
        self.assertIn(expected, actual)

    def test_equal_args_types(self):
        list_args = fit_transform(['one', 'two', 'three', 'one', 'four', 'two'])
        str_args = fit_transform('one', 'two', 'three', 'one', 'four', 'two')
        self.assertEqual(list_args, str_args)

    def test_no_argument(self):
        fit_transform()
        self.assertRaises(TypeError)

    def test_empty_list(self):
        actual = fit_transform([])
        self.assertFalse(actual)


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows
