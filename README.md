

# First BigData Assignment

## Installation
This project utilizez Vagrant.
To build the environment and run the program, simply type `make`.
However, beware that the program may take quite some time to run 
(the main reason is the number of combinations in src/clustering.pu -> cluster function).

Some resources (or dependencies), mainly package archives, are stored in resources dir.
They are installed from files, as it is faster to do so than download them.

SwissProt data was downloaded from the link: [sissprot](https://www.uniprot.org/uniprot/?query=*&fil=reviewed%3Ayes+AND+organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22+AND+proteome%3Aup000005640).

## Varia
Clustering solution is written in pyspark in `src` dir. The program does a little comparison of sparse and dense vectors,
and then computes clusters for varius sets of parameters (length of shingles, binary / count of occurance vectors).
After the program finishes it produces one artifact - report.md file, which contains the report.

This report can also be wied in realtime in log files. They are accessible at the the addres:

```
http://192.168.69.2:8088/cluster/app/<APP_ID>
```

where `<APP_ID>` can be found in console output (one have to choose worker and stdout logfile).

## Cleanup
To destroy vms run `make clean` or `vagrant destroy -f`.
To also remove the box: `make fullclean`.