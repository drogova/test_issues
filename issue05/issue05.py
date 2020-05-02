import urllib.request
from unittest.mock import patch
import pytest
import json
from io import StringIO

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


@pytest.fixture()
def patcher():
    return patch('urllib.request.urlopen')


def test_raise_value_error(patcher):
    with patcher as mo:
        io = StringIO('{"currentDateTime": "2020/04/25"}')
        mo.return_value.__enter__.return_value = io
        with pytest.raises(ValueError):
            what_is_year_now()


@pytest.mark.parametrize('resp,exp', [
    ('2020-04-24', 2020),
    ('24.04.2020', 2020),
])
def test_what_is_year_now(resp, exp, patcher):
    with patcher as mo:
        io = StringIO('{"currentDateTime": "%(resp)s"}' % {"resp": resp})
        mo.return_value.__enter__.return_value = io
        assert what_is_year_now() == exp


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год

    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)
    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)
