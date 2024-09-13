import time
import pytest
from datetime import datetime, timedelta
from api.verificationConfigs.variableSubstitutions import VariableSubstitutionMap


def test_get_now():
    vsm = VariableSubstitutionMap()
    assert abs(vsm.get_now() - int(time.time())) < 2  # Allowing a small time difference


def test_get_today_date():
    vsm = VariableSubstitutionMap()
    assert vsm.get_today_date() == int(datetime.today().strftime("%Y%m%d"))


def test_get_tomorrow_date():
    vsm = VariableSubstitutionMap()
    assert vsm.get_tomorrow_date() == int(
        (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")
    )


def test_get_threshold_years_date():
    vsm = VariableSubstitutionMap()
    years = 5
    expected_date = (
        datetime.today().replace(year=datetime.today().year - years).strftime("%Y%m%d")
    )
    assert vsm.get_threshold_years_date(years) == int(expected_date)


def test_contains_static_variable():
    vsm = VariableSubstitutionMap()
    assert "$now" in vsm
    assert "$today_int" in vsm
    assert "$tomorrow_int" in vsm


def test_contains_dynamic_variable():
    vsm = VariableSubstitutionMap()
    assert "$threshold_years_5" in vsm


def test_getitem_static_variable():
    vsm = VariableSubstitutionMap()
    assert callable(vsm["$now"])
    assert callable(vsm["$today_int"])
    assert callable(vsm["$tomorrow_int"])


def test_getitem_dynamic_variable():
    vsm = VariableSubstitutionMap()
    assert callable(vsm["$threshold_years_5"])


def test_getitem_key_error():
    vsm = VariableSubstitutionMap()
    with pytest.raises(KeyError):
        vsm["$non_existent_key"]
