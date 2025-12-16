from typing import NamedTuple

from flask import Flask, Response, render_template, stream_with_context, request

from waterfall_viz.transforms import waterfall_generator, convert_frequency_units
from waterfall_viz.generators import PulsedToneGenerator
from waterfall_viz import constants


APP = Flask(__name__)


class RequestFieldInputs(NamedTuple):
    carr_freq_input_hz: float
    sample_freq_input_hz: float
    gain_input: int
    recv_buffer_input: int
    waterfall_duration_input: float
    waterfall_nfft_input: int
    

def get_input_request_fields() -> RequestFieldInputs:
    carr_freq_input = float(request.form.get(
        'carr_freq_input', default=constants.DEFAULT_INPUT_CARRIER_FREQ_MHZ
    ))
    carr_freq_input_unit_dropdown = request.form.get(
        'carr_freq_input_unit_dropdown', default=constants.DEFAULT_FREQ_UNIT
    )
    carr_freq_input_hz = convert_frequency_units(
        carr_freq_input, carr_freq_input_unit_dropdown
    )
    
    sample_freq_input = float(request.form.get(
        'sample_freq_input', default=constants.DEFAULT_INPUT_SAMPLING_FREQ_MHZ
    ))
    sample_freq_input_unit_dropdown = request.form.get(
        'sample_freq_input_unit_dropdown', default=constants.DEFAULT_FREQ_UNIT
    )
    sample_freq_input_hz = convert_frequency_units(
        sample_freq_input, sample_freq_input_unit_dropdown
    )
    
    return RequestFieldInputs(
        carr_freq_input_hz = carr_freq_input_hz,
        sample_freq_input_hz = sample_freq_input_hz,
        gain_input = int(request.form.get(
            'gain_input', default=constants.DEFAULT_INPUT_GAIN_DB
        )),
        recv_buffer_input = int(request.form.get(
            'recv_buffer_input', default=constants.DEFAULT_INPUT_RECV_BUFFER_SIZE
        )),
        waterfall_duration_input = float(request.form.get(
            'waterfall_duration_input', default=constants.DEFAULT_INPUT_WATERFALL_DURATION_SEC
        )),
        waterfall_nfft_input = int(request.form.get(
            'waterfall_nfft_input', default=constants.DEFAULT_INPUT_WATERFALL_NFFT
        ))
    )
    
    
FIELD_INPUTS: RequestFieldInputs
        

@APP.route('/', methods=['GET', 'POST'])
def index():
    global FIELD_INPUTS
    FIELD_INPUTS = get_input_request_fields()
    carr_freq_input_value = convert_frequency_units(
        FIELD_INPUTS.carr_freq_input_hz, "Hz", constants.DEFAULT_FREQ_UNIT
    )
    sample_freq_input_value = convert_frequency_units(
        FIELD_INPUTS.sample_freq_input_hz, "Hz", constants.DEFAULT_FREQ_UNIT
    )
    
    sse_update_rate = int(
        1.0 / (FIELD_INPUTS.recv_buffer_input / FIELD_INPUTS.sample_freq_input_hz)
    )
    
    waterfall_history_num_samples = int(
        FIELD_INPUTS.waterfall_duration_input * FIELD_INPUTS.sample_freq_input_hz
    )
    waterfall_history_depth_size = waterfall_history_num_samples // FIELD_INPUTS.recv_buffer_input
    return render_template(
        'index.html',
        carr_freq_input_value=carr_freq_input_value,
        sample_freq_input_value=sample_freq_input_value,
        gain_input_value=FIELD_INPUTS.gain_input,
        recv_buffer_input_value=FIELD_INPUTS.recv_buffer_input,
        waterfall_duration_input_value=FIELD_INPUTS.waterfall_duration_input,
        waterfall_nfft_input_value=FIELD_INPUTS.waterfall_nfft_input,
        sse_update_rate = sse_update_rate,
        waterfall_width=FIELD_INPUTS.waterfall_nfft_input,
        waterfall_height=waterfall_history_depth_size,
        waterfall_colorbar_zmin=constants.WATERFALL_FULLSCALE_MIN_POWER_DB,
    )


@APP.route('/events')
def sse_data():
    field_inputs = FIELD_INPUTS
    response = Response(
        stream_with_context(
            waterfall_generator(
                PulsedToneGenerator(
                    carrier_freq_hz=field_inputs.carr_freq_input_hz,
                    sample_rate_hz=field_inputs.sample_freq_input_hz,
                    gain_db=field_inputs.gain_input,
                    buffer_size=field_inputs.recv_buffer_input,
                ),
                waterfall_duration_sec=field_inputs.waterfall_duration_input,
                fft_size=field_inputs.waterfall_nfft_input
            )
        ), 
        mimetype="text/event-stream"
    )
    
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    APP.run(debug=True)
