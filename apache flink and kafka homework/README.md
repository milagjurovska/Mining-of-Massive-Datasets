# RNMP Homework 1 – Apache Flink + Kafka (Python)

This project implements the homework requirements using:

- **Apache Kafka** (via Docker Compose)
- **Apache Flink** (Python API / PyFlink)
- A **Python producer** (`produce_messages.py`) that writes random sensor messages to Kafka topic **`sensors`**
- A **Python consumer** (`consume_messages.py`) that reads results from Kafka topics **`results1`** and **`results2`**
- A **Flink job** (`flink_job.py`) that:
  - Reads from Kafka topic `sensors`
  - Uses **time windows** (size **X ms**, slide **Y ms**) per key
  - Writes:
    - To `results1`: **count of messages** per window and key  
    - To `results2`: **min / max / count / average** per window and key

All commands below assume:

- You are on **Windows**
- Your project folder is: `C:\RNMP_homework1`
- You have **Docker Desktop** installed and running
- You have **Python 3.10** installed

---

## 1. Project structure

Expected files in `C:\RNMP_homework1`:

- `docker-compose.yml` – starts **Kafka** and **Zookeeper**
- `produce_messages.py` – sends sensor messages to topic **`sensors`**
- `consume_messages.py` – reads results from topics **`results1`** and **`results2`**
- `flink_job.py` – the **Flink streaming job** (Python)
- `venv310/` – Python **virtual environment** on Windows for producer/consumer

---

## 2. Create & prepare the Windows virtual environment

From **PowerShell**:

```powershell
cd C:\RNMP_homework1

# Create a venv (if you don't already have one)
python -m venv venv310

# Activate the venv
.\venv310\Scripts\Activate.ps1

# Upgrade pip & tools (recommended)
python -m pip install --upgrade pip setuptools wheel

# Install dependencies for producer / consumer
pip install kafka-python
```
You will use this same venv to run produce_messages.py and consume_messages.py on Windows.

## 3. Start Kafka and Zookeeper (Docker Compose)

In the same `C:\RNMP_homework1` folder, run:

cd C:\RNMP_homework1
```powershell
# Start Zookeeper + Kafka in the background
docker-compose up -d
```
## 4. Run the Flink job inside Docker
### 4.1. Attach container to the same Docker network

First, check the Docker network name that docker-compose created:
```powershell
docker network ls
```

You should see a network like: `rnmp_homework1_default`


Now start a Python 3.10 container attached to that network and mounting the project folder:
```powershell
docker run -it --rm `
  --network rnmp_homework1_default `
  -v C:\RNMP_homework1:/job `
  python:3.10-slim bash
 ```
Inside the container you will get a Linux shell, with /job pointing to your project folder.

### 4.2. Install Java (OpenJDK) inside the container

PyFlink requires Java. Inside the container shell run:
```powershell
apt-get update
apt-get install -y default-jre
```

This will install a JRE under `/usr/lib/jvm/`.

### 4.3. Set Java environment variables

Still inside the container:
```powershell
export JAVA_HOME=/usr/lib/jvm/default-java
export PATH="$JAVA_HOME/bin:$PATH"
```

#### Required to avoid the "InaccessibleObjectException" with Java 17+
```powershell
export JAVA_TOOL_OPTIONS="--add-opens=java.base/java.lang=ALL-UNNAMED"
```
### 4.4. Use the existing venv from the project 

Because the venv already lives under C:\RNMP_homework1 and we mounted that folder into /job, you can simply reuse it.

Inside the container:
```powershell
cd /job

# Activate the existing virtualenv
source venv/bin/activate
```
### 4.5. Run the Flink job

With the venv active and Java configured, still inside the container:
```powershell
cd /job
python flink_job.py
```

If everything is correct, you should see something like:

`Flink job started. Streaming from 'sensors' to 'results1' and 'results2'...`


Leave this process running.
This is your streaming job that continuously consumes from sensors and produces to results1 and results2.

## 5.Run the producer (send test data to sensors)

Back on Windows PowerShell, in another terminal window:
```powershell
cd C:\RNMP_homework1

# Activate the Windows venv
.\venv310\Scripts\Activate.ps1

# Start the producer
.\venv310\Scripts\python.exe .\produce_messages.py
```


You should see JSON messages printed like:

`{"key": "A", "value": 410, "timestamp": 1763773326021}`

`{"key": "D", "value": 792, "timestamp": 1763773327257}
...`

You can stop the producer at any time with Ctrl + C.

## 6.Run the consumer (verify results1 and results2)

In a third PowerShell window on Windows:
```powershell
cd C:\RNMP_homework1

# Activate the venv
.\venv310\Scripts\Activate.ps1

# Start the consumer
.\venv310\Scripts\python.exe .\consume_messages.py
```

You should see output similar to:

`Listening on topics: ['results1', 'results2'] ...`

`[results1] {"key":"D","window_start":1763775840000,"window_end":1763775900000,"cnt":5}`

`[results1] {"key":"A","window_start":1763775840000,"window_end":1763775900000,"cnt":3}
...`

`[results2] {"key":"B","window_start":1669748895000,"window_end":1669748896000,"min_value":10,"count":10,"average":55.55,"max_value":100}
...`