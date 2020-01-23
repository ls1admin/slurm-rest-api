# Slurm RestAPI

This is a flask based rest interface to slurm.
There are two sub-packages which implement interfaces to different parts of the slurm manager
  * acctapi - interacts with the accounting database slurmdb to get job history and user associations
  * slurmapi - interacts with the pyslurm package to get queue, node, partition, and stat info

Endpoints are
```
/users - can be filtered on user
/history - can be filtered on offset,limit,jobid,user,partition,jobname,associd
/queue
/partitions
/usage - returns additional partition usage information
/nodes
/stats
/load - returns archived load information, `archive_usage_load` must be enabled in config.yml
```

### Configuration

Before setting up the api, you will need to install and run Slurm.

##### Config
Clone this repository, and then modify the `config.yml` file to match your slurmdb credentials and usage needs. Remove the `#` on each line you would like to use and modify their contents, otherwise the system will use the default values which likely will not align to your database.

Note: You may want to create a new user with read-only access for reading from your account database.

The `table_assoc` and `table_job` variables must match the schema names of the assoc and job tables respectively.

### Setup, Install, and Run

Slurm-rest-api is dependant on conda being installed on your system. If you do not already have conda installed you can download miniconda from https://conda.io/miniconda.html

##### Supported versions
Slurm-rest-api has been tested to work on the following versions on slurm and pyslurm:

Slurm version `18.08.0` on pyslurm `18.08.0`.

#### Setup Scripts
The `build.sh` and `run.sh` scripts take care of the environment and dependencies needed for slurm-rest-api

##### Setup
To build on slurm version `18.08.0`run:
```
bash build.sh --pyslurm_version="18.08.0" 
```

If you are running a different version of slurm, you will need to include the version arguments when running the script.
More details on these arguments can be found by running:
```
bash build.sh --help
```

For a list of slurm versions that are supported by pyslurm, and more information on pyslurm install options, visit https://github.com/PySlurm/pyslurm

##### Run
To run slurm-rest-api, run:
```
bash run.sh
```

##### Testing
To verify that Slurm-rest-api is running correctly, enable `serve_index` in `config.yml`, re-run the app, and open your browser to `http://localhost:5000/`. This page will verify that the routes are accessable. Note that some routes may take some time if your database is large.

### Example routes for development

All routes return data in the `JSON` format.

#### Users

| Route | Description |
| --- | --- |
| `http://localhost:5000/users` | All user data |
| `http://localhost:5000/users?name=root` | Returns the user data for a specific user |

#### History

Returns the job history.

`http://localhost:5000/history`

Filters

Multiple filters can be included in a request by seperating them with `&`. See the offset filter for an example of using multiple filters to create history pagination.

| Filter | Comparators | Description | Default | Example |
| --- | --- | --- | --- | --- |
| `limit` | `=` | Number of entries to return | `10` | `http://localhost:5000/history?limit=25` |
| `offset` | `=` | Number of entries to skip, can be used as a "next page" when the number is set to a multiple of the limit parameter | `0` | `http://localhost:5000/history?limit=25&offset=25` |
| `user` | `=` | Only show results from a specific user | N/A | `http://localhost:5000/history?user=galaxy` |
| `partition` | `=` | Only show results from a specific partition | N/A | `http://localhost:5000/history?partition=high` |
| `jobid` | `=`,`>`,`<`,`>=`,`<=` | Only show results with job id matching criteria | N/A |  `http://localhost:5000/history?jobid<=987654` |
| `jobname` | `=` | Only show results with a specific job name | N/A | `http://localhost:5000/history?jobname=g12345_bcftools` |
| `state` | `=` | Only show results with a specific state. See below for state numbers | N/A | `http://localhost:5000/history?state=1` |

State number to type mapping for state filtering

| State Number | State Type |
| --- | --- |
| `0` | `JOB_PENDING` |
| `1` | `JOB_RUNNING` |
| `2` | `JOB_SUSPENDED` |
| `3` | `JOB_COMPLETE` |
| `4` | `JOB_CANCELLED` |
| `5` | `JOB_FAILED` |
| `6` | `JOB_TIMEOUT` |
| `7` | `JOB_NODE_FAIL` |
| `8` | `JOB_PREEMPTED` |
| `9` | `JOB_BOOT_FAIL` |
| `10` | `JOB_DEADLINE` |

#### Queue

Returns the Job Queue

`http://localhost:5000/queue`

#### Partitions

Returns information about all partitions

`http://localhost:5000/partitions`

#### Nodes

Returns information about all nodes

`http://localhost:5000/nodes`

#### Usage

Returns a matrix of data showing all partitions, the nodes on those partitions, and the cpu/memory usage by jobs on each of them.

`http://localhost:5000/usage`

#### Stats

Returns Slurm Statistics

`http://localhost:5000/stats`


#### Load

Returns a list of time stamped load information. When usage load archiving is active, slurm-rest-api will periodically save the current system load, which can then be queried with this route.

| Filter | Comparators | Description | Default | Example |
| --- | --- | --- | --- | --- |
| `time` | `=` | Time period of data to return, measured in seconds (last X seconds) | Same as `archive_wait_time` so a single entry is returned | `http://localhost:5000/load?time=60` |
| `offset` | `=` | Number of seconds to skip, can be used as a "next page" when the number is set to a multiple of the limit parameter | `0` | `http://localhost:5000/load?time=60&offset=120` |

## Legal ##

Copyright Government of Canada 2018

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

Jie Li updated the models in acctapi to accommdate the new version of SLURM

## Contact ##

**Jeffrey Thiessen**: jeffrey.thiessen@canada.ca

**Gary van Domselaar**: gary.vandomselaar@canada.ca

**Jie Li**:
jie.li@ttu.edu

