#! /usr/bin/env python

import argparse
import os
from collections import defaultdict

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
DOC:

See README.md
'''

# Template for the html file
def make_html(folder_name, body):
	html_string = """
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>{}</title>
		<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/gblanchard4/generate_secondary_documentation/master/simplecss98.css">
	</head>
	<body>
	<article class="markdown-body">
		{}
	</article>
	</body>
</html>
	""".format(os.path.basename(folder_name), body)
	return html_string

def start_div():
	return "<div>\n"

def end_div():
	return	"</div>\n"

# Make the main landing page
def make_overview_body(analysis_folder):
	# String buffer to hold the body
	body_string = start_div()
	# Make the heading for the page the analysis folder name
	folder_header = "<header><h1>{}</h1><header>\n".format(os.path.basename(analysis_folder))
	# Add it to the string buffer
	body_string += folder_header
	# Add the secondary folders to the string buffer
	for secondary_folder in list_subdirectories(analysis_folder):
		folder_link ='\t\t<h2><a href="{}">{}</a></h2>\n'.format(secondary_folder+'/overview.html', secondary_folder)
		body_string+=folder_link
	body_string += end_div()
	return body_string

# Helper function to return only the secondary folders
def list_subdirectories(parent_dir):
	return [name for name in os.listdir(parent_dir)
		if os.path.isdir(os.path.join(parent_dir, name))]

# Make the html body for the secondary folders
def make_secondary_body(secondary_folder_path):
	# String buffer to hold the body
	body_string = start_div()
	# The name of the secondary folder
	folder_name = os.path.basename(secondary_folder_path)

	#========================================================
	# Title
	#========================================================
	# Make the heading for the page the analysis folder name
	body_string += '<h1>{}</h1>\n'.format(os.path.basename(folder_name))
	#========================================================
	# Table of contents
	#========================================================
	body_string += '''
<h3>Table of contents</h3>
<a href="#alpha"><h4>Alpha Diversity</h4></a>\n
<a href="#beta"><h4>Beta Diversity</h4></a>\n
<a href="#taxa"><h4>Taxa Summary</h4></a>\n
<a href="#otu"><h4>OTU Category Significance</h4></a>\n
<a href="#core"><h4>Core Microbiome</h4></a>\n<hr>'''

	# End Table of Contents div
	body_string += end_div()
	#========================================================
	# Biom Stats
	#========================================================
	body_string += start_div()
	body_string += biom_summary_to_html_table(secondary_folder_path)

	body_string += end_div()
	#========================================================
	# Alpha diversity
	#========================================================
	body_string += start_div()
	body_string += '<a name="alpha"><h2>Alpha Diversity</h2></a>\n'
	# Descriptor
	body_string += '<h4>Alpha Diversity describes the he diversity within a sample.</h4>\n'
	# Instructions
	body_string+= '<h5>Click on the graph below for an interactive view</h5>\n'
	# Get an observed species plot to display
	alpha_graphic = [png for png in os.listdir("{}/alpha_diversity/alpha_rarefaction_plots/average_plots/".format(secondary_folder_path)) if png.startswith('observed_species')][0]
	alpha_graphic_path = "./alpha_diversity/alpha_rarefaction_plots/average_plots/{}".format(alpha_graphic)
	body_string += '<a href="./alpha_diversity/alpha_rarefaction_plots/rarefaction_plots.html"><img src="{}"></a>\n'.format(alpha_graphic_path)
	# Alpha div collated
	body_string += alpha_div_collated_to_html_table(secondary_folder_path)
	# Seperator
	body_string += '<hr>'
	body_string += end_div()
	#========================================================
	# Beta Diversity
	#========================================================
	body_string += start_div()
	body_string += '<a name="beta"><h2>Beta Diversity</h2></a>\n'
	# Descriptor
	body_string += '<h4>Beta Diversity describes the diversity between samples.</h4>\n'
	# Instructions
	beta_2d = '<h3>2D Plots</h3><h5>More axes can be seen by clicking on the plots</h5>\n'
	# Instructions
	beta_3d = '<h3>3D Plots</h3><h5>Follow the link for the Emperor 3D viewer</h5>\n'
	anosim = '<h3>ANOSIM Analysis</h3><h5>ANOSIM is a method that tests whether two or more groups of samples are significantly different.</h5>\n'
	anosim_unweighted = '<h4>ANOSIM Unweighted</h4>\n'
	anosim_weighted = '<h4>ANOSIM Weighted</h4>\n'
	for beta_folder in os.listdir(secondary_folder_path+"/beta_diversity/"):

		# For the 2d plots
		if beta_folder.startswith('2d_unweighted'):
			beta_png = get_beta_image_2d("{0}/beta_diversity/2d_unweighted_unifrac_plots/unweighted_unifrac_pc_2D_PCoA_plots.html".format(secondary_folder_path))
			beta_2d += '<h4>Unweighted</h4><a href="./beta_diversity/2d_unweighted_unifrac_plots/unweighted_unifrac_pc_2D_PCoA_plots.html"><img src="./beta_diversity/2d_unweighted_unifrac_plots/{}"></a>\n'.format(beta_png)
		if beta_folder.startswith('2d_weighted'):
			beta_png = get_beta_image_2d("{0}/beta_diversity/2d_weighted_unifrac_plots/weighted_unifrac_pc_2D_PCoA_plots.html".format(secondary_folder_path))
			beta_2d += '<h4>Weighted</h4><a href="./beta_diversity/2d_weighted_unifrac_plots/weighted_unifrac_pc_2D_PCoA_plots.html"><img src="./beta_diversity/2d_weighted_unifrac_plots/{}"></a>\n'.format(beta_png)

		# For the 3d Emperor plots
		if '_emperor_' in beta_folder and beta_folder.startswith('unweighted_'):
			beta_3d += '<a href="./beta_diversity/unweighted_unifrac_emperor_pcoa_plot/index.html"><h5>Unweighted</h5></a>\n'
		if '_emperor_' in beta_folder and beta_folder.startswith('weighted_'):
			beta_3d += '<a href="./beta_diversity/weighted_unifrac_emperor_pcoa_plot/index.html"><h5>Weighted</h5></a>\n'
		if beta_folder.startswith('ANOSIM_') and '_unweighted' in beta_folder:
			anosim_unweighted += '<a href="./beta_diversity/{0}/anosim_results.txt"><h5>{0}</h5></a>\n'.format(beta_folder)
			anosim_unweighted += anosim_to_html_table('/{0}/beta_diversity/{1}/anosim_results.txt'.format(secondary_folder_path, beta_folder))
		if beta_folder.startswith('ANOSIM_') and '_weighted' in beta_folder:
			anosim_weighted += '<a href="./beta_diversity/{0}/anosim_results.txt"><h5>{0}</h5></a>\n'.format(beta_folder)
			anosim_weighted += anosim_to_html_table('/{0}/beta_diversity/{1}/anosim_results.txt'.format(secondary_folder_path, beta_folder))
	# Add the 2d and 3d html
	body_string += beta_2d
	body_string += beta_3d
	# Add anosim
	body_string += anosim + anosim_unweighted + anosim_weighted
	body_string += "<hr>"
	body_string += end_div()
	#========================================================
	# Taxa summary
	#========================================================
	body_string += start_div()
	body_string += '<a name="taxa"><h2>Taxa Summary</h2></a>\n'
	# Descriptor
	body_string += '<h4>Taxanomic charts that show the makeup of each sample for Phylum through Species levels.</h4>\n'
	# Instructions
	body_string += '<h5>Follow the links for a taxa breakdown of your samples</h4>\n'
	# Create the links and graphics for the bar and area charts
	for taxa_folder in os.listdir(secondary_folder_path+'/taxa_summary/'):
		#bar_png, area_png = get_taxa_image("{1}/taxa_summary/{0}/taxa_summary_plots/".format(taxa_folder, secondary_folder_path))
		#body_string += '<h3>{0}</h3>\n<a href="file://{1}/taxa_summary/{0}/taxa_summary_plots/bar_charts.html"><img src="{2}"></a>\n<a href="file://{1}/taxa_summary/{0}/taxa_summary_plots/area_charts.html"><img src="{3}"></a>\n'.format(taxa_folder, secondary_folder_path, bar_png, area_png)
		body_string += '<h3>{0}</h3><h5><p><a href="./taxa_summary/{0}/taxa_summary_plots/bar_charts.html">Bar Charts</a> | <a href="./taxa_summary/{0}/taxa_summary_plots/area_charts.html">Area Charts</a></h5></p>\n'.format(taxa_folder)
	# Section break
	body_string += '<hr>\n'
	body_string += end_div()

	# Otu category sig
	body_string += start_div()
	body_string += '<a name="otu"><h2>OTU Category Significance</h2></a>\n'
	# Descriptor
	body_string += '<h4>Tests whether any of the OTUs in an OTU table are significantly associated with a category in the category mapping file.</h4>\n'
	# Instructions
	# body_string += '<h5>These files can be very large, this is a quick overview of the first 10 lines</h4>\n'
	for taxa_folder in os.listdir(secondary_folder_path+'/taxa_summary/'):
		body_string += '<h4>{}</h4>\n'.format(taxa_folder)
		# ANOVA
		if os.path.isfile(secondary_folder_path+'/taxa_summary/'+taxa_folder+'/ANOVA.txt'):
			body_string += anova_to_html(secondary_folder_path, taxa_folder)
		# G_test
		if os.path.isfile(secondary_folder_path+'/taxa_summary/'+taxa_folder+'/g_test.txt'):
			body_string += gtest_to_html(secondary_folder_path, taxa_folder)
	# Section break
	body_string += '<hr>\n'
	body_string += end_div()
	#========================================================
	# Core microbiome
	#========================================================
	body_string += start_div()
	body_string += '<a name="core"><h2>Core microbiome</h2></a><h5>Something something core microbiome</h5>\n'
	# Create links to all the core microbiome stuffs
	for core_folder in list_subdirectories(secondary_folder_path+'/core_microbiome/'):
		# Folder name
		body_string += '<h4>{}</h4>\n<table><tr>'.format(core_folder)
		# string buffers for txt & biom files
		txt_buffer = "<tr><td>Text Files</td>\n"
		txt_list = []
		biom_buffer = "<tr><td>Biom Files</td>\n"
		biom_list = []
		# Traverse the core folder for all its children
		for child_file in os.listdir(secondary_folder_path+'/core_microbiome/'+core_folder):
			# Use level for sorting
			# Text files
			if child_file.split('.')[1] == 'txt':
				level = int(child_file.rstrip('.txt').split('_')[-1])
				txt_tuple = './core_microbiome/'+core_folder+'/'+child_file, level
				txt_list.append(txt_tuple)
			# Biom files
			if child_file.split('.')[1] == 'biom':
				level = int(child_file.rstrip('.biom').split('_')[-1])
				biom_tuple = './core_microbiome/'+core_folder+'/'+child_file, level
				biom_list.append(biom_tuple)
		# Sort the list based on the level
		txt_list = sorted(txt_list, key= lambda txt: txt[1] )
		biom_list = sorted(biom_list, key= lambda biom: biom[1] )
		# Make some html
		for txt_file in txt_list:
			filepath = txt_file[0]
			file_level = str(txt_file[1])
			filename = os.path.basename(filepath)
			txt_buffer += '<td><a href="{}">{}</a></td>'.format(filepath, file_level)
		for biom_file in biom_list:
			filepath = biom_file[0]
			file_level = biom_file[1]
			filename = os.path.basename(filepath)
			biom_buffer += '<td><a href="{}">{}</a></td>'.format(filepath, file_level)
		# Add the new html to the body (and the pdf)
		#get the span length for the graph cell
		span_length = txt_buffer.count('</td>')
		pdf_path = secondary_folder_path+'/core_microbiome/'+core_folder+'/core_otu_size.pdf'
		pdf_buffer = '<tr><td>Graph</td><td colspan="{}"><a href="{}">core_otu_size.pdf</a></td></tr>\n'.format(span_length,pdf_path)
		body_string += '<table>{}</tr>{}</tr><tr>{}</tr></table>'.format(txt_buffer, biom_buffer, pdf_buffer)
		body_string += "<hr>"
		body_string += end_div()
	return body_string

# Get an image for the bar and area charts to use, return a tuple (barchart.png, areachart.png)
def get_taxa_image(taxa_folder_path):
	# Get barchart png
	with open('{}bar_charts.html'.format(taxa_folder_path), 'r') as bar:
		file_buffer = bar.read()
		bar_png = taxa_folder_path+file_buffer.split(' border=1 ismap usemap="#pointsrect1" /><br></td>')[0].split('<tr><td class="ntitle"><img src=')[1].strip("'")
	# Get area png
	with open('{}area_charts.html'.format(taxa_folder_path), 'r') as area:
		file_buffer = area.read()
		area_png = taxa_folder_path+file_buffer.split(' border=1 ismap usemap="#pointsrect1" /><br></td>')[0].split('<tr><td class="ntitle"><img src=')[1].strip("'")
	return bar_png, area_png

# Warning: May not be reliable in the future!
def get_beta_image_2d(beta_html):
	with open(beta_html, 'r') as html:
		file_buffer = html.read()
		beta_png = file_buffer.split('.png')[0].split('<img src="./')[-1]+'.png'
	return beta_png


# Turn a biom file into an html table of useful numbers
def biom_summary_to_html_table(secondary_folder_path):
	with open(secondary_folder_path+'/table_summary.txt', 'r') as table_file:
		# Table header string
		table_string = '<h2><a href="./table_summary.txt">Biom Table Stats</a></h2>\n<table>'
		for line in table_file:
			# Get important information
			# Number of samples
			if line.startswith('Num samples:'):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
			if line.startswith('Num observations: '):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
			if line.startswith('Total count: '):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
			if line.startswith(' Min: '):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
			if line.startswith(' Max: '):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
			if line.startswith(' Median: '):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
			if line.startswith(' Mean: '):
				value_list = line.rstrip().split(': ')
				table_string += '<tr><td><b>{}</b></td><td>{}</td></tr>\n'.format(value_list[0], value_list[1])
		#Close table
		table_string += '</table><hr>\n'
	return table_string

# def anosim_to_html_table(anosim_txt):
# 	# Table header string
# 	table_string = '<table>\n'
# 	try:
# 		with open(anosim_txt) as anosim_file:
# 			for line in anosim_file:
# 				split_line = line.rstrip().split('\t')
# 				table_string += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(split_line[0],split_line[1],split_line[2],split_line[3])
# 			table_string += '</table>'
# 	except IOError:
# 		table_string += '<tr><td>File Not Found</td></tr></table>'
#
# 	return table_string

def anosim_to_html_table(anosim_txt):
	table_string = '<table>\n'
	try:
		with open(anosim_txt) as anosim_file:
			anosim_read = anosim_file.readlines()
			method = anosim_read[0].split('\t')[-1].rstrip('\n')
			r_stat = anosim_read[4].split('\t')[-1].rstrip('\n')
			p_val =  anosim_read[5].split('\t')[-1].rstrip('\n')
			perms =  anosim_read[6].split('\t')[-1].rstrip('\n')
			table_string += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(method,r_stat,p_val,perms)
			table_string += '</table>'
	except IOError:
		table_string += '<tr><td>File Not Found</td></tr></table>'
	return table_string

def alpha_div_collated_to_html_table(secondary_folder_path):
	# Path to alpha div collated
	alpha_div_collated_path = secondary_folder_path+'/alpha_diversity/alpha_div_collated/'
	secondary_basename = os.path.basename(secondary_folder_path)
	# Collection of categories in the folder
	category_dict = defaultdict(list)
	for folder in list_subdirectories(alpha_div_collated_path):
		# Split the name on the last element
		category = folder.split('_')[-1]
		# Add the folder to the dictionary with the category as the key
		category_dict[category].append(folder)
	# Make html tables for each file per category
	alpha_div_html = "<h4>Alpha Div Collated</h4>\n"
	for key in category_dict.keys():
		# Filename
		table_string = '<h5>{}</h5>\n<div style="height:20em;overflow:auto;width:auto;"><table>\n'.format(key)
		# Table Header
		table_string += '<tr><td>Metric</td><td>Group1</td><td>Group2</td><td>Group1 mean</td><td>Group1 std</td><td>Group2 mean</td><td>Group2 std</td><td>t stat</td><td>p-value</td></tr>\n'

		for metric in category_dict[key]:
			metric_name = metric.rsplit('_',1)[0]
			metric_box_plots = './alpha_diversity/alpha_div_collated/{}/{}_boxplots.pdf'.format(metric, key)
			# Open the stats file
			stats_file = '{}/alpha_diversity/alpha_div_collated/{}/{}_stats.txt'.format(secondary_folder_path, metric, key)
			with open(stats_file, 'r') as stats:
				for line in stats:
					# Header line
					if line.startswith("Group1"):
						pass
					# Data
					else:
						group1, group2, group1mean, group1std, group2mean, group2std, tstat, pvalue = line.rstrip('\n').split('\t')
						table_string += '<tr><td><a href="{}">{}</a></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(metric_box_plots, metric_name, group1, group2, group1mean, group1std, group2mean, group2std, tstat, pvalue)
		# End table
		table_string += '</table></div>'
		alpha_div_html += table_string
	return alpha_div_html

def anova_to_html(secondary_folder_path, taxa_folder):
	anova_file = '{}/taxa_summary/{}/ANOVA.txt'.format(secondary_folder_path, taxa_folder)
	with open(anova_file, 'r') as anoava:
		# File link
		anova_html = '<a href="./taxa_summary/{}/ANOVA.txt"><h5>ANOVA</h5></a>\n'.format(taxa_folder)
		# Start table
		anova_html += '<div style="height:25em;overflow:auto;"><table>'
		for index,line in enumerate(anoava):
			if index == 0:
				# Header
				anova_html += '<tr>'
				split_line= line.rstrip('\n').split('\t')
				for cell in split_line:
					# Add cell to row
					anova_html += '<td nowrap>{}</td>'.format(cell)
				# End row
				anova_html += '</tr>'
			else:
				# Start row
				anova_html += '<tr>'
				split_line= line.split('\t')
				for cell in split_line:
					# Add cell to row
					anova_html += '<td nowrap>{}</td>'.format(cell)
				# End row
				anova_html += '</tr>'
		# End table
		anova_html += '</table></div>'
	return anova_html

def gtest_to_html(secondary_folder_path, taxa_folder):
	gtest_file = '{}/taxa_summary/{}/g_test.txt'.format(secondary_folder_path, taxa_folder)
	with open(gtest_file, 'r') as gtest:
		# File link
		gtest_html = '<a href="./taxa_summary/{}/g_test.txt"><h5>G Test</h5></a>\n'.format(taxa_folder)
		# Start table
		gtest_html += '<div style="height:25em;overflow:auto;"><table>'
		for index,line in enumerate(gtest):
			if index == 0:
				# Header
				gtest_html += '<tr>'
				split_line= line.rstrip('\n').split('\t')
				for cell in split_line:
					# Add cell to row
					gtest_html += '<td nowrap>{}</td>'.format(cell)
				# End row
				gtest_html += '</tr>'
			else:
				# Start row
				gtest_html += '<tr>'
				split_line= line.split('\t')
				for cell in split_line:
					# Add cell to row
					gtest_html += '<td nowrap>{}</td>'.format(cell)
				# End row
				gtest_html += '</tr>'
		# End table
		gtest_html += '</table></div>'
		return gtest_html


def main():
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Calculate stats on the input fastqs')
	# Secondary analysis directory generated with automated script
	parser.add_argument('-i','--input',dest='input', help='The secondary analysis folder to generate documentation on', required=True)
	# No root directory flag
	parser.add_argument('--noroot',dest='noroot', action='store_true', help='Do not generate a main page, child directory passed only')

	# Parse arguments
	args = parser.parse_args()
	# Set arguments
	analysis_folder = os.path.abspath(args.input)
	noroot = args.noroot

	# Mainpage is only if noroot == False
	if noroot:
		# Write the secondary pages
		with open(analysis_folder+'/overview.html', 'w') as html_file:
				html_file.write(make_html(analysis_folder, make_secondary_body(analysis_folder)))
	else:
		# Write main overview page
		with open(analysis_folder+'/overview.html', 'w') as html_file:
			html_file.write(make_html(analysis_folder, make_overview_body(analysis_folder)))

		# Write the secondary pages
		for secondary_folder in list_subdirectories(analysis_folder):
			path = analysis_folder+'/'+secondary_folder
			with open(path+'/overview.html', 'w') as html_file:
				html_file.write(make_html(path, make_secondary_body(analysis_folder+'/'+secondary_folder)))

if __name__ == '__main__':
	main()
