from typing import List, Tuple
import pytest


def test_list_success():
    actual = fit_transform(['cat', 'dog', 'bird', 'bat', 'cat', 'bird'])
    expected = ('bat', [1, 0, 0, 0])
    assert expected in actual


def test_equal_args_types():
    list_args = fit_transform(['one', 'two', 'three', 'one', 'four', 'two'])
    str_args = fit_transform('one', 'two', 'three', 'one', 'four', 'two')
    assert list_args == str_args


def test_no_argument():
    with pytest.raises(TypeError):
        fit_transform()


def test_empty_list():
    actual = fit_transform([])
    assert actual is not True


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
