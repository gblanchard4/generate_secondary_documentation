#! /usr/bin/env python

import argparse
import os
import markdown

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
DOC:
Requires: python-markdown


Secondary analysis folder structure
+---root
|	+---mapping_file.txt
|	+---tree.tre
|	+---biom_table.biom
|	+---parameters.txt
|	+---logfile.log
|	+---biom_summary.txt
|	\---alpha_diversity
|		\---alpha_rarefaction_plots
|			+---rarefaction_plots.html
|			\---average_plots
|				+--(pngs containing plots)
|		\---alpha_div_collated
|			+---chao1.txt
|			\---chao1_category
|				+--category_boxplots.pdf
|				+--category_stats.txt
|			+---observed_species.txt
|			\---observed_specie_category
|				+--category_boxplots.pdf
|				+--category_stats.txt
|			+---PD_whole_tree.txt
|			\---PD_whole_tree_category
|				+--category_boxplots.pdf
|				+--category_stats.txt
|			+---shannon.txt
|			\---shannon_category
|				+--category_boxplots.pdf
|				+--category_stats.txt
|			+---simpson.txt
|			\---simpson_category
|				+--category_boxplots.pdf
|				+--category_stats.txt
|			+batchdatetime	
|		\---alpha_rarefaction_plots
|		+---log_datetime.txt


Markdown page Example:

# Root Folder Name 		>- Link to root folder
-----------------------------
* Secondary 			\-
* Secondary_category1 	 |-- Internal links
* Secondary_category2	/-

Secondary
-----------------------------
Filepath
 

'''
def make_header(analysis_folder):
	title = "# {}  \n".format(os.path.basename(analysis_folder)) 
	return title

def make_secondary_folder_list(analysis_folder):
	secondary_folder_list = []
	for secondary_folder in list_subdirectories(analysis_folder):
		filepath =  analysis_folder+'/'+secondary_folder
		folder_bullet = "* #####[{}]({}/index.html)  \n".format(secondary_folder,filepath)
		secondary_folder_list.append(folder_bullet)
	return secondary_folder_list 

def make_secondary_folder_index(analysis_folder):
	
	for secondary_folder in list_subdirectories(analysis_folder):
		string_list = ['<link href="file://{}/github-markdown.css" rel="stylesheet"></link>  \n'.format(analysis_folder)]
		#string_list = ['<link href="http://kevinburke.bitbucket.org/markdowncss/markdown.css" rel="stylesheet"></link>  \n']
		name = secondary_folder
		filepath = analysis_folder+'/'+name
	
		# Lists to hold the strings for each section, so we don't have duplicates
		alpha_list = []
		beta_list = []
		taxa_list = []

		if os.path.isdir(filepath):
			string_list.append("## {0}  \n---  \n#### [Click To Open Analysis Folder In Browser]({1})  \n".format(name, filepath))

			# Stats table
			string_list.append(biom_summary_to_table(filepath))

			# Need seperate string buffers for each 'section'

			# Alpha diversity
			alpha_list.append("#### Alpha Diversity\n")
			alpha_graphic = [png for png in os.listdir("{}/alpha_diversity/alpha_rarefaction_plots/average_plots/".format(filepath)) if png.startswith('observed_species')][0]
			alpha_graphic_path = "{}/alpha_diversity/alpha_rarefaction_plots/average_plots/{}".format(filepath, alpha_graphic)
			alpha_list.append("[![Alpha Plot](file://{} 'Example Alpha Plot')](file://{}/alpha_diversity/alpha_rarefaction_plots/rarefaction_plots.html)  \n  \n".format(alpha_graphic_path, filepath))
			#alpha_list.append("* [Rarefaction Plots](file://{}/alpha_diversity/alpha_rarefaction_plots/rarefaction_plots.html)  \n".format(filepath))

			# Taxa summary
			taxa_list.append("#### Taxa Summary  \n")
			for taxa_folder in os.listdir(filepath+"/taxa_summary/"):
				taxa_list.append("##### {}  \n".format(taxa_folder))
				taxa_list.append("* [Bar Charts](file://{0}/taxa_summary/{1}/taxa_summary_plots/bar_charts.html)  \n".format(filepath,taxa_folder)) 
				taxa_list.append("* [Area Charts](file://{0}/taxa_summary/{1}/taxa_summary_plots/area_charts.html)  \n".format(filepath,taxa_folder)) 

			# Beta Diversity
			beta_list.append("#### Beta Diversity  \n")
			beta_2d_list = ["##### 2D Plots \n"]
			beta_3d_list =  ["##### 3D Plots \n"]
			for beta_folder in os.listdir(filepath+"/beta_diversity/"):
				# For the 2d plots
				if beta_folder.startswith('2d_unweighted'):
					beta_2d_list.append("* [Unweighted Unifrac](file://{0}/beta_diversity/2d_unweighted_unifrac_plots/unweighted_unifrac_pc_2D_PCoA_plots.html)  \n".format(filepath))
				if beta_folder.startswith('2d_weighted'):
					beta_2d_list.append("* [Weighted Unifrac](file://{0}/beta_diversity/2d_weighted_unifrac_plots/weighted_unifrac_pc_2D_PCoA_plots.html)  \n".format(filepath))

				# For the 3d Emperor plots
				if '_emperor_' in beta_folder:
					if beta_folder.startswith('unweighted_'):
						beta_3d_list.append("* [Unweighted Unifrac](file://{0}/beta_diversity/unweighted_unifrac_emperor_pcoa_plot/index.html)  \n".format(filepath))
					if beta_folder.startswith('weighted_'):
						beta_3d_list.append("* [Weighted Unifrac](file://{0}/beta_diversity/weighted_unifrac_emperor_pcoa_plot//index.html)  \n".format(filepath))
			# Add the 2d and 3d plots to the main list
			beta_list.extend(beta_2d_list)
			beta_list.extend(beta_3d_list)

			# Add Alpha, Taxa, and Beta to the master list
			string_list.extend(alpha_list)
			string_list.extend(taxa_list)
			string_list.extend(beta_list)

			with open(filepath+'/index.md', 'w') as index_file:
				for markdown_string in string_list:
					index_file.write(markdown_string)
	
	return list_subdirectories(analysis_folder)


def list_subdirectories(parent_dir):
	return [name for name in os.listdir(parent_dir)
		if os.path.isdir(os.path.join(parent_dir, name))]

def biom_summary_to_table(secondary_folder):
	with open(secondary_folder+'/table_summary.txt') as table_file:
		# Markdown header string 
		markdown_string = "#### [Biom Stats](file://{}/table_summary.txt)\n```  \n".format(secondary_folder)
		for line in table_file:
			# Get important information
			# Number of samples
			if line.startswith('Num samples:'):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}			{}\n".format(value_list[0], value_list[1])
				markdown_string += line
			if line.startswith('Num observations: '):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}	{}\n".format(value_list[0], value_list[1])
				markdown_string += line
			if line.startswith('Total count: '):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}			{}\n".format(value_list[0], value_list[1])
				markdown_string += line
			if line.startswith(' Min: '):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}					{}\n".format(value_list[0].lstrip(), value_list[1])
				markdown_string += line
			if line.startswith(' Max: '):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}					{}\n".format(value_list[0].lstrip(), value_list[1])
				markdown_string += line
			if line.startswith(' Median: '):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}				{}\n".format(value_list[0].lstrip(), value_list[1])
				markdown_string += line
			if line.startswith(' Mean: '):
				#value_list = line.rstrip().split(': ')
				#markdown_string += "{}				{}\n".format(value_list[0].lstrip(), value_list[1])
				markdown_string += line
	markdown_string += "```   \n"
	return markdown_string





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

	# Write the markdown file
	with open(analysis_folder+'/index.md', 'w') as markdown_file:
		# CSS
		markdown_file.write('<link href="file://{}/github-markdown.css" rel="stylesheet"></link>  \n'.format(analysis_folder))
		# Make the title
		markdown_file.write(make_header(analysis_folder))
		# Make the instructions
		#markdown_file.write("---  \n###Click on any of the links below to jump to that analysis overview.\n---  \n")
		# Make the bullet links
		for bullet in make_secondary_folder_list(analysis_folder):
			markdown_file.write(bullet)
	# Make the children folders
	for secondary_folder in make_secondary_folder_index(analysis_folder):
			# convert to html
			markdown_file = analysis_folder+'/'+secondary_folder+'/index.md'
			html = analysis_folder+'/'+secondary_folder+'/index.html'
			with open(markdown_file, 'r') as markdown_in, open(html, 'w') as html_out:
				html_from_markdown = markdown.markdown(markdown_in.read())
				html_out.write(html_from_markdown)
	# Convert the main page
	main_markdown = analysis_folder+'/index.md'
	main_html =  analysis_folder+'/index.html'
	with open(main_markdown, 'r') as markdown_in, open(main_html, 'w') as html_out:
				html_from_markdown = markdown.markdown(markdown_in.read())
				html_out.write(html_from_markdown)










if __name__ == '__main__':
	main()
