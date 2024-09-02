import os
from flask import Flask, render_template, request, jsonify, Response, send_file
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__, static_folder='templates')

speech_config = speechsdk.SpeechConfig(subscription="adff6f8e12d24ecf8f12cacb35b9ed12", region="eastus")
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
recognition_result = ""
is_listening = False


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    global is_listening, transcribed_text
    action = request.json.get('action')

    if action == 'start':
        is_listening = True
        transcribed_text = ""  # Reset the transcribed text on new start
        return jsonify(status='started')

    elif action == 'pause':
        is_listening = False
        return jsonify(status='paused')

    elif action == 'resume':
        is_listening = True
        return jsonify(status='resumed')

    elif action == 'stop':
        is_listening = False
        # Save transcribed text to a file
        file_path = 'transcription.txt'
        with open(file_path, 'w') as f:
            f.write(transcribed_text)
        return jsonify(status='stopped', file_path=file_path)

    return jsonify(status='error')

@app.route('/control-stream', methods=['GET'])
def control_stream():
    def generate():
        global is_listening, transcribed_text
        while is_listening:
            result = speech_recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                transcribed_text += result.text + " "  # Accumulate the transcribed text
                yield f"data: {result.text}\n\n"
            elif result.reason == speechsdk.ResultReason.NoMatch:
                yield f"data: [No speech detected]\n\n"
            else:
                yield f"data: [Error: {result.reason}]\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)