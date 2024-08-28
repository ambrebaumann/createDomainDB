#!/bin/bash

domainFile=$1
SCOPEorCATH=$2
outputDir=$3
nbCPUs=$4

# Create output directory
mkdir -p $outputDir

# if SCOPe is selected or if CATH is selected
if [ $SCOPEorCATH == "SCOPE" ]; then
    # Run SCOPe pipeline
    python createSCOPetsv.py $domainFile $outputDir
elif [ $SCOPEorCATH == "CATH" ]; then
    # Run CATH pipeline
    python createCATHtsv.py $domainFile $outputDir
else
    echo "Invalid input. Please enter SCOPE or CATH."
    exit 1
fi

# Extract pdb ids to download from the tsv files
cut -f2 ${outputDir}/*.tsv | sort | uniq > ${outputDir}/pdb${SCOPEorCATH}_toDownload.txt

# Download pdb files
# Create pdb directory
mkdir -p ${outputDir}/pdb

# Read IDs from the text file and download in parallel
cat ${outputDir}/pdb${SCOPEorCATH}_toDownload.txt | xargs -I {} -P $nbCPUs aria2c -x 16 -s 16 -d "${outputDir}/pdb" -o "{}.pdb" "https://files.rcsb.org/download/{}.pdb" > /dev/null 2>&1

# Check if all files were downloaded
ls ${outputDir}/pdb | sed 's/.pdb//' | sort | uniq > tmp.txt
comm -23 ${outputDir}/pdb${SCOPEorCATH}_toDownload.txt tmp.txt > ${outputDir}/pdb_notDownloaded.log
rm tmp.txt

# Create domain files
# Create domain directory
mkdir -p ${outputDir}/pdb${SCOPEorCATH}_per_domain

# Process domain files
python processDomains.py ${outputDir}/*.tsv ${outputDir}/pdb ${outputDir}/pdb${SCOPEorCATH}_per_domain $outputDir $nbCPUs
