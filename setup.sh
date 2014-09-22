#!/bin/bash

echo "Cloning lingotranslator from github"

git clone https://github.com/tiagopasq/lingotranslator

echo "Do you want to install BabelNet?"
read install_babel

if [ $install_babel = 'y' ]
then
    install_babelnet
    echo "All done!"
fi
