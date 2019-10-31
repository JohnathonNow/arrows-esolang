import unittest
import subprocess


class TestArrows(unittest.TestCase):

    def test_command(self):
        output = subprocess.check_output(['arrows', 'samples/helloworld.png'])
        self.assertEqual(output, b'HELLO WORLD\n')

    def test_io(self):
        teststr = b'my name is jeffrey\n'
        output = subprocess.check_output(['arrows', 'samples/echo.png'],
                                         input=teststr)
        self.assertEqual(output, teststr)


if __name__ == '__main__':
    unittest.main()
