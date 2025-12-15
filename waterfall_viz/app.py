from typing import NamedTuple

from flask import Flask, Response, render_template, stream_with_context, request
import time
import random
import json
import numpy as np

from waterfall_viz.transforms import waterfall_generator
from waterfall_viz import constants

APP = Flask(__name__)


class RequestFieldInputs(NamedTuple):
    carr_freq_input: float
    carr_freq_input_unit_dropdown: str
    sample_freq_input: float
    sample_freq_input_unit_dropdown: str
    gain_input: int
    recv_buffer_input: int
    waterfall_duration_input: float
    waterfall_nfft_input: int
    

def get_input_request_fields() -> RequestFieldInputs:
    return RequestFieldInputs(
        carr_freq_input = request.form.get(
            'carr_freq_input', default=constants.DEFAULT_INPUT_CARRIER_FREQ_MHZ
        ),
        carr_freq_input_unit_dropdown = request.form.get(
            'carr_freq_input_unit_dropdown', default=constants.DEFAULT_FREQ_UNIT
        ),
        sample_freq_input = request.form.get(
            'sample_freq_input', default=constants.DEFAULT_INPUT_SAMPLING_FREQ_MHZ
        ),
        sample_freq_input_unit_dropdown = request.form.get(
            'sample_freq_input_unit_dropdown', default=constants.DEFAULT_FREQ_UNIT
        ),
        gain_input = request.form.get(
            'gain_input', default=constants.DEFAULT_INPUT_GAIN_DB
        ),
        recv_buffer_input = request.form.get(
            'recv_buffer_input', default=constants.DEFAULT_INPUT_RECV_BUFFER_SIZE
        ),
        waterfall_duration_input = request.form.get(
            'waterfall_duration_input', default=constants.DEFAULT_INPUT_WATERFALL_DURATION_SEC
        ),
        waterfall_nfft_input = request.form.get(
            'waterfall_nfft_input', default=constants.DEFAULT_INPUT_WATERFALL_NFFT
        )
    )
    
    
FIELD_INPUTS: RequestFieldInputs
        

@APP.route('/', methods=['GET', 'POST'])
def index():
    global FIELD_INPUTS
    FIELD_INPUTS = get_input_request_fields()
    print(FIELD_INPUTS.waterfall_nfft_input)
    return render_template(
        'index.html',
        carr_freq_input_value=FIELD_INPUTS.carr_freq_input,
        sample_freq_input_value=FIELD_INPUTS.sample_freq_input,
        gain_input_value=FIELD_INPUTS.gain_input,
        recv_buffer_input_value=FIELD_INPUTS.recv_buffer_input,
        waterfall_duration_input_value=FIELD_INPUTS.waterfall_duration_input,
        waterfall_nfft_input_value=FIELD_INPUTS.waterfall_nfft_input,
        
    )


@APP.route('/events')
def sse_data():
    field_inputs = FIELD_INPUTS
    print("Within events .... ", field_inputs.waterfall_nfft_input)

    response = Response(
        # stream_with_context(generate_random_heatmap_data()), 
        stream_with_context(
            waterfall_generator(
                fft_size=int(field_inputs.waterfall_nfft_input))
        ), 
        mimetype="text/event-stream"
    )
    
    # Prevent caching of the response
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    APP.run(debug=True)
