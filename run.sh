for file in ../Collapse-FASTQ/data/RiboSeqOrg/collapsed_fastq/PRJNA252511/*; do
       	echo $file; 
	python combine.py -f ${file} -d PRJNA252511_test.sqlite;
done
