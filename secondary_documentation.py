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
		\---alpha_rarefaction_plots
			+---rarefaction_plots.html
			\---average_plots
				+--(pngs containing plots)
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
|			
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
	title = "# [{}]({})  \n".format(os.path.basename(analysis_folder),os.path.abspath(analysis_folder)) 
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
		if os.path.isdir(filepath):
			string_list.append("## {0}  \n#### [Filepath]({1})  \n".format(name, filepath))

			# Alpha diversity
			string_list.append("#### Alpha Diversity\n* [Rarefaction Plots](file://{}/alpha_diversity/alpha_rarefaction_plots/rarefaction_plots.html)  \n".format(filepath))

			# Taxa summary
			string_list.append("#### Taxa Summary  \n")
			for taxa_folder in os.listdir(filepath+"/taxa_summary/"):
				string_list.append("##### {1}  \n* [Bar Charts](file://{0}/taxa_summary/{1}/taxa_summary_plots/bar_charts.html)  \n* [Area Charts](file://{0}/taxa_summary/{1}/taxa_summary_plots/area_charts.html)  \n".format(filepath,taxa_folder)) 

			# Beta Diversity
			string_list.append("#### Beta Diversity  \n")
			for beta_folder in os.listdir(filepath+"/beta_diversity/"):
				# For the 2d plots
				if beta_folder.startswith('2d'):
					string_list.append("##### 2D Plots  \n* [Unweighted Unifrac](file://{0}/beta_diversity/2d_unweighted_unifrac_plots/unweighted_unifrac_pc_2D_PCoA_plots.html)  \n* [Weighted Unifrac](file://{0}/beta_diversity/2d_weighted_unifrac_plots/weighted_unifrac_pc_2D_PCoA_plots.html)  \n".format(filepath))
				# For the Emperor plots
				if '_emperor_' in beta_folder:
					string_list.append("##### 3D Plots  \n* [Unweighted Unifrac](file://{0}/beta_diversity/unweighted_unifrac_emperor_pcoa_plot/index.html)  \n* [Weighted Unifrac](file://{0}/beta_diversity/weighted_unifrac_emperor_pcoa_plot//index.html)  \n".format(filepath))

	return string_list


def list_subdirectories(parent_dir):
    return [name for name in os.listdir(parent_dir)
            if os.path.isdir(os.path.join(parent_dir, name))]


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
