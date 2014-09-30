#! /usr/bin/env python

import argparse
import os

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
DOC:


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
		folder_bullet = "* [{}](#{})  \n".format(secondary_folder,secondary_folder.lower())
		secondary_folder_list.append(folder_bullet)
	return secondary_folder_list 

def make_secondary_folder(analysis_folder):
	string_list = []
	for secondary_folder in list_subdirectories(analysis_folder):
		name = secondary_folder
		filepath = analysis_folder+'/'+name
	
		# Lists to hold the strings for each section, so we don't have duplicates
		alpha_list = []
		beta_list = []
		taxa_list = []

		if os.path.isdir(filepath):
			string_list.append("---\n## {0}  \n#### [Click To Open Analysis Folder In Browser]({1})  \n".format(name, filepath))

			# Stats table
			string_list.append(biom_summary_to_table(filepath))

			# Need seperate string buffers for each 'section'

			# Alpha diversity
			alpha_list.append("#### Alpha Diversity\n")
			alpha_graphic = os.listdir("{}/alpha_diversity/alpha_rarefaction_plots/average_plots/".format(filepath))[0]
			alpha_graphic_path = "{}/alpha_diversity/alpha_rarefaction_plots/average_plots/{}".format(filepath, alpha_graphic)
			#print alpha_graphic
			#print "![Alpha Plot](file:/{} 'Alpha plot')  \n".format(alpha_graphic_path)
			alpha_list.append("![Alpha Plot](file://{} 'Example Alpha Plot')  \n  \n".format(alpha_graphic_path))
			alpha_list.append("* [Rarefaction Plots](file://{}/alpha_diversity/alpha_rarefaction_plots/rarefaction_plots.html)  \n".format(filepath))

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
	return string_list


def list_subdirectories(parent_dir):
	return [name for name in os.listdir(parent_dir)
		if os.path.isdir(os.path.join(parent_dir, name))]

def biom_summary_to_table(secondary_folder):
	with open(secondary_folder+'/table_summary.txt') as table_file:
		# Markdown header string 
		markdown_string = "#### Biom Stats\n```  \n"
		for line in table_file:
			# Get important information
			# Number of samples
			if line.startswith('Num samples:'):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}			{}\n".format(value_list[0], value_list[1])
			if line.startswith('Num observations: '):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}	{}\n".format(value_list[0], value_list[1])
			if line.startswith('Total count: '):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}			{}\n".format(value_list[0], value_list[1])
			if line.startswith(' Min: '):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}					{}\n".format(value_list[0].lstrip(), value_list[1])
			if line.startswith(' Max: '):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}					{}\n".format(value_list[0].lstrip(), value_list[1])
			if line.startswith(' Median: '):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}				{}\n".format(value_list[0].lstrip(), value_list[1])
			if line.startswith(' Mean: '):
				value_list = line.rstrip().split(': ')
				markdown_string += "{}				{}\n".format(value_list[0].lstrip(), value_list[1])
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
	with open(analysis_folder+'/index.md', 'w') as markdown:
		markdown.write(make_header(analysis_folder))
		for bullet in make_secondary_folder_list(analysis_folder):
			markdown.write(bullet)
		for secondary_folder_string in make_secondary_folder(analysis_folder):
			markdown.write(secondary_folder_string)










if __name__ == '__main__':
	main()
