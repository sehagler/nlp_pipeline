#!/bin/sh

servers=("development" "production")

subdirs=("production" "test")

pipeline_modes=("training_sets" \
"linguamatics_i2e_prequeries" \
"linguamatics_i2e_indexer" \
"linguamatics_i2e_push_queries" \
"linguamatics_i2e_postqueries")

project_names=("AdverseEvants" \
"BeatAML_Waves_1_And_2" \
"BeatAML_Waves_3_And_4" \
"BreastCancerPathology" \
"CCC19" \
"KDLReports" \
"NewBiomarkers" \
"OhsuNlpTemplate")
	
if false ; then
	nohup python3 -u ../NLP_Software/development/nlp_analysis.py -mode pipeline \
	-server ${servers[0]} -subdir ${subdirs[1]} -pipeline_mode ${pipeline_modes[4]} \
	-project_name ${project_names[3]} &> nlp_analysis.out
else
	nohup python3 -u ../NLP_Software/production/nlp_analysis.py -mode pipeline \
	-server ${servers[1]} -subdir ${subdirs[1]} -pipeline_mode ${pipeline_modes[1]} \
	-project_name ${project_names[3]} &> nlp_analysis.out
fi