from google.cloud import texttospeech
import fitz  # PyMuPDF - pdf2text

class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        """Extracts text from a PDF file."""
        try:
            text = ""
            pdf_document = fitz.open(self.pdf_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
            return text
        except Exception as e:
            print(f"An error occurred while extracting text from PDF: {e}")
            return ""

class AudioSynthesizer:
    def __init__(self, project_id, location):
        self.project_id = project_id
        self.location = location
        self.client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    def synthesize_long_audio(self, text, output_gcs_uri):
        """
        Synthesizes long input, writing the resulting audio to `output_gcs_uri`.

        :param text: Text to be synthesized
        :param output_gcs_uri: GCS URI where the audio will be saved
        """
        input_text = texttospeech.SynthesisInput(
            text="Hello, how are you?"
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Standard-A"
        )

        parent = f"projects/{self.project_id}/locations/{self.location}"

        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=input_text,
            audio_config=audio_config,
            voice=voice,
            output_gcs_uri=output_gcs_uri,
        )

        operation = self.client.synthesize_long_audio(request=request)
        # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
        result = operation.result(timeout=300)
        print(
            "\nFinished processing, check your GCS bucket to find your audio file! Printing what should be an empty result: ",
            result,
        )

class TextToSpeechProcessor:
    def __init__(self, pdf_path, project_id, location, output_gcs_uri):
        self.pdf_path = pdf_path
        self.project_id = project_id
        self.location = location
        self.output_gcs_uri = output_gcs_uri
        self.extractor = PDFTextExtractor(pdf_path)
        self.synthesizer = AudioSynthesizer(project_id, location)

    def process(self):
        """Extract text from PDF and synthesize it to audio."""
        text = self.extractor.extract_text()
        if not text:
            raise ValueError("No text extracted from the PDF.")
        self.synthesizer.synthesize_long_audio(text, self.output_gcs_uri)
