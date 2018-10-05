import unittest
import subprocess

class TestArrows(unittest.TestCase):

    def test_command(self):
        subprocess.call(['arrows', 'samples/helloworld.png'])
        output = subprocess.check_output(["./a.out"])
        self.assertEqual(output, 'HELLO WORLD\n')


if __name__ == '__main__':
    unittest.main()
