# Read-File-Combination
Combine collapsed read files into a single DB

## Premise 
Given a set of FASTA Ribo-Seq read files that have been collapsed from FASTQ format to take the following format:

```
>seq<read_number>_x<read count>
NNNNNNNNNNNNNNNNNNNNNNNNNNNNN
```

Example:
```
>seq1_x15121
ACGTACGCAGTTTTATCCGGTAAAGCGAATGA
```

combine these read files so the sequence is stored just once and the counts are recorded per sample

