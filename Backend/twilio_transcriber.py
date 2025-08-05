import os
import asyncio
import websockets
import json
import base64
from dotenv import load_dotenv

load_dotenv()

class TwilioTranscriber:
    # function that will run automatically when object is created from this class
    # using init to provide args for this object creation
    def __init__(self, on_final_transcript=None, on_complete_turn=None,frontend_websocket=None):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.websocket = None
        self.running_transcript = ""
        self.audio_buffer = bytearray()
        self.buffer_size = 320  # 50ms at 8kHz mu-law (8000/20 = 400 samples, but Twilio sends 160 bytes per 20ms chunk)
        self.chunks_to_buffer = 3  # Buffer 3 chunks (60ms) to exceed 50ms minimum
        self.on_final_transcript = on_final_transcript  # Callback for each final turn
        self.on_complete_turn = on_complete_turn  # Callback for complete user turn (after silence)
        self.frontend_websocket = frontend_websocket
        # Turn aggregation
        self.accumulated_turns = []
        self.last_turn_time = None
        self.silence_timeout = 2.0  # 2 seconds of silence before considering turn complete
        self.turn_timeout_task = None
        
        
    async def connect(self):
        """Connect to AssemblyAI Universal-Streaming WebSocket"""
        uri = f"wss://streaming.assemblyai.com/v3/ws?sample_rate=8000&encoding=pcm_mulaw"
        
        # Create headers with API key
        headers = {
            "Authorization": self.api_key
        }
        
        try:
            # step 1
            # Connect using headers for authentication
            self.websocket = await websockets.connect(uri, additional_headers=headers)
            print("🟢 Connected to Universal-Streaming")
            
            # Start listening for responses from assemblyAi
            # Runs it in parallel, allows other things to run [async operation]
            asyncio.create_task(self.listen_for_responses())
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
           
    
    # this method helps us to connect step 1 and step3
    # get data from assemblyAi 
    # generate into json
    # pass into step 3
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


    # step 3 helps to handle data what we get from step2
    # check data type and based on that we send response 
    async def handle_response(self, data):
        """Handle different types of responses from Universal-Streaming"""
        # Universal-Streaming sends different message formats
        if isinstance(data, dict):
            message_type = data.get("type") or data.get("message_type")
            
            if message_type == "Begin":
                print(f"🟢 Session started: {data.get('id', 'N/A')}")
            
            elif message_type == "Turn":
                # Handle turn-based transcription results
                transcript = data.get("transcript", "")
                end_of_turn = data.get("end_of_turn", False)
                confidence = data.get("end_of_turn_confidence", 0.0)
                turn_order = data.get("turn_order", 0)
                
                if transcript:
                    if end_of_turn:
                        print(f"✅ Final Turn: {transcript} (confidence: {confidence:.2f})")
                        
                        # This is a final transcript segment
                        final_result = {
                            "transcript": transcript,
                            "confidence": confidence,
                            "turn_order": turn_order,
                            "words": data.get("words", []),
                            "end_of_turn": True,
                            "timestamp": asyncio.get_event_loop().time()
                        }
                        
                        # Add to accumulated turns
                        self.accumulated_turns.append(final_result)
                        self.last_turn_time = final_result["timestamp"]
                        
                        # Cancel previous timeout and start new one
                        if self.turn_timeout_task:
                            self.turn_timeout_task.cancel()
                        
                        self.turn_timeout_task = asyncio.create_task(
                            self._wait_for_silence_timeout()
                        )
                        
                        # Call the individual turn callback if provided
                        if self.on_final_transcript:
                            await self.on_final_transcript(final_result)

                        if self.frontend_websocket:
                            await self.frontend_websocket.send_json({
                                "type": "final_transcript",
                                "text": transcript,
                                "confidence": confidence
                            })

                    else:
                        print(f"🟡 Partial Turn: {transcript}", end='\r')
            
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
                # Process any remaining turns
                await self._process_complete_turn()
            
            elif message_type == "Error":
                error_code = data.get("code", "unknown")
                error_message = data.get("message", "Unknown error")
                print(f"❌ Error: {error_code} - {error_message}")
            
            else:
                # Print unknown message types for debugging
                print(f"📝 Unknown message type: {message_type}, data: {data}")
        else:
            print(f"📝 Non-dict response: {data}")
    
      # step 4 sends chunks to assembly ai so it can parse into text 
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
    

    async def _wait_for_silence_timeout(self):
        """Wait for silence timeout, then process complete turn"""
        try:
            await asyncio.sleep(self.silence_timeout)
            await self._process_complete_turn()
        except asyncio.CancelledError:
            # Timeout was cancelled because new speech was detected
            pass
    
    async def _process_complete_turn(self):
        """Process accumulated turns as one complete user turn"""
        if not self.accumulated_turns:
            return
        
        # Combine all accumulated transcripts
        combined_transcript = " ".join([turn["transcript"] for turn in self.accumulated_turns])
        
        # Calculate average confidence
        avg_confidence = sum([turn["confidence"] for turn in self.accumulated_turns]) / len(self.accumulated_turns)
        
        # Create complete turn result
        complete_turn = {
            "transcript": combined_transcript.strip(),
            "confidence": avg_confidence,
            "num_segments": len(self.accumulated_turns),
            "segments": self.accumulated_turns.copy(),
            "is_complete_turn": True
        }

        
        print(f"🎯 COMPLETE USER TURN: '{complete_turn['transcript']}'")
        print(f"   Combined from {complete_turn['num_segments']} segments")
        print(f"   Average confidence: {complete_turn['confidence']:.2f}")
        
        # Call the complete turn callback (this goes to LLM)
        if self.on_complete_turn:
            await self.on_complete_turn(complete_turn)
        
        # Clear accumulated turns
        self.accumulated_turns.clear()
        self.last_turn_time = None
    
 
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