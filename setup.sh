#!/bin/bash

function install_babelnet() {
    echo "This setup assumes you already have Java installed. Do you want to continue?"
    read should_continue

    if [ $should_continue = 'n' ]
    then
        return
    fi

    mkdir ~/BabelNet
    cd ~/BabelNet

    echo "Downloading BabelNet..."

    wget http://babelnet.org/data/2.5/BabelNet-API-2.5.tar.bz2

    echo "Downloading BabelNet index bundle..."

    wget http://babelnet.org/data/2.5/babelnet-2.5-index-bundle.tar.bz2

    echo "Installing BabelNet..."

    tar -jxvf BabelNet-API-2.5.tar.bz2
    tar -jxvf babelnet-2.5-index-bundle.tar.bz2

    echo "babelnet.dir=${PWD}/BabelNet-2.5" > BabelNet-API-2.5/config/babelnet.var.properties

    git clone https://gist.github.com/76fa62c1a00d8226c9bf.git

    cp 76fa62c1a00d8226c9bf/BabelNetDemo.java BabelNet-API-2.5/src/it/uniroma1/lcl/babelnet
    rm -rfv 76fa62c1a00d8226c9bf

    cd BabelNet-API-2.5
    ant
}

echo "Cloning lingotranslator from github"

git clone https://github.com/tiagopasq/lingotranslator

echo "Do you want to install BabelNet?"
read install_babel

if [ $install_babel = 'y' ]
then
    install_babelnet
    echo "All done!"
fi
