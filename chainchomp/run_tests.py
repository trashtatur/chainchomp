import os
import unittest

os.environ['CHAINCHOMP_TEST'] = '1'
os.environ['CHAINCHOMP_TEST_DIR'] = os.path.join(os.getcwd(), 'test/fixtures')
loader = unittest.TestLoader()
start_dir = os.path.join(os.getcwd(), 'test')
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)

os.environ['CHAINCHOMP_TEST'] = '0'
