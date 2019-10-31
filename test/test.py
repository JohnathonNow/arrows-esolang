import unittest
import subprocess


class TestArrows(unittest.TestCase):

    def test_command(self):
        output = subprocess.check_output(['arrows', 'samples/helloworld.png'])
        self.assertEqual(output, b'HELLO WORLD\n')


if __name__ == '__main__':
    unittest.main()
