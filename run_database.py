import os
import time
import glob
import click
import pandas as pd

from scripts.database import PodcastDB
from scripts.utils import log

@click.command()
@click.option(
    "-m", "--metadata_path", required=True,
    help="Directory containing podcast metadata CSV files."
)
@click.option(
    "-t", "--transcript_path", required=True,
    help="Directory containing transcription JSON files."
)
def main(metadata_path, transcript_path):
    """
    Read all metadata and transcription files, and write them to PostgreSQL database.
    
    Args:
        metadata_path (str): Path to CSV metadata files.
        transcript_path (str): Path to JSON transcription files.
    """
    start = time.time()
    logger = log('write_to_db')
    
    try:
        db = PodcastDB()
        logger.info("Started uploading podcast data to database.")

        # Collect all metadata and transcript files
        metadata_files = glob.glob(os.path.join(metadata_path, "*.csv"))
        transcript_files = glob.glob(os.path.join(transcript_path, "*.json"))

        if not metadata_files:
            logger.warning("No metadata files found.")
        if not transcript_files:
            logger.warning("No transcription files found.")

        if metadata_files:
            metadata_dfs = pd.concat(
                [pd.read_csv(file) for file in metadata_files], ignore_index=True
            )
            metadata_dfs = metadata_dfs[[
                'episode_id', 'title', 'published_on',
                'pub_date', 'duration', 'audio_url',
                'podcast', 'podcast_url'
            ]]
            logger.info(f"Uploading {len(metadata_dfs)} metadata records to 'episodes' table.")
            db.upload_to_db(metadata_dfs, 'episodes')

        if transcript_files:
            transcript_dfs = pd.concat(
                [pd.read_json(file, lines=True) for file in transcript_files], ignore_index=True
            )
            logger.info(f"Uploading {len(transcript_dfs)} transcripts to 'transcripts' table.")
            db.upload_to_db(transcript_dfs, 'transcripts')

        logger.info(f"Finished database upload. Duration: {(time.time() - start) / 60:.2f} minutes")

    except Exception as e:
        logger.error(f"Failed to upload podcast data to database: {e}")

if __name__ == "__main__":
    main()
