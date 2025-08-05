from pydub import AudioSegment
import io

def convert_mp3_to_mulaw(mp3_bytes: bytes) -> bytes:
    mp3 = AudioSegment.from_file(io.BytesIO(mp3_bytes), format="mp3")
    mulaw = mp3.set_frame_rate(8000).set_channels(1).set_sample_width(1)

    output = io.BytesIO()
    mulaw.export(output, format="raw", codec="pcm_mulaw")
    return output.getvalue()
