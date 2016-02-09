trep
----

Sample Configuration
====================
Here some special variables:
* env
* join
* ROOT

``` yaml
test_results:
  source: xunit
  jenkins: # TODO: Add Jenkins support
    url: 'http://jenkins.domain.com'
    version_artifact: 'version.yaml.txt'
  xunit:
    filename: nosetests.xml

testrail:
  url: 'https://mirantis.testrail.com'
  username: 'user@example.com'
  password: 'password'
  project: 'Test Project'
  milestone: 'Version 1.0'
  test_suite: 'Test Suite ${testrail.milestone}'
  test_plan: '${testrail.project} ${testrail.milestone}'
  test_run_description: 'Run ${testrail.test_suite}
    on ISO [#${env["ISO_ID"]}](${env["ISO_LINK"]})

    [Test results](${env["JOB_LINK"]})'
  test_section: 'All' # TODO: Add TestRail Suite section support
  test_include: null # TODO: Add Include or Exclude test cases from reporting
  test_exclude: null
  suite_configurations: # TODO: Add support of TestRail configurations
    'Operating systems':
      - 'Linux'
      - 'Windows'
      - 'Mac OS X'
    'Browser':
      - 'IE'
      - 'Firefox'
      - 'Chrome'
logging:
  log_level: INFO
  log_file: ./trep.log
  max_bytes: ${10*1024*1024} # 10MB
  backup_count: 10


# TODO: Future improvemets regarding to Lauchpad bugs
#launchpad:
#    project: 'LP Project name'
#    milestone: '2.0'
#    release_statuses:
#      released: 'Fix Released'
#      invalid: 'Invalid'

```    
