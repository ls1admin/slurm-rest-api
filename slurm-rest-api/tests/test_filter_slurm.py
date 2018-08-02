import unittest

from slurmapi.filter_slurm import filter_partitions

class TestFiltering(unittest.TestCase):

    def setUp(self):
        pass

    def test_filter_two(self):
        initdata = {"filter1": [], "filter2": [], "filter3": []}
        filter_list = ["filter1", "filter2"]
        expected = {"filter3": []}

        filter_partitions(initdata, filter_list)
        self.assertEqual(expected, initdata)

    def test_filter_none(self):
        initdata = {"filter1": [], "filter2": [], "filter3": []}
        filter_list = []
        expected = {"filter1": [], "filter2": [], "filter3": []}

        filter_partitions(initdata, filter_list)
        self.assertEqual(expected, initdata)

    def test_filter_one_center(self):
        initdata = {"filter1": [], "filter2": [], "filter3": []}
        filter_list = ["filter2"]
        expected = {"filter1": [], "filter3": []}

        filter_partitions(initdata, filter_list)
        self.assertEqual(expected, initdata)

    def test_filter_all(self):
        initdata = {"filter1": [], "filter2": [], "filter3": []}
        filter_list = ["filter1", "filter2", "filter3"]
        expected = {}

        filter_partitions(initdata, filter_list)
        self.assertEqual(expected, initdata)

    def test_filter_missing(self):
        initdata = {"filter1": [], "filter2": [], "filter3": []}
        filter_list = ["filter4"]
        expected = {"filter1": [], "filter2": [], "filter3": []}

        filter_partitions(initdata, filter_list)
        self.assertEqual(expected, initdata)

    def test_filter_one_missing(self):
        initdata = {"filter1": [], "filter2": [], "filter3": []}
        filter_list = ["filter1", "filter4"]
        expected = {"filter2": [], "filter3": []}

        filter_partitions(initdata, filter_list)
        self.assertEqual(expected, initdata)

if __name__ == "__main__":
    unittest.main()
