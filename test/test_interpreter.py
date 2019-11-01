import unittest
import subprocess


class TestArrows(unittest.TestCase):

    def test_command(self):
        output = subprocess.check_output(['arrows', 'samples/helloworld.png'])
        self.assertEqual(output, b'HELLO WORLD\n')

    def test_io(self):
        teststr = b'my name is jeffrey\n'
        p = subprocess.Popen(['arrows', 'samples/echo.png'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (out, err) = p.communicate(teststr)
        self.assertEqual(out, teststr)


if __name__ == '__main__':
    unittest.main()
