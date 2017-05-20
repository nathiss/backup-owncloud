import backup
import unittest

class TestBackup(unittest.TestCase):

    def testSplitPaths(self):
        paths = [
                '/1/2/3/4',
                '/5/6/7/8'
            ]
        splited_paths = [
                ['1','2','3','4'],
                ['5','6','7','8']
            ]
        self.assertEqual(backup.splitPaths(paths), splited_paths)

    def testGetVerifyCerts(self):
        self.assertTrue(backup.getVerifyCerts('true'))
        self.assertFalse(backup.getVerifyCerts('false'))
        self.assertFalse(backup.getVerifyCerts('foo'))

if __name__ == "__main__":
    unittest.main()
