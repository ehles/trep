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
from functools32 import lru_cache
from pprint import pformat

from trep import itrr
from .outgoing.testrail import Client as TrClient
from .outgoing.testrail.client import Run
from .settings import get_conf
from trep.incoming import source

from settings import logger


class Reporter(object):

    def __init__(self,
                 xunit_report,
                 plan_description,
                 run_description,
                 env_description,
                 test_results_link, *args, **kwargs):
        self._config = {}
        self._cache = {}
        self.xunit_report = xunit_report
        self.plan_description = plan_description
        self.run_description = run_description
        self.env_description = env_description
        self.test_results_link = test_results_link
        super(Reporter, self).__init__(*args, **kwargs)

    def config_testrail(self, base_url, username, password, milestone, project,
                        tests_suite):
        self._config['testrail'] = dict(
            base_url=base_url,
            username=username,
            password=password,
        )
        self.milestone_name = milestone
        self.project_name = project
        self.tests_suite_name = tests_suite

    @property
    def testrail_client(self):
        return TrClient(**self._config['testrail'])

    @property
    @lru_cache()
    def project(self):
        project = self.testrail_client.projects.find(name=self.project_name)
        if not project:
            logger.error("Project not found:%s" % self.project_name)
        return project

    @property
    @lru_cache()
    def milestone(self):
        milestone = self.project.milestones.find(name=self.milestone_name)
        if not milestone:
            logger.error("Milestone not found:%s" % self.milestone_name)
        return milestone

    @property
    @lru_cache()
    def os_config(self):
        return self.project.configs.find(name='Operation System')

    @property
    @lru_cache()
    def suite(self):
        suite = self.project.suites.find(name=self.tests_suite_name)
        if not suite:
            logger.error("Test suite not found:%s" % suite)
        return suite

    @property
    @lru_cache()
    def cases(self):
        return self.suite.cases()

    @property
    @lru_cache()
    def testrail_statuses(self):
        return self.testrail_client.statuses

    @staticmethod
    def get_plan_name():
        return get_conf()['testrail']['plan']

    @staticmethod
    def get_run_name():
        return get_conf()['testrail']['run']

    def get_or_create_plan(self):
        """Get exists or create new TestRail Plan"""
        plan_name = self.get_plan_name()
        plan = self.project.plans.find(name=plan_name)
        if plan is None:
            plan = self.project.plans.add(name=plan_name,
                                          description=self.plan_description,
                                          milestone_id=self.milestone.id)
            logger.debug('Created new plan "{}"'.format(plan_name))
        else:
            logger.debug('Founded plan "{}"'.format(plan_name))
        return plan

    def get_xunit_test_suite(self):
        with open(self.xunit_report) as f:
            suites = xunitparser.parse(f)
            return suites

    def add_result_to_case(self, testrail_case, xunit_case):
        itrr_result = xunit_case.get_result()
        if itrr_result == itrr.TEST_RESULT_PASS:
            status_name = 'passed'
        elif itrr_result == itrr.TEST_RESULT_FAIL:
            status_name = 'failed'
        elif itrr_result == itrr.TEST_RESULT_SKIP:
            status_name = 'skipped'
        elif itrr_result == itrr.TEST_RESULT_BLOCKED:
            status_name = 'blocked'
        else:
            return
        status_ids = [k for k, v in self.testrail_statuses.items()
                      if v == status_name]
        if len(status_ids) == 0:
            logger.warning("Can't find status {} for result {}".format(
                status_name, xunit_case.name))
            return
        status_id = status_ids[0]
        case_info = xunit_case.get_info()
        case_info['time'] = case_info['time'].seconds
        comment = pformat(case_info)
        elasped = case_info['time']
        if elasped > 0:
            elasped = "{}s".format(elasped)
        testrail_case.add_result(
            status_id=status_id,
            elapsed=elasped,
            comment=comment
        )

    def find_testrail_cases(self, xunit_suite):
        cases = self.suite.cases()
        filtered_cases = []
        for xunit_case in xunit_suite.test_cases:
            test_name = xunit_case.name
            testrail_case = cases.find(custom_test_group=test_name)
            if testrail_case is None:
                logger.warning('Testcase for {} not found'.format(test_name))
                continue
            self.add_result_to_case(testrail_case, xunit_case)
            filtered_cases.append(testrail_case)
        cases[:] = filtered_cases
        return cases

    def create_test_run(self, plan, cases):
        run = Run(name=self.get_run_name(),
                  description=self.run_description,
                  suite_id=self.suite.id,
                  milestone_id=self.milestone.id,
                  config_ids=[],
                  case_ids=[x.id for x in cases])
        plan.add_run(run)
        return run

    def print_run_url(self, test_run):
        msg = '[TestRun URL] {}/index.php?/runs/view/{}'
        logger.info(msg.format(self._config['testrail']['base_url'],
                               test_run.id))
        print(msg.format(self._config['testrail']['base_url'], test_run.id))

    def execute(self):
        xunit_suites = source.TrepSource().get_itrr()
        for xunit_suite in xunit_suites.test_results:
            cases = self.find_testrail_cases(xunit_suite)
            if len(cases) == 0:
                logger.warning('No cases matched, program will terminated')
                return
            plan = self.get_or_create_plan()
            test_run = self.create_test_run(plan, cases)
            test_run.add_results_for_cases(cases)
            self.print_run_url(test_run)
