#!/bin/bash

BABELNET_PATHS="http://lasid.sor.ufscar.br/assets/babelnet_paths.tar.bz2"
BABELNET_API="http://lasid.sor.ufscar.br/assets/babelnet-api-1.0.1.tar.gz"
BABEL_CORE_LUCENE="http://lasid.sor.ufscar.br/assets/babel-core-lucene.tar.bz2"

function download_babelnet {
    mkdir ~/BabelNet
    cd ~/BabelNet

    echo "Downloading BabelNet api"
    wget -c $BABELNET_API

    echo "Downloading BabelNet paths"
    wget -c $BABELNET_PATHS

    echo "Downloading BabelNet Core Lucene"
    wget -c $BABEL_CORE_LUCENE
}

echo "Before running this script, make sure you have Java JDK version 7 or higher and the ant tool installed in your sytstem."
echo "Do you want to continue? [y/n]"
read -r resp

if [ $resp != 'y' ]
then
    exit 1
fi

echo "This script installs BabelNet in your system. The following files need to be downloaded:"
echo "$BABELNET_PATHS"
echo "$BABELNET_API"
echo "$BABEL_CORE_LUCENE"
echo "This script can download these files or you can download them manually and place them under ~/BabelNet"
echo "Do you want to download these files now? [y/n]"
read -r resp

if [ $resp == 'y' ]
then
    download_babelnet
else
    echo "From this point, this script assumes you have downloaded the files mentioned before and placed them under ~/BabelNet"
    echo "Do you want to continue? [y/n]"
    read -r inner_resp

    if [ $inner_resp != 'y' ]
    then
        exit 1
    fi
fi

mv run-babelnet.sh ~/BabelNet

cd ~/BabelNet

git clone https://gist.github.com/4483a973282528da1d81.git

mv 4483a973282528da1d81/*.java .
rm -rfv 4483a973282528da1d81

echo "Extracting BabelNet"

tar -jxvf babelnet_paths.tar.bz2

mv babel-core-lucene.tar.bz2 babelnet_paths

cd babelnet_paths
tar -jxvf babel-core-lucene.tar.bz2
cd ..

tar -xzvf babelnet-api-1.0.1.tar.gz

cd babelnet-api-1.0.1/config

echo "Configuring BabelNet"

mv log4j.properties log4j.properties.old
echo "log4j.rootLogger=DEBUG, file" > log4j.properties
tail -n +2 log4j.properties.old >> log4j.properties

echo "babelnet.dir=$HOME/BabelNet/babelnet_paths" > babelnet.var.properties

cd ..

mv ~/BabelNet/run-babelnet.sh .

mv create-kbpath-index.sh create-kbpath-index.sh.old

head create-kbpath-index.sh.old > create-kbpath-index.sh
echo "java -Xmx1024m -Xms512m -XX:-UseGCOverheadLimit -classpath bin:lib/*:config it.uniroma1.lcl.knowledge.KnowledgeBasePathIndexFactory \$1" >> create-kbpath-index.sh

sh create-kbpath-index.sh ~/BabelNet/babelnet_paths

mv ~/BabelNet/*.java ~/BabelNet/babelnet-api-1.0.1/src/it/uniroma1/lcl/babelnet

ant

echo "All done!"

