import unittest
import re

from slurmapi.parse_slurm_node_list import parse_all_lists, parse_list

class TestParsing(unittest.TestCase):

    def setUp(self):
        pass

    def test_typical(self):
        s = 'slurm-0-[0-2],slurm-1-[0-6],slurm-1-[28-31],slurm-5-[1-3]'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2', 'slurm-1-0', 'slurm-1-1', 'slurm-1-2', 'slurm-1-3', 'slurm-1-4', 'slurm-1-5', 'slurm-1-6', 'slurm-1-28', 'slurm-1-29', 'slurm-1-30', 'slurm-1-31', 'slurm-5-1', 'slurm-5-2', 'slurm-5-3']"
        self.assertEqual(result,str(parse_list(s)))

    def test_multi_range(self):
        s = 'slurm-0-[0-2],slurm-1-[0-6,28-31],slurm-5-[1-3]'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2', 'slurm-1-0', 'slurm-1-1', 'slurm-1-2', 'slurm-1-3', 'slurm-1-4', 'slurm-1-5', 'slurm-1-6', 'slurm-1-28', 'slurm-1-29', 'slurm-1-30', 'slurm-1-31', 'slurm-5-1', 'slurm-5-2', 'slurm-5-3']"
        self.assertEqual(result,str(parse_list(s)))

    def test_single_3(self):
        s = 'slurm-0-[0-2]'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2']"
        self.assertEqual(result,str(parse_list(s)))

    def test_single_no_range(self):
        s = 'slurm-0-0'
        result = "['slurm-0-0']"
        self.assertEqual(result,str(parse_list(s)))

    def test_double_range(self):
        s = 'slurm-0-[0-2],slurm-1-[0-4]'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2', 'slurm-1-0', 'slurm-1-1', 'slurm-1-2', 'slurm-1-3', 'slurm-1-4']"
        self.assertEqual(result,str(parse_list(s)))

    def test_single_in_range(self):
        s = 'slurm-0-[0-2],slurm-1-[0]'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2', 'slurm-1-0']"
        self.assertEqual(result,str(parse_list(s)))

    def test_double_first_no_range(self):
        s = 'slurm-0-0,slurm-1-[0-4]'
        result = "['slurm-0-0', 'slurm-1-0', 'slurm-1-1', 'slurm-1-2', 'slurm-1-3', 'slurm-1-4']"
        self.assertEqual(result,str(parse_list(s)))

    def test_double_last_no_range(self):
        s = 'slurm-0-[0-2],slurm-1-0'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2', 'slurm-1-0']"
        self.assertEqual(result,str(parse_list(s)))

    def test_multi_range_first_no_range(self):
        s = 'slurm-0-[0-2,4-5,7],slurm-1-0'
        result = "['slurm-0-0', 'slurm-0-1', 'slurm-0-2', 'slurm-0-4', 'slurm-0-5', 'slurm-0-7', 'slurm-1-0']"
        self.assertEqual(result,str(parse_list(s)))


class TestAllListsParsing(unittest.TestCase):

    def setUp(self):
        pass

    def test_typical(self):
        arr = []
        arr.append("slurm-0-0")
        arr.append("slurm-0-1")
        result = "['slurm-0-0', 'slurm-0-1']"
        self.assertEqual(result,str(parse_all_lists(arr)))

    def test_duplicate(self):
        arr = []
        arr.append("slurm-0-0,slurm-0-1")
        arr.append("slurm-0-1")
        result = "['slurm-0-0', 'slurm-0-1']"
        self.assertEqual(result,str(parse_all_lists(arr)))

    def test_duplicate2(self):
        arr = []
        arr.append("slurm-0-0")
        arr.append("slurm-0-0,slurm-0-1")
        result = "['slurm-0-0', 'slurm-0-1']"
        self.assertEqual(result,str(parse_all_lists(arr)))

    def test_single_input(self):
        arr = []
        arr.append("slurm-0-0,slurm-0-1")
        result = "['slurm-0-0', 'slurm-0-1']"
        self.assertEqual(result,str(parse_all_lists(arr)))

    def test_only_one(self):
        arr = []
        arr.append("slurm-0-0")
        result = "['slurm-0-0']"
        self.assertEqual(result,str(parse_all_lists(arr)))


if __name__ == "__main__":
    unittest.main()
