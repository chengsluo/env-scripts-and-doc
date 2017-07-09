#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#需要确认已安装ping wget python3
import os
from os.path import getsize


def buildJavaPath():
    path = '# JDK PATH\n\
    export JAVA_HOME=/opt/jdk1.8.0\n\
    export JRE_HOME=/opt/jdk1.8.0/jre\n\
    export CLASSPATH=.:\$JAVA_HOME/lib:\$JRE_HOME/lib:\$CLASSPATH\n\
    export PATH=\$JAVA_HOME/bin:\$JRE_HOME/bin:\$PATH'

    #有时候需要根据情况替换下载连接,下载连接可能会失效
    # http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
    cmd = ['wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz -O jdk1.8.tar.gz',
           'tar -xzvf jdk1.8.tar.gz',
           'mv jdk1.8.0_131 jdk1.8.0',
           #此处版本号131需要修改
           'cp -r jdk1.8.0 /opt',
           'echo "' + path + '" ' + '>> /etc/profile',
           '. /etc/profile']
    net = False
    nex = False
    res = os.popen('ping www.baidu.com -c 1 -w 5').readlines()
    for item in res:
        s = str(item)
        if s.find('bytes from'):
            net = True
    if net == False:
        print ('Unable to link network !')
        return

    s = str(os.environ)
    if s.find('jdk') < 0:
        nex = True
    if nex == False:
        print ('JDK already exists !')
        return

    # if net and nex:
    #     os.system(cmd[0])

    jdk_size = getsize('jdk1.8.tar.gz')
    if jdk_size < 180000000:
        print ('Download error !')
        return

    for item in cmd[1:]:
        print ("Start CMD :"+item)
        os.system(item)


if __name__ == '__main__':
    buildJavaPath()

# 重新运行时需要删除profile里面误添加的.