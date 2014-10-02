#! /usr/bin/env python

import argparse
import os

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
DOC:
 

'''

# Template for the html file
def make_html(folder_name, body):
	html_string = """
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>{}</title>
		<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/gblanchard4/sublimetext-markdown-preview/master/markdown.css">
	</head>
	<body>
	<article class="markdown-body">
		{}
	</article>
	</body>
</html>
	""".format(os.path.basename(folder_name), body)
	return html_string

# Make the main landing page
def make_overview_body(analysis_folder):
	# String buffer to hold the body
	body_string = ""

	# Make the heading for the page the analysis folder name
	folder_header = "<h1>{}</h1>\n".format(os.path.basename(analysis_folder)) 
	# Add it to the string buffer
	body_string += folder_header
	# Add the secondary folders to the string buffer
	for secondary_folder in list_subdirectories(analysis_folder):
		filepath =  analysis_folder+'/'+secondary_folder
		folder_link ='\t\t<h2><a href="{}">{}</a></h2>\n'.format(filepath+'/overview.html', secondary_folder)
		body_string+=folder_link
	return body_string

# Helper function to return only the secondary folders
def list_subdirectories(parent_dir):
	return [name for name in os.listdir(parent_dir)
		if os.path.isdir(os.path.join(parent_dir, name))]

# Make the html body for the secondary folders
def make_secondary_body(secondary_folder_path):
	# String buffer to hold the body
	body_string = ""

	# The name of the secondary folder
	folder_name = os.path.basename(secondary_folder_path)
	# Make the heading for the page the analysis folder name
	body_string += '<h1>{}</h1>\n'.format(os.path.basename(folder_name)) 
	# Click here to open analysis folder in browser
	body_string += '<h5><a href="{}">(Click To Manually Browse Analysis Folder)</a></h5><hr>'.format(secondary_folder_path)
	'''
	# Key files listing (mapping, biom, tree)
	mapping_file_path = secondary_folder_path+'/'
	biom_file_path = 
	tree_file_path = 
	key_files ="""
	<h3>Base Files:</h3>
	<ul>
		<li><a href="{}">Mapping File</a></li>
		<li><a href="{}">Biom File</a></li>
		<li><a href="{}">Tree File</a></li>
	</ul>
	""".format()
	'''
	# Biom Stats
	body_string += biom_summary_to_html_table(secondary_folder_path)

	# Alpha diversity
	body_string += '<h2>Alpha Diversity</h2><h5>Click on the graph below for an interactive view</h5>\n'
	# Get an observed species plot to display
	alpha_graphic = [png for png in os.listdir("{}/alpha_diversity/alpha_rarefaction_plots/average_plots/".format(secondary_folder_path)) if png.startswith('observed_species')][0]
	alpha_graphic_path = "{}/alpha_diversity/alpha_rarefaction_plots/average_plots/{}".format(secondary_folder_path, alpha_graphic)
	body_string += '<a href="file://{}/alpha_diversity/alpha_rarefaction_plots/rarefaction_plots.html"><img src="{}"></a><hr>\n'.format(secondary_folder_path,alpha_graphic_path)

	# Beta Diversity
	body_string += '<h2>Beta Diversity</h2>\n'
	beta_2d = '<h3>2D Plots</h3><h5>More axes can be seen by clicking on the plots</h5>\n'
	beta_3d = '<h3>3D Plots</h3><h5>Follow the link for the Emperor 3D viewer</h5>\n'
	anosim = '<h3>ANOSIM Analysis</h3><h5>ANOSIM is a method that tests whether two or more groups of samples are significantly different.</h5>\n'
	anosim_unweighted = '<h4>ANOSIM Unweighted</h4>\n'
	anosim_weighted = '<h4>ANOSIM Weighted</h4>\n'
	for beta_folder in os.listdir(secondary_folder_path+"/beta_diversity/"):
		# For the 2d plots
		if beta_folder.startswith('2d_unweighted'):
			beta_png = get_beta_image_2d("{0}/beta_diversity/2d_unweighted_unifrac_plots/unweighted_unifrac_pc_2D_PCoA_plots.html".format(secondary_folder_path))
			beta_2d += '<h4>Unweighted</h4><a href="file://{0}/beta_diversity/2d_unweighted_unifrac_plots/unweighted_unifrac_pc_2D_PCoA_plots.html"><img src="file://{0}/beta_diversity/2d_unweighted_unifrac_plots/{1}"></a>\n'.format(secondary_folder_path, beta_png)
		if beta_folder.startswith('2d_weighted'):
			beta_png = get_beta_image_2d("{0}/beta_diversity/2d_weighted_unifrac_plots/weighted_unifrac_pc_2D_PCoA_plots.html".format(secondary_folder_path))
			beta_2d += '<h4>Weighted</h4><a href="file://{0}/beta_diversity/2d_weighted_unifrac_plots/weighted_unifrac_pc_2D_PCoA_plots.html"><img src="file://{0}/beta_diversity/2d_weighted_unifrac_plots/{1}"></a>\n'.format(secondary_folder_path, beta_png)
		# For the 3d Emperor plots
		if '_emperor_' in beta_folder and beta_folder.startswith('unweighted_'):
			beta_3d += '<a href="file://{0}/beta_diversity/unweighted_unifrac_emperor_pcoa_plot/index.html"><h5>Unweighted</h5></a>\n'.format(secondary_folder_path)
		if '_emperor_' in beta_folder and beta_folder.startswith('weighted_'):
			beta_3d += '<a href="file://{0}/beta_diversity/weighted_unifrac_emperor_pcoa_plot/index.html"><h5>Weighted</h5></a>\n'.format(secondary_folder_path)
		if beta_folder.startswith('ANOSIM_') and '_unweighted' in beta_folder:
			anosim_unweighted += '<a href="file://{0}/beta_diversity/{1}/anosim_results.txt"><h5>{1}</h5></a>\n'.format(secondary_folder_path, beta_folder)
		if beta_folder.startswith('ANOSIM_') and '_weighted' in beta_folder:
			anosim_weighted += '<a href="file://{0}/beta_diversity/{1}/anosim_results.txt"><h5>{1}</h5></a>\n'.format(secondary_folder_path, beta_folder)

	# Add the 2d and 3d html
	body_string += beta_2d
	body_string += beta_3d
	# Add anosim
	body_string += anosim + anosim_unweighted + anosim_weighted +"<hr>\n"
	
	# Taxa summary
	body_string += '<h2>Taxa Summary</h2><h5>Follow the links for a taxa breakdown of your samples</h4>\n'
	# Create the links and graphics for the bar and area charts
	for taxa_folder in os.listdir(secondary_folder_path+'/taxa_summary/'):
		#bar_png, area_png = get_taxa_image("{1}/taxa_summary/{0}/taxa_summary_plots/".format(taxa_folder, secondary_folder_path))
		#print bar_png
		#print area_png
		#body_string += '<h3>{0}</h3>\n<a href="file://{1}/taxa_summary/{0}/taxa_summary_plots/bar_charts.html"><img src="{2}"></a>\n<a href="file://{1}/taxa_summary/{0}/taxa_summary_plots/area_charts.html"><img src="{3}"></a>\n'.format(taxa_folder, secondary_folder_path, bar_png, area_png)
		body_string += '<h3>{0}</h3>\n<a href="file://{1}/taxa_summary/{0}/taxa_summary_plots/bar_charts.html"><h5>Bar Charts</h5></a>\n<a href="file://{1}/taxa_summary/{0}/taxa_summary_plots/area_charts.html"><h5>Area Charts</h5></a>\n'.format(taxa_folder, secondary_folder_path)
	# Section break
	body_string += '<hr>\n'	

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
		table_string = '<h2><a href="{}">Biom Table Stats</a></h2>\n<table>'.format(secondary_folder_path)
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





def main():
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Calculate stats on the input fastqs')
	# Secondary analysis directory generated with automated script
	parser.add_argument('-i','--input',dest='input', help='The secondary analysis folder to generate documentation on', required=True)
	# Parse arguments
	args = parser.parse_args()
	# Set arguments 
	analysis_folder = os.path.abspath(args.input)

	# Error checking
	ERROR = False
	#Make sure the input directory exists
	if not os.path.isdir(analysis_folder):
		print "Input directory not found"
		ERROR = True



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