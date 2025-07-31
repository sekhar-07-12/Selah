import os
import wave
import json

try:
    from vosk import Model, KaldiRecognizer
except ImportError:
    Model = None


def transcribe_uploaded_audio(wav_file_path, model_path="vosk-model-small-en-us-0.15"):
    """
    Transcribes a given WAV audio file using the Vosk offline speech recognition model.

    Args:
        wav_file_path (str): Path to the WAV audio file.
        model_path (str): Path to the Vosk model directory.

    Returns:
        str: The transcribed text from the audio file or an error message.
    """
    if Model is None:
        return "Vosk module is not installed."

    if not os.path.exists(model_path):
        return f"Vosk model not found at '{model_path}'. Please download and place it correctly."

    if not os.path.exists(wav_file_path):
        return "Audio file not found."

    try:
        wf = wave.open(wav_file_path, "rb")
    except Exception as e:
        return f"Failed to open audio file: {e}"

    # Verify audio format: WAV, Mono CMU, 16kHz, 16-bit PCM
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        return "Audio file must be WAV format Mono PCM 16kHz."

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            partial_result = json.loads(rec.Result())
            results.append(partial_result)

    final_result = json.loads(rec.FinalResult())
    results.append(final_result)

    # Combine text parts
    text = " ".join([res.get("text", "") for res in results]).strip()

    return text if text else "No speech detected in audio."
