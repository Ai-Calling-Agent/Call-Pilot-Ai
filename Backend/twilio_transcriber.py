import os
import asyncio
import websockets
import json
import base64
from dotenv import load_dotenv

load_dotenv()

class TwilioTranscriber:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.websocket = None
        self.running_transcript = ""
        self.audio_buffer = bytearray()
        self.buffer_size = 320  # 50ms at 8kHz mu-law (8000/20 = 400 samples, but Twilio sends 160 bytes per 20ms chunk)
        self.chunks_to_buffer = 3  # Buffer 3 chunks (60ms) to exceed 50ms minimum
        
    async def connect(self):
        """Connect to AssemblyAI Universal-Streaming WebSocket"""
        # Universal-Streaming endpoint with query parameters
        uri = f"wss://streaming.assemblyai.com/v3/ws?sample_rate=8000&encoding=pcm_mulaw"
        
        # Create headers with API key
        headers = {
            "Authorization": self.api_key
        }
        
        try:
            # Connect using headers for authentication
            self.websocket = await websockets.connect(uri, additional_headers=headers)
            print("🟢 Connected to Universal-Streaming")
            
            # Start listening for responses
            asyncio.create_task(self.listen_for_responses())
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            # Fallback to token-based auth if headers don't work
            try:
                fallback_uri = f"wss://streaming.assemblyai.com/v3/ws?sample_rate=8000&encoding=pcm_mulaw&token={self.api_key}"
                self.websocket = await websockets.connect(fallback_uri)
                print("🟢 Connected to Universal-Streaming (fallback)")
                asyncio.create_task(self.listen_for_responses())
            except Exception as fallback_error:
                print(f"❌ Fallback connection error: {fallback_error}")
    
    async def listen_for_responses(self):
        """Listen for transcription responses"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_response(data)
        except websockets.exceptions.ConnectionClosed:
            print("🔒 WebSocket connection closed")
        except Exception as e:
            print(f"❌ Error listening for responses: {e}")
    
    async def handle_response(self, data):
        """Handle different types of responses from Universal-Streaming"""
        # Universal-Streaming sends different message formats
        if isinstance(data, dict):
            message_type = data.get("type") or data.get("message_type")
            
            if message_type == "Begin":
                print(f"🟢 Session started: {data.get('id', 'N/A')}")
            
            elif message_type == "PartialTranscript":
                text = data.get("text", "")
                if text:
                    print(f"🟡 Partial: {text}", end='\r')
            
            elif message_type == "FinalTranscript":
                text = data.get("text", "")
                if text:
                    print(f"✅ Final: {text}")
                    # Store for voice agent processing
                    self.running_transcript += " " + text if self.running_transcript else text
            
            elif message_type == "SessionTerminated" or message_type == "End":
                print("🔒 Session terminated")
            
            elif message_type == "Error":
                error_code = data.get("code", "unknown")
                error_message = data.get("message", "Unknown error")
                print(f"❌ Error: {error_code} - {error_message}")
            
            else:
                # Print unknown message types for debugging
                print(f"📝 Unknown message type: {message_type}, data: {data}")
        else:
            print(f"📝 Non-dict response: {data}")
    
    async def stream_audio(self, audio_bytes):
        """Stream audio data to Universal-Streaming with buffering"""
        if self.websocket and self.websocket.close_code is None:
            try:
                # Add audio to buffer
                self.audio_buffer.extend(audio_bytes)
                
                # Check if we have enough audio buffered (at least 50ms worth)
                # Twilio sends 160 bytes per 20ms chunk, so we need at least 400 bytes for 50ms
                min_buffer_size = 400  # 50ms worth of mu-law audio at 8kHz
                
                if len(self.audio_buffer) >= min_buffer_size:
                    # Send the buffered audio
                    audio_to_send = bytes(self.audio_buffer)
                    await self.websocket.send(audio_to_send)
                    
                    # Clear the buffer
                    self.audio_buffer.clear()
                    
            except Exception as e:
                print(f"❌ Error streaming audio: {e}")
    
    async def terminate_session(self):
        """Terminate the transcription session"""
        if self.websocket and self.websocket.close_code is None:
            try:
                # Send any remaining buffered audio before closing
                if len(self.audio_buffer) > 0:
                    audio_to_send = bytes(self.audio_buffer)
                    await self.websocket.send(audio_to_send)
                    self.audio_buffer.clear()
                
                # Close the connection
                await self.websocket.close()
                print("🔒 Session terminated")
            except Exception as e:
                print(f"❌ Error terminating session: {e}")
    
    def get_running_transcript(self):
        """Get the accumulated transcript for voice agent processing"""
        return self.running_transcript
    
    def clear_running_transcript(self):
        """Clear the running transcript after processing"""
        self.running_transcript = ""