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

import os
import sys
import metayaml
import logging
import logging.handlers

import helpers

logger = None
conf = None


GLOBAL_STAGE_CONFIG = 'etc/trep/trep.yaml'
ENV_VARIABLES_PREFIX = 'TREP_'


def get_environment_params(conf, env2conf):
    """ Update configuration parameters with values from environment variables.
    """
    for k, v in env2conf.iteritems():
        path = v.split('.')
        container = reduce(lambda d, key: d.get(key), path[:-1], conf)
        new_value = os.environ.get('{}{}'.format(ENV_VARIABLES_PREFIX, k))
        if new_value:
            try:
                container[path[-1]] = new_value
            except TypeError:
                return False
    return True


def get_logger():
    global logger
    if not logger:
        logger = logging.getLogger(__package__)
        log_file = get_conf()['logging']['log_file']
        if log_file:
            # Add the log message handler to the logger
            max_bytes = int(get_conf()['logging']['max_bytes'])
            backup_count = int(get_conf()['logging']['backup_count'])
            ch = logging.handlers.RotatingFileHandler(log_file,
                                                      maxBytes=max_bytes,
                                                      backupCount=backup_count)
        else:
            ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - '
                                      '%(levelname)s - '
                                      '%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(get_conf()['logging']['log_level'])
    return logger


class PleaseFillRequiredParameter(Exception):
    pass


def fix_me():
    raise PleaseFillRequiredParameter("Please fill parameter")


def init_conf(local_conf=''):
    global conf
    global logger
    if not conf:
        # Read configuration
        # FIXME: search configuration under virtualenv
        if os.path.isfile(os.path.join(sys.prefix, 'local', GLOBAL_STAGE_CONFIG)):
            stage_config = GLOBAL_STAGE_CONFIG
        elif os.path.isfile(os.path.join(sys.prefix, GLOBAL_STAGE_CONFIG)):
            stage_config = os.path.join(sys.prefix, GLOBAL_STAGE_CONFIG)
        else:
            stage_config = os.environ.get("TREP_CONFIG",
                                          os.path.join(helpers.config_stage_directory(), "trep.yaml"))
        local_conf = local_conf or os.environ.get("LOCAL_CONF", None)
        configs = [stage_config]
        if local_conf:
            configs.append(local_conf)

        conf = metayaml.read(configs,
                             defaults={
                                 "__FIX_ME__": fix_me,
                                 "join": os.path.join,
                                 "ROOT": helpers.root_directory(),
                                 # "env": os.environ,
                             })
    if not logger:
        logger = get_logger()
    if not get_environment_params(conf, environment2configuration):
        sys.exit(1)
    return conf, logger


def get_conf():
    global conf
    if not conf:
        conf = init_conf()
    return conf

environment2configuration = {
    # Environment variables to configuration mapping
    'TESTRAIL_URL': 'testrail.url',
    'TESTRAIL_USER': 'testrail.username',
    'TESTRAIL_PASSWORD': 'testrail.password',
    'TESTRAIL_PROJECT': 'testrail.project',
    'TESTRAIL_MILESTONE': 'testrail.milestone',
    'TESTRAIL_TEST_SUITE': 'testrail.test_suite',
    'TESTRAIL_TEST_PLAN': 'testrail.test_plan',
    'TESTRAIL_TEST_SECTION': 'testrail.test_section',
    'TESTRAIL_TEST_INCLUDE': 'testrail.test_include',
    'TESTRAIL_TEST_EXCLUDE': 'testrail.test_exclude',

    'TEST_RESULTS_XUNIT_FILENAME': 'test_results.xunit.filename',

    'LOG_LEVEL': 'common.log_level',
    'LOG_FILE': 'common.log_file',
}
