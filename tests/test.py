import pytest

@pytest.mark.smoke
def test_no1():
   assert 1== 2, 'did not match' 

@pytest.mark.regression
def test_add():
    assert 1==1, 'Did match'
    

@pytest.mark.skip
def test_no2():
    assert 'a'=='A', 'Did not match'