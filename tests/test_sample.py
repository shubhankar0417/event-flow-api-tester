import pytest

@pytest.mark.skip
def test_sample():
    print("This is a sample test")

@pytest.mark.skip
def test_sample_fail():
    print("This is a sample failed test")
    assert True == False
