
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

def get_youtube_transcript(url):
    try:
        # Validating and extracting the video ID from the URL
        if "https://www.youtube.com/watch?v=" not in url:
            return "Invalid URL. Please provide a valid YouTube video URL."

        start_index = url.index("https://www.youtube.com/watch?v=") + len("https://www.youtube.com/watch?v=")
        video_id = url[start_index:]

        # Getting the transcript using the YouTubeTranscriptApi
        srt = YouTubeTranscriptApi.get_transcript(video_id)

        # Combining the transcript text
        transcript_text = ''
        for i in srt:
            transcript_text += i['text'] + "\n"

        return transcript_text

    except NoTranscriptFound:
        return "Transcript not available for this video."

    except Exception as e:
        return f"An error occurred: {str(e)}"
