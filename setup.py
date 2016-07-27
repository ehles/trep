#!/usr/bin/env python
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

from os.path import join as pjoin
from setuptools import setup, find_packages

REQUIREMENTS = (
    'requests',
    'pytest-runner',
    'metayaml',
    'functools32',
    'Jinja2',
)

setup(name='trep',
      version='0.1',
      packages=find_packages(),
      scripts=[pjoin('bin', 'trep')],
      package_data={'': ['templates/*']},
      data_files=[
          ('configs/trep', ['configs/trep.yaml'])],
      install_requires=REQUIREMENTS
      )
