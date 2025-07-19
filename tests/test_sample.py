import pytest

def test_sample():
    print("This is a sample test")

def test_sample_fail():
    print("This is a sample failed test")
    assert True == False