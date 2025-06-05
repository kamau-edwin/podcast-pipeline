## 🔄 Pipeline Logic Overview

This pipeline is designed to automate the process of downloading podcast episodes from RSS feeds, extracting metadata, transcribing audio using WhisperX, and storing all results in a PostgreSQL database.

The pipeline has two main stages:

---

### 🗂️ Stage 1: Download and Metadata Extraction

**Script:** `download_podcast.py`

This stage uses RSS feeds to:
- Parse podcast episode metadata (title, date, audio URL)
- Download audio files (if not already downloaded)
- Save metadata into a `.csv` file under the `metadata/` directory

#### 📋 Metadata Schema (Saved as CSV)

| Column         | Data Type   | Description                                       |
|----------------|-------------|---------------------------------------------------|
| `podcast`      | `str`       | Name of the podcast (sanitized)                  |
| `podcast_url`  | `str`       | URL of the RSS entry                             |
| `title`        | `str`       | Episode title                                    |
| `episode_id`   | `str`       | Unique identifier for the episode                |
| `published_on` | `datetime`  | Full timestamp of publication                    |
| `pub_date`     | `date`      | Publication date only (no time)                  |
| `audio_url`    | `str`       | Direct link to the audio file                    |
| `duration`     | `int`       | Duration of the episode in seconds               |
| `filename`     | `str`       | Full path to the downloaded audio file (MP3)     |

These columns are written as a single `.csv` file per run under the `metadata/` folder and later uploaded to the `episodes` table in the database.

---

### 🧠 Stage 2: Transcription and Diarization

**Script:** `transcribe.py`

This stage uses [WhisperX](https://github.com/m-bain/whisperx) to:
- Transcribe each episode's speech to text
- Perform speaker diarization
- Save the result as a `.json` file in the `transcripts/` folder

#### 📋 Transcript Schema (Saved as JSON Lines)

| Column         | Data Type   | Description                                      |
|----------------|-------------|--------------------------------------------------|
| `episode_id`   | `str`       | Corresponding ID of the episode (from filename)  |
| `speaker`      | `str`       | Detected speaker label (e.g. SPEAKER_0)         |
| `start_time`   | `float`     | Start time of the spoken segment (in seconds)   |
| `end_time`     | `float`     | End time of the spoken segment (in seconds)     |
| `transcript`   | `str`       | Text spoken by that speaker in the segment      |

Each episode gets its own `.json` file written in JSON Lines format. These files are later uploaded to the `transcripts` table in the database.

---

### 🗄️ Final Database Tables

After running `run_database.py`, the following PostgreSQL tables are populated:

#### 🧾 `episodes` Table

Holds metadata about each podcast episode. Matches the CSV schema.

#### 🗣️ `transcripts` Table

Contains diarized, timestamped transcripts for each episode. Matches the JSON schema.

---

## 🔁 Full Pipeline Flow

```mermaid
graph TD
  A[RSS Feed URL] --> B[Download & Parse Feed]
  B --> C[Download MP3 Files]
  B --> D[Save Metadata CSV]
  C --> E[Transcribe with WhisperX]
  E --> F[Save JSON Transcripts]
  D --> G[Upload to PostgreSQL (episodes)]
  F --> H[Upload to PostgreSQL (transcripts)]
