from setuptools import setup
from setuptools.command.build_py import build_py

class MkBuild(build_py):
    def run(self):
        pass
        

setup(
    cmdclass={"build_py": MkBuild},
)
