import os

try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
except ImportError:
    Model = None

def offline_speech_to_text(duration=5, model_path="vosk-model-small-en-us-0.15"):
    if Model is None:
        return "Speech-to-text dependencies are missing (vosk/pyaudio)."
    if not os.path.exists(model_path):
        return f"Please download the Vosk model and place it at '{model_path}'."

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    results = []
    for _ in range(0, int(16000 / 8192 * duration)):
        data = stream.read(8192, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            res = rec.Result()
            results.append(res)
    stream.stop_stream()
    stream.close()
    p.terminate()

    final_result = rec.FinalResult()
    results.append(final_result)

    # Combine partial results
    text = ""
    import json as js
    for r in results:
        try:
            j = js.loads(r)
            text += j.get('text', '') + " "
        except:
            continue
    return text.strip()
