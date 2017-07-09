## 基本描述

这是我基于Docker配置单机版hadoop集群的详细过程,希望对其他人能有所帮助.

--2017.04.20--

--chengsluo--

---

# 安装

## Docker下载安装

## DockerDao加速器配置

# 配置Hadoop流程

**(配置之前请先在对应官网上下载对应的4个包,版本要完全一样.不一样的话需要在使用中修改各个相应文件,会有点烦:)**
**(hadoop-2.7.3.tar.gz/jdk-8u101-linux-x64.tar.gz/scala-2.11.8.tgz/spark-2.0.1-bin-hadoop2.7.tgz)**

1. 根据需求修改两个slaves文件,默认为3节点(包括主节点);
    ```
    master
    slave01
    slave02
    ```
1. 利用Dockerfile生成镜像;
    ```
    docker build -t="hadoop" .
    ```
1. 根据集群节点数量,调整运行容器的名称和IP关系,以及挂载;
    ```
    docker run  -m 2GB  -v /home/chengs/Res/DockerConf:/mnt -d -P -p 50030:50030 -p 50070:50070 -p 18088:8088 -p 18090:8090 -p 18900:8900 -p 18080:8080 -p 14040:4040 -p 16066:6066 -p 17077:7077 -p 9000:9000 -p 9001:9001 -p 8030:8030 -p 8033:8033 -p 8035:8035 -p 8032:8032 --name master -h master --add-host slave01:172.17.0.3 --add-host slave02:172.17.0.4 hadoop
    docker run  -m 2GB -d -P --name slave01 -h slave01 --add-host master:172.17.0.2 --add-host slave02:172.17.0.4  hadoop
    docker run  -m 2GB -d -P --name slave02 -h slave02 --add-host master:172.17.0.2 --add-host slave01:172.17.0.3  hadoop
    ```
1. 进入容器
    ```
    docker exec -it master bash
    docker exec -it slave01 bash
    docker exec -it slave02 bash
    ```
1. 切换用户hdfs,生成ssh key-gen.并互传;
    ```
    su hdfs
    ssh-keygen
    #拷贝到其他节点
    ssh-copy-id -i /home/hdfs/.ssh/id_rsa -p 22 hdfs@master
    ssh-copy-id -i /home/hdfs/.ssh/id_rsa -p 22 hdfs@slave01
    ssh-copy-id -i /home/hdfs/.ssh/id_rsa -p 22 hdfs@slave02
    ```
1. 测试ssh;
    ```
    ssh slave01
    exit
    ```
1. 启动;
    ```
    hdfs namenode -format     #格式化namenode
    cd /usr/local/hadoop/sbin
    ./start-dfs.sh             #启动dfs 
    jps #测试
    ```
1. 启动Hyarn管理
    ```
    ./start-yarn.sh
    ```
1. 启动Spark
    ```
    cd /usr/local/spark2.0.1/sbin/
    ./start-all.sh
    ```

# 利用wordcount进行测试

1. 在原机器,本地目录DockerConf/File下构建输入文件或文件夹,并上传到hdfs.
    ```
    hadoop fs -mkdir /wc_input
    hadoop fs -put /mnt/File/* /wc_input/
    ```
1. 运行示例程序
    ```
    cd /usr/local/hadoop/share/hadoop/mapreduce/
    #如果已经有过测试,需先删除/wc_output文件夹 hdfs$:hadoop fs -rm -r /wc_output
    hadoop jar hadoop-mapreduce-examples-2.7.3.jar wordcount /wc_input /wc_output
    #等待时间可能较长,正常情况下可通过18088端口查看任务情况
    ```    
1. 查看目录,获取结果
    ```
    hadoop fs -ls /wc_output
    #大结果文件难以查看: hadoop fs -cat /wc_output/part-r-00000
    ```
1. 将结果存回本地挂载目录,方便查看
    ```
    hadoop fs -get /wc_output/part-r-00000 /mnt/Result/
    ```
1. **切记,关机前需要停掉hadoop.**
    ```
    cd /usr/local/hadoop/sbin
    ./stop-all.sh   
    #启动快捷方式
    ./start-all.sh
    ```
## 容器持久化

### 方法一,维护好容器:
1. 开始时:
    ```
    docker start master
    docker start slave01
    docker start slave02
    ########
    docker exec -it master bash
    su hdfs
    cd /usr/local/hadoop/sbin
    ./start-all.sh 
    ```
2. 结束时:
    ```
    cd /usr/local/hadoop/sbin
    ./stop-all.sh   
    exit
    exit
    #######
    docker stop slave01
    docker stop slave02
    docker stop master
    ```
3. 中间不要瞎搞(0_0)


# 需要了解的一些基本操作

* 拉取最新Centos基础镜像
    ```
    docker pull centos
    ```
* 查看镜像状况
    ```
    docker images
    ```
* 查看容器状况
    ```
    docker ps -a
    ```
* 再次运行退出的容器
    ```
    docker start container_name
    ```
* 关闭所有未运行的容器
    ```
    docker rm $(docker ps -a -q)
    ```
* 强制关闭所有容器
    ```
    docker rm  -f $(docker ps -a -q)
    ```
* 删除镜像
    ```
    docker rmi imname ae5c
    ```
* 容器存容器文件
    ```
    docker export slave01 > /path/slave01.tar
    ```
* 容器存镜像文件
    ```
    docker save master > /path/master.tar
    ```
* 利用镜像生成容器，最好在这里映射。
    ```
    docker run   -d -P -p 50070:50070 -p 8088:8088  --name container_name -h container_name --add-host slave01:172.17.0.3  image_name
    ```
* 登录正在运行的容器
    ```
    docker exec -it container_name /bin/bash
    ```

