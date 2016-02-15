# trep
Test Reporter


xUnit test result format
------------------------
* http://llg.cubic.org/docs/junit/
* Sample xunit test result:
    
    ```xml
        <?xml version="1.0" encoding="UTF-8"?>
        <testsuite>
        
          <!-- if your classname does not include a dot, the package defaults to "(root)" -->
          <testcase name="my testcase" classname="my package.my classname" time="29">
        
            <!-- If the test didn't pass, specify ONE of the following 3 cases -->
        
            <!-- option 1 --> <skipped />
            <!-- option 2 --> <failure message="my failure message">my stack trace</failure>
            <!-- option 3 --> <error message="my error message">my crash report</error>
        
            <system-out>system-out tag contents</system-out>
        
            <system-err>system-err tag contents</system-err>
        
          </testcase>
        </testsuite>
    ```