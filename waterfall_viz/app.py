from flask import Flask, Response, render_template, stream_with_context, request
import time
import random
import json
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Serve the HTML page with the Plotly chart setup."""
    carr_freq_input: float = 100
    if request.method == 'POST':
        carr_freq_input = request.form.get('carr_freq_input')
        carr_freq_input_unit_dropdown = request.form.get('carr_freq_input_unit_dropdown')
        print(f"Carr Freq Input: {carr_freq_input}")
        print(f"Carr Freq Unit: {carr_freq_input_unit_dropdown}")
        
        return render_template(
            'index.html',
            carr_freq_input_value=carr_freq_input
        )
    return render_template('index.html', carr_freq_input_value=carr_freq_input)


@app.route('/events')
def sse_data():
    """Stream real-time data as Server-Sent Events."""
    def generate_random_heatmap_data():
        while True:
            # Generate a new 10x10 matrix of random data
            z_data = [[random.random() for _ in range(128)] for _ in range(128)]
            
            # Format the data as JSON and wrap it in the SSE 'data: ' format
            json_data = json.dumps(z_data)
            yield f"data:{json_data}\n\n"
            
            time.sleep(0.05)

    response = Response(
        stream_with_context(generate_random_heatmap_data()), 
        mimetype="text/event-stream"
    )
    
    # Prevent caching of the response
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

if __name__ == '__main__':
    app.run(debug=True)
