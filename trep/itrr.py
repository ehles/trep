#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from datetime import timedelta


TEST_RESULT_PASS = 'pass'
TEST_RESULT_FAIL = 'fail'
TEST_RESULT_ERROR = 'error'
TEST_RESULT_SKIP = 'skip'
TEST_RESULT_BLOCKED = 'blocked'


class ITRR(object):
    # available test statuses
    testResults = {
        TEST_RESULT_PASS: 0,
        TEST_RESULT_FAIL: 1,
        TEST_RESULT_ERROR: 2,
        TEST_RESULT_SKIP: 3,
        TEST_RESULT_BLOCKED: 4,
    }

    def __init__(self):
        # Container for test results
        self.test_results = []

    def add_test_suite(self, name):
        test_suite = TestSuite(name)
        self.test_results.append(test_suite)
        return test_suite


class TestSuite(object):
    def __init__(self, name):
        self.name = name
        self.test_cases = []

    def add_test_case(self, name):
        test_case = TestCase(name)
        self.test_cases.append(test_case)
        return test_case


class TestCase(object):
    def __init__(self, name):
        self.name = name
        self.test_items = []

    def add_test_item(self, name):
        test_item = TestItem(name)
        self.test_items.append(test_item)
        return test_item

    def is_fail(self):
        item_results = {i.result for i in self.test_items}
        bad_results = {
            TEST_RESULT_FAIL,
            TEST_RESULT_ERROR,
            TEST_RESULT_SKIP,
            TEST_RESULT_BLOCKED}
        if bad_results & item_results:
            return True
        else:
            return False

    def no_items(self):
        return len(self.test_items) == 1 and self.test_items[0].name == None

    def get_result(self):
        if self.no_items():
            return self.test_items[0].result
        else:
            return {True: TEST_RESULT_FAIL,
                    False: TEST_RESULT_PASS}[self.is_fail()]

    def get_info(self):
        info = {
            'stdout': '',
            'stderr': '',
            'time': timedelta(seconds=0),
        }
        if self.no_items():
            self.test_items[0].name = self.name
        for item in self.test_items:
            info['stdout'] += '[%s] stdout:"%s";' % (item.name,
                                                  item.info['stdout'] or '')

            info['stderr'] += '[%s] stderr:"%s";' % (item.name,
                                                  item.info['stderr'] or '')

            info['time'] += item.info['time']
        return info


class TestItem(object):

    def __init__(self, name):
        self.result = None
        self.info = {
            'stdout': '',
            'stderr': '',
            'time': timedelta(seconds=0),
        }
        self.name = name

    def add_result(self, result, info={}):
        assert result in ITRR.testResults
        self.result = result
        if info:
            self.info['stdout'] = info.get('stdout', '')
            self.info['stderr'] = info.get('stderr', '')
            self.info['time'] = info.get('time', timedelta(seconds=0))


# class TestProject(object):
#     pass
#
#
# class TestPlan(object):
#     pass
#
#
# class TestRun(object):
#     pass
