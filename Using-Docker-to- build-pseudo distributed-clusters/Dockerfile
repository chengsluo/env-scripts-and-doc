#基于centos构建
FROM centos
MAINTAINER chengsluo
RUN yum install -y openssh-server sudo
RUN sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config
RUN yum  install -y openssh-clients

RUN echo "root:pwd" | chpasswd
RUN echo "root   ALL=(ALL)       ALL" >> /etc/sudoers

RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key

RUN mkdir /var/run/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

#安装java
ADD jdk-8u101-linux-x64.tar.gz /usr/local/
RUN mv /usr/local/jdk1.8.0_101 /usr/local/jdk1.8
#配置JAVA环境变量
ENV JAVA_HOME /usr/local/jdk1.8
ENV PATH $JAVA_HOME/bin:$PATH
#安装hadoop
ADD hadoop-2.7.3.tar.gz /usr/local
RUN mv /usr/local/hadoop-2.7.3 /usr/local/hadoop
#配置hadoop环境变量
ENV HADOOP_HOME /usr/local/hadoop
ENV PATH $HADOOP_HOME/bin:$PATH

#安装scala 注意Spark2.0.1对于Scala的版本要求是2.11.x
ADD scala-2.11.8.tgz /usr/local
RUN mv /usr/local/scala-2.11.8 /usr/local/scala2.11.8

#配置scala环境变量
ENV SCALA_HOME /usr/local/scala
ENV PATH $SCALA_HOME/bin:$PATH

#安装spark
ADD spark-2.0.1-bin-hadoop2.7.tgz /usr/local
RUN mv /usr/local/spark-2.0.1-bin-hadoop2.7 /usr/local/spark2.0.1

#配置spark环境变量
ENV SPARK_HOME /usr/local/spark2.0.1
ENV PATH $SPARK_HOME/bin:$PATH

#创建hdfs账号
RUN useradd hdfs
RUN echo "hdfs:123" | chpasswd

RUN yum install -y which sudo

#添加hadoop配置文件
ADD hadoop/etc/hadoop/core-site.xml /usr/local/hadoop/etc/hadoop/
ADD hadoop/etc/hadoop/hadoop-env.sh /usr/local/hadoop/etc/hadoop/
ADD hadoop/etc/hadoop/hdfs-site.xml /usr/local/hadoop/etc/hadoop/
ADD hadoop/etc/hadoop/mapred-site.xml /usr/local/hadoop/etc/hadoop/
ADD hadoop/etc/hadoop/yarn-site.xml /usr/local/hadoop/etc/hadoop/
ADD hadoop/etc/hadoop/slaves /usr/local/hadoop/etc/hadoop/

ADD spark2.0.1/conf/slaves /usr/local/spark2.0.1/conf/
ADD spark2.0.1/conf/spark-env.sh /usr/local/spark2.0.1/conf/
#修改文件权限
RUN chown -R hdfs:hdfs /usr/local/hadoop
RUN chown -R hdfs:hdfs /usr/local/spark2.0.1
