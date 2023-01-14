# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # `Spark Components`
# MAGIC 
# MAGIC Spark applications run as independent sets of processes on a cluster, coordinated by the `SparkContext`
# MAGIC object in your main program (called the _driver program_).
# MAGIC 
# MAGIC Specifically, to run on a cluster, the SparkContext can connect to several types of _cluster managers_
# MAGIC (either Spark's own standalone cluster manager, Mesos, YARN or Kubernetes), which allocate resources across
# MAGIC applications. Once connected, Spark acquires *executors* on nodes in the cluster, which are
# MAGIC processes that run computations and store data for your application.
# MAGIC Next, it sends your application code (defined by JAR or Python files passed to SparkContext) to
# MAGIC the executors. Finally, SparkContext sends *tasks* to the executors to run.
# MAGIC 
# MAGIC  
# MAGIC 
# MAGIC There are several useful things to note about this architecture:
# MAGIC 
# MAGIC 1. Each application gets its own executor processes, which stay up for the duration of the whole
# MAGIC    application and run tasks in multiple threads. This has the benefit of isolating applications
# MAGIC    from each other, on both the scheduling side (each driver schedules its own tasks) and executor
# MAGIC    side (tasks from different applications run in different JVMs). However, it also means that
# MAGIC    data cannot be shared across different Spark applications (instances of SparkContext) without
# MAGIC    writing it to an external storage system.
# MAGIC 2. Spark is agnostic to the underlying cluster manager. As long as it can acquire executor
# MAGIC    processes, and these communicate with each other, it is relatively easy to run it even on a
# MAGIC    cluster manager that also supports other applications (e.g. Mesos/YARN/Kubernetes).
# MAGIC 3. The driver program must listen for and accept incoming connections from its executors throughout
# MAGIC    its lifetime (e.g., see [spark.driver.port in the network config
# MAGIC    section](configuration.html#networking)). As such, the driver program must be network
# MAGIC    addressable from the worker nodes.
# MAGIC 4. Because the driver schedules tasks on the cluster, it should be run close to the worker
# MAGIC    nodes, preferably on the same local area network. If you'd like to send requests to the
# MAGIC    cluster remotely, it's better to open an RPC to the driver and have it submit operations
# MAGIC    from nearby than to run a driver far away from the worker nodes.
# MAGIC 
# MAGIC # Cluster Manager Types
# MAGIC 
# MAGIC The system currently supports several cluster managers:
# MAGIC 
# MAGIC * [Standalone]  -- a simple cluster manager included with Spark that makes it
# MAGIC   easy to set up a cluster.
# MAGIC * [Apache Mesos] -- a general cluster manager that can also run Hadoop MapReduce
# MAGIC   and service applications. (Deprecated)
# MAGIC * [Hadoop YARN] -- the resource manager in Hadoop 2.
# MAGIC * [Kubernetes]  -- an open-source system for automating deployment, scaling,
# MAGIC   and management of containerized applications.
# MAGIC 
# MAGIC  
# MAGIC 
# MAGIC # Submitting Applications
# MAGIC 
# MAGIC Applications can be submitted to a cluster of any type using the `spark-submit` script.
# MAGIC The [application submission guide]  describes how to do this.
# MAGIC 
# MAGIC # Monitoring
# MAGIC 
# MAGIC Each driver program has a web UI, typically on port 4040, that displays information about running
# MAGIC tasks, executors, and storage usage. Simply go to `http://<driver-node>:4040` in a web browser to
# MAGIC access this UI. The [monitoring guide] also describes other monitoring options.
# MAGIC 
# MAGIC # Job Scheduling
# MAGIC 
# MAGIC Spark gives control over resource allocation both _across_ applications (at the level of the cluster
# MAGIC manager) and _within_ applications (if multiple computations are happening on the same SparkContext).
# MAGIC The [job scheduling overview] describes this in more detail.
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC The following table summarizes terms you'll see used to refer to cluster concepts:
# MAGIC 
# MAGIC <table class="table">
# MAGIC   <thead>
# MAGIC     <tr><th style="width: 130px;">Term</th><th>Meaning</th></tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr>
# MAGIC       <td>Application</td>
# MAGIC       <td>User program built on Spark. Consists of a <em>driver program</em> and <em>executors</em> on the cluster.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Application jar</td>
# MAGIC       <td>
# MAGIC         A jar containing the user's Spark application. In some cases users will want to create
# MAGIC         an "uber jar" containing their application along with its dependencies. The user's jar
# MAGIC         should never include Hadoop or Spark libraries, however, these will be added at runtime.
# MAGIC       </td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Driver program</td>
# MAGIC       <td>The process running the main() function of the application and creating the SparkContext</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Cluster manager</td>
# MAGIC       <td>An external service for acquiring resources on the cluster (e.g. standalone manager, Mesos, YARN, Kubernetes)</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Deploy mode</td>
# MAGIC       <td>Distinguishes where the driver process runs. In "cluster" mode, the framework launches
# MAGIC         the driver inside of the cluster. In "client" mode, the submitter launches the driver
# MAGIC         outside of the cluster.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Worker node</td>
# MAGIC       <td>Any node that can run application code in the cluster</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Executor</td>
# MAGIC       <td>A process launched for an application on a worker node, that runs tasks and keeps data in memory
# MAGIC         or disk storage across them. Each application has its own executors.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Task</td>
# MAGIC       <td>A unit of work that will be sent to one executor</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Job</td>
# MAGIC       <td>A parallel computation consisting of multiple tasks that gets spawned in response to a Spark action
# MAGIC         (e.g. <code>save</code>, <code>collect</code>); you'll see this term used in the driver's logs.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td>Stage</td>
# MAGIC       <td>Each job gets divided into smaller sets of tasks called <em>stages</em> that depend on each other
# MAGIC         (similar to the map and reduce stages in MapReduce); you'll see this term used in the driver's logs.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Apache Spark Architecture
# MAGIC *  let's see an overview of the Apache Spark architecture. As mentioned before, Apache Spark allows you to treat many machines as one machine and this is done via a master-worker type architecture where there is a driver or master node in the cluster, accompanied by worker nodes. The master sends work to the workers and either instructs them to pull to data from memory or from disk (or from another data source like S3 or Redshift).
# MAGIC 
# MAGIC * The diagram below shows an example Apache Spark cluster, basically there exists a Driver node that communicates with executor nodes. Each of these executor nodes have slots which are logically like execution cores.
# MAGIC 
# MAGIC 
# MAGIC <img src="https://github.com/raveendratal/PysparkTelugu/blob/master/images/spark_cluster.png?raw=true">
# MAGIC 
# MAGIC * The Driver sends Tasks to the empty slots on the Executors when work has to be done:
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC <img src="https://github.com/raveendratal/PysparkTelugu/blob/master/images/spark_cluster_slots.png?raw=true">
# MAGIC 
# MAGIC Note: In the case of the Community Edition there is no Worker, and the Master, not shown in the figure, executes the entire code.
# MAGIC 
# MAGIC 
# MAGIC <img src="https://github.com/raveendratal/PysparkTelugu/blob/master/images/single_node_cluster.png?raw=true" >

# COMMAND ----------

# MAGIC %md
# MAGIC ######Execution of Spark application 
# MAGIC 1. Submit the code to be executed 
# MAGIC 2. **Cluster manager allocates resources** for driver process
# MAGIC 3. **Spark session initialises spark cluster** (driver + executors) by **communicating with cluster manager** (number of executors are a configuration set by the user)
# MAGIC 4. **Cluster manager initiates executors** and send their information (location etc.) to the spark cluster
# MAGIC 5. **Driver now communicates with the workers** to perform the task. This involves **moving data around (shuffling) and executing code**. Each worker responds with the status of those task
# MAGIC 
# MAGIC <img src="https://spark.apache.org/docs/3.0.0-preview/img/cluster-overview.png" />

# COMMAND ----------

# MAGIC %md
# MAGIC The Spark application execution has the following components
# MAGIC 1. **Sparksession**: SparkSession provides the entry point for a spark application to interact with the underlying compute.
# MAGIC 2. **Spark Job**: A job corresponds to one "Action" that triggers execution on a set of dataFrame/table projection/transformation
# MAGIC 3. **Stages**: Stages are a logical grouping of different tasks that have to be performed on a dataset
# MAGIC 4. **Tasks**: Task is an atomic unit of work performed on a block of data

# COMMAND ----------

# MAGIC %md
# MAGIC ### `What is sparkContext`
# MAGIC * A SparkContext represents the connection to a Spark cluster, 
# MAGIC * and can be used to create RDDs, accumulators and broadcast variables on that cluster
# MAGIC * Note: Only one SparkContext should be active per JVM. You must stop() the active SparkContext before creating a new one. 
# MAGIC * param: config a Spark Config object describing the application configuration. 
# MAGIC * Any settings in this config overrides the default configs as well as system properties.
# MAGIC - When executing a Spark application, we must interact with the cluster using a SparkSession.
# MAGIC - Using SparkSession, you can access all of low-level and legacy contexts and configurations accordingly
# MAGIC - A SparkContext object within SparkSession represents connection with the spark cluster. This class is how you communicate with some of Spark’s lower-level APIs, such as RDDs. (SparkSession can have supports different contexts like HiveContext etc.)

# COMMAND ----------

#spark session
# spark context 
#spark
sc # spark context 
spark # spark session 

# COMMAND ----------

v_list = [1,2,3,4,5,6,7,8,9,10]
rdd_list = sc.parallelize(v_list,3)

# method or function 

# COMMAND ----------

rdd_list.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark Configuration
# MAGIC Spark contains a lot of configurable properties in the following catagories:
# MAGIC 1. Application properties
# MAGIC 2. Runtime environment
# MAGIC 3. Shuffle behavior
# MAGIC 4. Execution behavior
# MAGIC 5. Compression and serialization etc.
# MAGIC 
# MAGIC Let us look at a few of them.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Get All Spark Configuration using `sparkContext(sc).getConf().getAll()`

# COMMAND ----------

sc.getConf().getAll()

# COMMAND ----------

spark.conf.get("spark.sql.shuffle.partitions")

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions","100")

# COMMAND ----------

spark.sql("SET spark.sql.shuffle.partitions=50")

# COMMAND ----------

print(sc.version) # Retrieve SparkContext version
print(sc.pythonVer) # Retrieve Python version
print(sc.master) # Master URL to connect to
print(str(sc.sparkHome)) # Path where Spark is installed on worker nodes
print(str(sc.sparkUser()))# Retrieve name of the Spark User running SparkContext
print(sc.appName) # Return application name
print(sc.applicationId) # Retrieve application ID
print(sc.defaultParallelism)# Return default level of parallelism
print(sc.defaultMinPartitions) # Default minimum number of partitions for

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC _**What is partitions ?**_
# MAGIC <br>
# MAGIC _Partitions in spark is data broken down into smaller blocks_

# COMMAND ----------

# MAGIC %md
# MAGIC #### How partitions are created?
# MAGIC * A contiguous collection of these blocks constitutes a partition. For example HDSF block size: 128 MB
# MAGIC * Size of partitions: `spark.sql.files.maxPartitionBytes`
# MAGIC * You can change partition number with repartition(n) during the read or after df.repartition(20)
# MAGIC * Finally, shuffle partitions are created during the shuffle stage. By default, the number of shuffle partitions is set to 200 in spark.sql.shuffle.partitions. You can adjust this number depending on the size of the data set you have, to reduce the amount of small partitions being sent across the network to executors’ tasks. lower value such as the number of cores on the executors or less

# COMMAND ----------

spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

spark.conf.set("spark.sql.files.maxPartitionBytes","100M")

# COMMAND ----------

# MAGIC %md
# MAGIC __`Question: What does ETL stand for and what are the stages of the process?`__
# MAGIC * Answer: ETL stands for extract-transform-load
# MAGIC 
# MAGIC * Extract refers to ingesting data. Spark easily connects to data in a number of different sources.
# MAGIC * Transform refers to applying structure, parsing fields, cleaning data, and/or computing statistics.
# MAGIC * Load refers to loading data to its final destination, usually a database or data warehouse.
# MAGIC 
# MAGIC __`Question: How does the Spark approach to ETL deal with devops issues such as updating a software version?`__
# MAGIC * Answer: By decoupling storage and compute, updating your Spark version is as easy as spinning up a new cluster. Your old code will easily connect to Azure Blob, or other storage. This also avoids the challenge of keeping a cluster always running, such as with Hadoop clusters.
# MAGIC 
# MAGIC __`Question: How does the Spark approach to data applications differ from other solutions?`__
# MAGIC * Answer: Spark offers a unified solution to use cases that would otherwise need individual tools. For instance, Spark combines machine learning, ETL, stream processing, and a number of other solutions all with one technology.