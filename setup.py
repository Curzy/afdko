import platform
from setuptools import setup, find_packages, Extension
import os
from setuptools.command.build_clib import build_clib
from setuptools.command.install_lib import install_lib
import subprocess


def getExecutableDir():
	curSystem = platform.system()
	if curSystem == "Windows":
		binDir = "win"
	elif curSystem == "Linux":
		binDir = "linux"
	elif curSystem == "Darwin":
		binDir = "osx"
	else:
		raise KeyError("Do not recognize target OS: %s" % (sys.platform))
	return binDir
	
def compile(pgkDir):
	binDir = getExecutableDir()
	programsDir = os.path.join(pgkDir, "Tools", "Programs")
	if binDir == 'osx':
		cmd = "sh BuildAll.sh"
	elif binDir == 'win':
		cmd = "BuildAll.cmd"
	elif binDir == 'linux':
		cmd = "sh BuildAllLinux.sh"
	curdir = os.getcwd()
	subprocess.check_call(cmd, cwd=programsDir, shell=True)
	os.chdir(curdir)

class CustomInstallLib(install_lib):
	"""Custom handler for the 'build_clib' command.
	Build the C programs before running the original bdist_egg.run()"""
	def run(self):
		pgkDir = self.distribution.package_dir['']
		compile(pgkDir)
		install_lib.run(self)


classifiers = {"classifiers": [
	"Development Status :: 5 - Production/Stable",
	"Environment :: Console",
	"Environment :: Other Environment",
	"Intended Audience :: Developers",
	"Intended Audience :: End Users/Desktop",
	"License :: OSI Approved :: BSD License",
	"Natural Language :: English",
	"Operating System :: OS Independent",
	"Programming Language :: Python",
	"Programming Language :: Python :: 2",
	"Programming Language :: Python :: 3",
	"Topic :: Text Processing :: Fonts",
	"Topic :: Multimedia :: Graphics",
	"Topic :: Multimedia :: Graphics :: Graphics Conversion",
]}

binDir = getExecutableDir()

setup(name="afdko",
	  version="2.6.0.dev0",
	  description="Adobe Font Development Kit for OpenType",
	  url='https://github.com/adobe-type-tools/afdko',
	  author='Read Roberts and many other Adobe engineers',
	  author_email='readrob@pacbell.net',
	  license='Apache License, Version 2.0',
	  platforms=["Any"],
	  package_dir={'': 'FDK'},
	  packages=find_packages('FDK'),
	  include_package_data = True,
	  package_data = {
		# If any package contains *.txt files, include them:
		'Tools': ["%s/*" % (binDir)],
		'Adobe\ Cmaps': ['Adobe-CNS1/*.txt'],
		'SharedData': ['CID\ charsets/*'],
	  },
	  setup_requires=['wheel'],
	  install_requires=[
		  'fonttools>=3.11.1',
		  'booleanOperations>=0.3',
		  'defcon>=0.1',
		  'ufolib>=2.0.0',
	  ],
	  entry_points={
		  'console_scripts': [
			  "compareFamilyTest = FDK.Tools.SharedData.FDKScripts.CompareFamily:main",
			  "txFDK = Tools.%s:run_cmd" % (binDir),
			  "spotFDK = Tools.%s:run_cmd" % (binDir),
		  ],
	  },
	  cmdclass={'install_lib': CustomInstallLib},
	  **classifiers
	)
