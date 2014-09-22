echo "Before running this script, make sure you have downloaded the BabelNet packages and placed them in ~/BabelNet"

mv run-babelnet.sh ~/BabelNet

cd ~/BabelNet

echo "Extracting BabelNet"

tar -jxvf babelnet_paths.tar.bz2

mv babel-core-lucene.tar.bz2 babelnet_paths

cd babelnet_paths
tar -jxvf babel-core-lucene.tar.bz2
cd ..

tar -jxvf babelnet-api-1.0.1.tar.gz

cd babelnet-api-1.0.1/config

echo "Configuring BabelNet"

mv log4j.properties log4j.properties.old
echo "log4j.rootLogger=DEBUG, file" > log4j.properties
tail -n +2 log4j.properties.old >> log4j.properties

echo "babelnet.dir=/home/tiago/BabelNet/babelnet_paths" > babelnet.var.properties

cd ..

mv ~/run-babelnet.sh .

mv create-kbpath-index.sh create-kbpath-index.sh.old

head create-kbpath-index.sh.old > create-kbpath-index.sh
echo "java -Xmx1024m -Xms512m -XX:-UseGCOverheadLimit -classpath bin:lib/*:config it.uniroma1.lcl.knowledge.KnowledgeBasePathIndexFactory $1" >> create-kbpath-index.sh

sh create-kbpath-index.sh ~/BabelNet/babelnet_paths

echo "All done!"

