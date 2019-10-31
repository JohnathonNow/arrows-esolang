import os
import shutil
import subprocess
import tempfile
import unittest


class TestArrows(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_command(self):
        exe = os.path.join(self.dir, 'a.out')
        subprocess.check_output(['arrowsc',
                                 'samples/helloworld.png',
                                 '-o',
                                 exe])
        try:
            output = subprocess.check_output([exe])
        except subprocess.CalledProcessError as e:
            output = e.output
        finally:
            self.assertEqual(output, b'HELLO WORLD\n')


if __name__ == '__main__':
    unittest.main()
