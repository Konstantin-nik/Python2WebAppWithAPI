from flask import Flask, render_template, request
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
from pydub import AudioSegment
from pydub.playback import play

credentials = service_account.Credentials.from_service_account_file('bcnpy2key.json')

app = Flask(__name__)

client = texttospeech.TextToSpeechClient(credentials=credentials)


def translate_text(target: str, text: str) -> dict:

    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result


def tts(text, language):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("static/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    audio = AudioSegment.from_file("static/output.mp3", format="mp3")
    play(audio)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate_m():
    text_to_translate = request.form['text_to_translate']
    target_language = request.form['target_language']

    result = translate_text(target_language, text_to_translate)
    tts(result["translatedText"], target_language)

    return render_template('translated.html', original_text=text_to_translate,
                           translated_text=result["translatedText"], audio_url='output.mp3')


if __name__ == '__main__':
    app.run(debug=True)
