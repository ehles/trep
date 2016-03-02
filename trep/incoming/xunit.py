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
from trep.vendor import xunitparser
from trep import itrr as test_result


def prepare_source(conf):
    return SourceXUnit(conf)


class SourceXUnit(object):
    fields_from_results = ['time', 'stdout', 'stderr', 'trace', 'typename']

    def __init__(self, conf):
        self.filename = conf['filename']

    def get_itrr(self):
        filename = self.filename
        return self.get_itrr_by_filename(filename)

    def get_aux_info(self, xunit_case):
        aux_info = {}
        for field in self.fields_from_results:
            if field == 'time':
                aux_info[field] = xunit_case.time
            else:
                value = getattr(xunit_case, field, None)
                if value:
                    aux_info[field] = value
        return aux_info

    @staticmethod
    def get_case_result(xunit_case):
        if xunit_case.success:
            return test_result.TEST_RESULT_PASS
        elif xunit_case.failed:
            return test_result.TEST_RESULT_FAIL
        elif xunit_case.skipped:
            return test_result.TEST_RESULT_SKIP
        elif xunit_case.errored:
            return test_result.TEST_RESULT_BLOCKED
            # return test_result.TEST_RESULT_ERROR
        else:
            return None

    def get_itrr_by_filename(self, filename):
        itrr = test_result.ITRR()
        with open(filename) as f:
            for test_suite, tr in xunitparser.parse(f):
                ts = itrr.add_test_suite(test_suite.name)
                for xunit_case in test_suite:
                    tc = ts.add_test_case(xunit_case.methodname)
                    ti = tc.add_test_item(None)
                    result = SourceXUnit.get_case_result(xunit_case)
                    aux = self.get_aux_info(xunit_case)
                    ti.add_result(result, info=aux)
        return itrr
