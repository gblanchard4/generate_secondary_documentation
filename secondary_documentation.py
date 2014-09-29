#! /usr/bin/env python

import argparse
import os

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
DOC
'''


def main():

	
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Calculate stats on the input fastqs')

		
	
	# Secondary analysis directory generated with automated script
	parser.add_argument('-i','--input',dest='input', help='The secondary analysis folder to generate documentation on', required=True)
	# Output file
	parser.add_argument('-o','--output',dest='output', help='The output folder', required=True)

	# Parse arguments
	args = parser.parse_args()

	# Set arguments 
	secondary_folder = os.path.abspath(args.input)
	output_dolder =  os.path.abspath(args.output)

	# Error checking
	ERROR = False

	#Make sure the input directory exists
	if not os.path.isdir(secondary_foldern)






if __name__ == '__main__':
	main()
