# src/priceoye/routes.py

from flask import Blueprint, render_template, request, session, jsonify, Response
from priceoye.agents_ import orchestrator_agent
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
import logging
import time
import random
import json
import asyncio

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the PriceOye homepage."""
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html', chat_history=session['chat_history'])

def format_input(user_input, history):
    """Format the input with conversation history for chat completions."""
    messages = []
    for msg in history:
        if msg.get('user'):
            messages.append({"role": "user", "content": msg['user']})
        if msg.get('agent'):
            messages.append({"role": "assistant", "content": msg['agent']})
    messages.append({"role": "user", "content": user_input})
    return messages

def retry_on_503(func, max_attempts=3, initial_delay=1):
    """Retry a function on 503 errors with exponential backoff."""
    def wrapper(*args, **kwargs):
        attempts = 0
        delay = initial_delay
        while attempts < max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if '503' in str(e) or 'UNAVAILABLE' in str(e):
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    sleep_time = delay * (2 ** (attempts - 1)) * (0.8 + random.uniform(0, 0.4))
                    logger.warning(f"503 error on attempt {attempts}/{max_attempts}. Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                else:
                    raise
    return wrapper

@bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat queries with history (non-streaming)."""
    try:
        data = request.get_json()
        user_input = data.get('message') if data else None
        if not user_input:
            logger.error("No message provided in request")
            return jsonify({'error': 'No message provided'}), 400
        
        logger.debug(f"Received user input: {user_input}")
        
        # Get chat history
        chat_history = session.get('chat_history', [])
        
        # Format input with history
        full_input = format_input(user_input, chat_history)
        
        # Run agent with retry
        @retry_on_503
        def run_agent():
            try:
                # Get or create event loop
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Define async function to process stream
                async def process_stream():
                    result = Runner.run_streamed(orchestrator_agent, full_input)
                    full_response = ""
                    async for event in result.stream_events():
                        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                            full_response += event.data.delta
                    return full_response
                
                # Run async function in loop
                return loop.run_until_complete(process_stream())
            except Exception as e:
                logger.error(f"Streaming error: {str(e)}")
                raise
        
        response = run_agent()
        logger.debug(f"Agent response: {response}")
        
        # Update chat history
        chat_history.append({'user': user_input, 'agent': response})
        session['chat_history'] = chat_history[-10:]  # Limit to last 10 messages
        session.modified = True
        
        return jsonify({'response': response, 'history': session['chat_history']})
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@bp.route('/chat_stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat queries with history."""
    try:
        data = request.get_json()
        user_input = data.get('message') if data else None
        if not user_input:
            return Response(json.dumps({'error': 'No message provided'}), status=400, mimetype='application/json')
        
        chat_history = session.get('chat_history', [])
        
        # Format input with history
        full_input = format_input(user_input, chat_history)
        
        def generate():
            try:
                # Get or create event loop
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Define async function to process stream
                async def process_stream():
                    result = Runner.run_streamed(orchestrator_agent, full_input)
                    full_response = ""
                    async for event in result.stream_events():
                        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                            chunk = event.data.delta
                            full_response += chunk
                            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                    
                    # Update chat history
                    chat_history.append({'user': user_input, 'agent': full_response})
                    session['chat_history'] = chat_history[-10:]  # Limit to last 10 messages
                    session.modified = True
                    yield f"data: {json.dumps({'complete': True, 'history': session['chat_history']})}\n\n"
                
                # Run async function and yield results
                for output in loop.run_until_complete(process_stream()):
                    yield output
            except Exception as e:
                logger.error(f"Error in /chat_stream: {str(e)}")
                yield f"data: {json.dumps({'error': f'Server error: {str(e)}'})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        logger.error(f"Error in /chat_stream endpoint: {str(e)}")
        return Response(json.dumps({'error': f'Server error: {str(e)}'}), status=500, mimetype='application/json')