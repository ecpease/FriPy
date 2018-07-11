import sys
from distutils.core import setup
# from setuptools import setup
import codecs
try:
	codecs.lookup('mbcs')
except LookupError:
	ascii = codecs.lookup('ascii')
	func = lambda name, enc = ascii: {True: enc}.get(name=='mbcs')
	codecs.register(func)

DESCRIPTION = """\
Classes for pulling nwis data.
"""

# setup(name="nwis_pull",version="0.1",description="Classes for pulling nwis data into pandas dataframes",
	# author="Ross Kushnereit",packages=["nwis_pull"])


def run():
    setup(name="nwis_pull",
          version="0.1",
          description="Classes for pulling nwis data into pandas dataframes",
          author="Ross Kushnereit",
          packages=["nwis_pull"],
          author_email = 'ross.kush@gmail.com'
          )
if __name__ == "__main__":
    run()