#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

java -Xmx1024m -Xms512m -XX:-UseGCOverheadLimit -classpath bin:lib/*:config it.uniroma1.lcl.babelnet.BabelNet $@
