"""Distributed execution on AWS spot instances using Clusterk.

http://www.clusterk.com/
https://clusterk.atlassian.net/wiki/display/DOC/Public+Documentation
"""
import contextlib

from bcbio.log import logger

@contextlib.contextmanager
def create(parallel):
    """Create a queue based on the provided parallel arguments.

    TODO Startup/tear-down. Currently using default queue for testing
    """
    yield {"name": parallel["queue"]}

def runner(queue, parallel):
    """Run individual jobs on an existing queue.
    """
    def run(fn_name, items):
        logger.info("clusterk: %s" % fn_name)
        assert "wrapper" in parallel, "Clusterk requires bcbio-nextgen-vm wrapper"
        fn = getattr(__import__("{base}.clusterktasks".format(base=parallel["module"]),
                                fromlist=["clusterktasks"]),
                     parallel["wrapper"])
        wrap_parallel = {k: v for k, v in parallel.items() if k in set(["fresources"])}
        out = []
        for data in [fn(fn_name, queue, parallel.get("wrapper_args"), wrap_parallel, x) for x in items]:
            if data:
                out.extend(data)
        return out
    return run
