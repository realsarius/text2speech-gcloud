from text_to_speech import TextToSpeechProcessor
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    pdf_file_path = "pdf/the-book-collector-example-2023-01-001.pdf"
    processor = TextToSpeechProcessor(
        pdf_path=pdf_file_path,
        project_id=os.getenv("PROJECT_ID"),
        location=os.getenv("LOCATION"),
        output_gcs_uri=f"{os.getenv('OUTPUT_GCS_URI')}/output2.wav"
    )
    processor.process()
