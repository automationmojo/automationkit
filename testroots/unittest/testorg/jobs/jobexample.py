
from akit.testing.testjob import TestJob

# Open Questions on Jobs
# 1. How do you deal with the interface for jobs from external work drivers, like jenkins
# 2. 


class ExampleJob(TestJob):

    # Friendly name for the test job
    name = "Example Job"

    # Description of the job
    description = "This is an example job.  This discription describes the aspects of the job."

    # The test packs or tests that are included in this TestJob
    includes = [
        "tests.internal.test_example",
        "tests.internal.tabs.test_tabs"
    ]

    # The tests that are to be excluded from this TestJob
    excludes = None
