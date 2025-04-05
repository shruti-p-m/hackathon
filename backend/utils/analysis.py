import whisper
import torchaudio
from moviepy.editor import VideoFileClip
from transformers import pipeline
import os

# Load models
whisper_model = whisper.load_model("base")
sentiment_pipeline = pipeline("sentiment-analysis")
emo_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)


def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)


def get_transcript(audio_path):
    result = whisper_model.transcribe(audio_path)
    transcript = result["text"]
    segments = result["segments"]
    transcript_segments = [
        {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
        for seg in segments
    ]
    return transcript, transcript_segments


def summarize_transcript(transcript):
    # Placeholder: Replace with real summarization model
    return "Summary: " + transcript[:100] + "..."


def analyze_sentiment_and_emotion(transcript_segments):
    speakers = {"Speaker 1": "", "Speaker 2": ""}  # Dummy speaker assignment for now
    for seg in transcript_segments:
        if "Hello" in seg["text"]:
            speakers["Speaker 1"] += seg["text"] + " "
        else:
            speakers["Speaker 2"] += seg["text"] + " "

    sentiment_results = {
        speaker: sentiment_pipeline(text)[0]['label']
        for speaker, text in speakers.items()
    }
    emotion_results = {
        speaker: sorted(emo_pipeline(text)[0], key=lambda x: -x['score'])[0]['label']
        for speaker, text in speakers.items()
    }
    return sentiment_results, emotion_results


def generate_tone_timeline(transcript_segments):
    timeline = []
    for seg in transcript_segments:
        sentiment = sentiment_pipeline(seg["text"])[0]['label']
        timeline.append({"time": seg["start"], "tone": sentiment})
    return timeline


def process_video(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    extract_audio(video_path, audio_path)

    transcript, segments = get_transcript(audio_path)
    summary = summarize_transcript(transcript)
    tone_timeline = generate_tone_timeline(segments)
    sentiments, emotions = analyze_sentiment_and_emotion(segments)

    return {
        "transcript": transcript,
        "transcript_with_timestamps": segments,
        "meeting_minutes": summary,
        "tone_timeline": tone_timeline,
        "sentiment_per_speaker": sentiments,
        "emotion_per_speaker": emotions
    }
