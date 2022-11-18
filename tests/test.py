import pytest
from importlib.machinery import SourceFileLoader

foo = SourceFileLoader("hackedNews.py","home/fagan/hackedNews/").load_module()

''' LIST OF UNIT TESTS '''
def testing_test():
	assert True

