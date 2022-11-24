"""Console script for sphoin."""

__author__ = "pom11"
__copyright__ = "Copyright 2022, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.1.0"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

import argparse
import sys
from sphoin.app import Slot
import os
import random
import re
from datetime import datetime as dt
import json
import os

def main():
	"""Console script for sphoin."""
	import argparse
	parser = argparse.ArgumentParser(description="Connect via apiv1 to sphoin.app slots")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-e","--example",help="view example",action="store_true")
	group.add_argument("-f","--file",help="load .json config file")
	args = parser.parse_args()

	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	if args.file:
		slot = Slot(config=args.file)
		if slot == "slot_error":
			sys.exit(1)
	elif args.example:
		Slot(config="example")
	

if __name__ == "__main__":
	sys.exit(main())
