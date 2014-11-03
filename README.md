Generate Scondary Analysis Documentation
========================================

A script to make an overview look at the qiime secondary analysis from my [qiime_secondary_analysis.py](https://github.com/gblanchard4/qiime_secondary_analysis).  
  
I created this to make looking at qiime analysis data easier. It can be pretty intimidating to get a zip directory of data. This helps relieve some fear by giving a user an easier interface to navigate the analysis with an enviroment they are familiar with, your favorite web browser. 



# Expectations  
Right now the script expects a certain folder structure, I will try to generalize it more in the future. Need to catch IOError for ANOSIM folders

```
RootFolder
|
└───/Secondary1
		|->	table_summary.txt
		|
		└───/alpha_diversity
		|		└───/alpha_div_collated
		|		|		└───/[metric]_[category]
		|		|				|─> [category]_boxplots.pdf
		|		|				|─> [category]_stats.txt
		|		└───/alpha_rarefaction_plots
		|				|─> rarefaction_plots.html
		|
		└───/beta_diversity
		|		└───/2d_unweighted_unifrac_plots/
		|		|			|─> *.html
		|		└───/2d_weigthted_uniifrac_plots/
		|		|			|─> *.html
		|		└───/unweighted_unifrac_emperor_pcoa_plot/
		|		|			|─> *.html
		|		└───/weighted_unifrac_emperor_pcoa_plot/
		|		|			|─> *.html
		|		└───/ANOSIM_*_unweighte/
		|		|			|─> anosim_results.txt
		|		└───/ANOSIM_*_weighted/
		|					|─> anosim_results.txt
		|
		└───/taxa_summary
		|		└───/taxa_[category]
		|				└───/taxa_summary_plots
		|						|─> area_charts.html
		|						|─> bar_charts.html
		|
		└───/core_microbiome
				└───core_microbiome_[category]/
						|─> core_otus_[50-100].txt
						|─> core_otus_[50-100].biom
						|─> core_otus_size.pdf

```
# Usage 
`html_doc.py -i RootFolder` 
This will create a file called `overview.html` in the *RootFolder* and each *SecondaryFolder*
## --noroot
`html_doc.py -i SecondaryFolder --noroot` 
If you pass this flag, you can input a single secondary analysis folder
