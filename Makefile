

all: generate-key build format-hdfs start-hdfs upload-data
	echo done.

generate-key:
	bash provision/generate-key.sh

build:
	vagrant up

start-hdfs:
	vagrant ssh master -c "/vagrant/provision/start_hdfs.sh"

stop-hdfs:
	vagrant ssh master -c "/vagrant/provision/stop_hdfs.sh"

format-hdfs:
	vagrant ssh master -c "/vagrant/provision/format_hdfs.sh"

upload-data:
	vagrant ssh master -c "hadoop fs -put /vagrant/resources/swissprot.csv data.csv"

run:
	vagrant ssh master -c "spark-submit --deploy-mode cluster --driver-memory 1024m --py-files /vagrant/src/clustering.py, /vagrant/src/main.py"
	vagrant ssh master -c "hadoop fs -cat report.md" | cat >report.md

clean:
	vagrant destroy -f

fullclean: clean
	vagrant box remove "hashicorp/bionic64"
