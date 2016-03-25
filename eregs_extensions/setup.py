from setuptools import setup, find_packages

ns = "eregs_ns.parser"  # The namespace for regulations-parser extensions.
fs = "fec_regparser"  # The directory name for the package.
entry_points = {
    "%s.term_definitions" % ns: [
        "fec_terms = %s.term_defs:term_defs" % fs
    ],
    "%s.preprocessors" % ns: [
        "RepeatedEmphasis = %s.preprocs:RepeatedEmphasis" % fs
    ],
    "%s.test_suite" % ns: [
        "testsuite = %s.tests" % fs
    ],
    "%s.preprocessors" % ns: [
        "RepeatedEmphasis = %s.preprocs:RepeatedEmphasis" % fs
    ],
    "%s.term_ignores" % ns: [
        "fec_ignore_terms = %s.term_defs:ignores" % fs
    ]
}

setup(
    name=fs,
    version="1.0.0",
    packages=find_packages(),
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],
    entry_points=entry_points
)
