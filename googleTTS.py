from google.cloud import texttospeech

class TextToSpeechSynthesizer:
    def __init__(self, 
                 text="Hello, World!", 
                 language_code="en-US", 
                 ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
                 audio_encoding=texttospeech.AudioEncoding.MP3,
                 output_file="output.mp3"):
        """
        Initializes the TextToSpeechSynthesizer with the specified parameters.
        
        Args:
            text (str): The text to synthesize.
            language_code (str): The language code for the voice.
            ssml_gender (SsmlVoiceGender): The gender of the voice.
            audio_encoding (AudioEncoding): The audio encoding format.
            output_file (str): The filename for the output audio file.
        """
        self.text = text
        self.language_code = language_code
        self.ssml_gender = ssml_gender
        self.audio_encoding = audio_encoding
        self.output_file = output_file
        self.client = texttospeech.TextToSpeechClient()

    def set_text(self, text):
        """Sets the text to be synthesized."""
        self.text = text

    def set_language_code(self, language_code):
        """Sets the language code for the voice."""
        self.language_code = language_code

    def set_ssml_gender(self, ssml_gender):
        """Sets the SSML voice gender."""
        self.ssml_gender = ssml_gender

    def set_audio_encoding(self, audio_encoding):
        """Sets the audio encoding format."""
        self.audio_encoding = audio_encoding

    def set_output_file(self, output_file):
        """Sets the filename for the output audio file."""
        self.output_file = output_file

    def synthesize_speech(self):
        """Synthesize the speech based on the current settings and save it to the output file."""
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=self.text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_code, 
            ssml_gender=self.ssml_gender
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=self.audio_encoding
        )

        # Perform the text-to-speech request
        response = self.client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )

        # The response's audio_content is binary
        with open(self.output_file, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{self.output_file}"')