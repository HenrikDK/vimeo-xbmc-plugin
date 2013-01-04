import sys
import unittest2, io
from mock import Mock
import MockVimeoDepends

sys.path.append('../plugin/')
sys.path.append('../xbmc-mocks/')
class BaseTestCase(unittest2.TestCase):#pragma: no cover

	def setUp(self):
		MockVimeoDepends.MockVimeoDepends().mockXBMC()
		MockVimeoDepends.MockVimeoDepends().mock()
	
	def readTestInput(self, filename, should_eval = True):
		testinput = io.open("resources/" + filename)
		inputdata = testinput.read()
		if should_eval:
			inputdata = eval(inputdata)
		return inputdata
	
	def raiseError(self, exception):
		raise exception
