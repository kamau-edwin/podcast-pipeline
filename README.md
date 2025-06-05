# 🎙️ Podcast Pipeline

This repository contains a complete pipeline for downloading, transcribing, and storing podcast episodes in a PostgreSQL database. It leverages RSS feeds, WhisperX for transcription, and SQLAlchemy for database integration.

---

## Features

- Download podcast audio episodes via RSS
- Extract and save metadata (e.g. title, publish date, duration)
- Transcribe and diarize episodes using [WhisperX](https://github.com/m-bain/whisperx)
- Save transcripts and metadata to a PostgreSQL database
- Log every stage for reproducibility and debugging

---

## Tech Stack

- Python 3.10+
- Linux or Unix 

Make sure `ffmpeg` is installed and accessible in your PATH. `WhisperX` relies on it for  audio processing.


## Setup Instructions

### 1. Clone the Repository

```bash
git clone git@github.com:kamau-edwin/podcast-pipeline.git
cd podcast-pipeline
# Recommendation Create a virtual env
# install dependencies
pip install -r requirements.txt

```

### 2. Create a Configuration file

In the `scripts` folder edit the file `config.py` 

```python
   # required for database connection
	DB_CONFIG = {
	    'user': 'your_username', # database admin username
	    'password': 'your_password', # database admin password
	    'host': 'cloud host path', # database instance address
	    'port': '5432',
	    'database': 'database name' # database name need to be created before hand
	}
	# required for Diarization 
	HF_TOKEN =  "your_huggingface_token"  
```
See [obtaining a hugging face token](https://github.com/kamau-edwin/podcast-pipeline/blob/main/docs/hugging_face.md)


## Running the Pipeline

### Step 1: Download and Transcribe Podcasts

Use the CLI to download podcast episodes and generate transcripts:
**RSS_URL** comes from the input file `rss_feed.csv`


```bash
python main.py -u <RSS_URL> -p downloads
```
### Step 2: Write all metadata and transcript files to PostgreSQL 

After running step 1 for all the RSS URLs run this step 

```bash
	python run_database.py -m metadata -t transcripts
```

## Documentation  
The following documents provide a more detail overview of the pipeline, design decision

* [Pipeline logic overview](https://github.com/kamau-edwin/podcast-pipeline/blob/main/docs/pipeline_logic.md)


