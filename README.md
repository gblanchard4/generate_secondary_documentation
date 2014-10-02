Generate Scondary Analysis Documentation
========================================

A script to make an overview look at the qiime secondary analysis from my [qiime_secondary_analysis.py](https://github.com/gblanchard4/qiime_secondary_analysis).  
  
I created this to make looking at qiime analysis data easier. It can be pretty intimidating to get a zip directory of data. This helps relieve some fear by giving a user an easier interface to navigate the analysis with an enviroment they are familiar with, your favorite web browser. 



# Expectations  
Right now the script expects a certain folder structure, I will try to generalize it more in the future.

```
RootFolder
|
└───/Secondary1
		|
		|->	mapping_file.txt
		|->	mapping_file.txt
		|->	tree_file.tre
		|->	biom.biom
		|->	table_summary.txt
		|
		└───/alpha_diversity
		|		|
		|		└───/alpha_div_collated
		|		|		|
		|		|		|-> rarefaction_plots.html
		|		|		|
		|		|		└───/average_plots	
		|		|
		|		└───/alpha_rarefaction_plots
		|
		└───/beta_diversity
		|		|
		|		└───/2d_unweighted_unifrac_plots
		|		|
		|		└───/2d_weigthted_uniifrac_plots
		|		|
		|		└───/ANOSIM_*_unweighted
		|		|
		|		└───/ANOSIM_*_weighted
		|		|
		|		└───/unweighted_unifrac_emperor_pcoa_plot
		|		|
		|		└───/weighted_unifrac_emperor_pcoa_plot
		|		
		|
		└───/taxa_summary
		|		|
		|		└───/taxa_*
		|				|
		|				└───/taxa_summary_plots
		|						|
		|						|-> area_charts.html
		|						|-> bar_charts.html
		|						|
		|						└───/charts
		|
		└───/core_microbiome
				|
				└───core_microbiome_*/
						|
						|─> core_otus_(50-100).txt
						|─> core_otus_(50-100).biom
						|─> core_otus_size.pdf

```
# Usage 
`html_doc.py -i RootFolder`

This will create a file called `overview.html` in the *RootFolder* and each *SecondaryFolder*
