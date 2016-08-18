# -*- coding:utf8 -*-
from dev_c import dev_c
import time
import unittest

class TestDev_c(unittest.TestCase):
    def test_add_dev_lic(self):
        """测试增加dev lic """
        x = dev_c()
        res = x.add_dev_lic("1lijie@senlime.com")
        self.assertEqual(res["result"], 0)

if __name__ == "__main__":
    unittest.main()
