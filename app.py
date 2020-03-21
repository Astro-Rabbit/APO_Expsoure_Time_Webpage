from flask import Flask, request, render_template, Response
from APOExptime import Sky, Target, Instrument, Observation, makeplots
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import random
import io

app = Flask(__name__)


@app.route('/')
def get_parameters():
    return render_template('input.html')

@app.route('/greet')
def my_form_post():
    instrument_name = str(request.args.get('instrument', 'World'))
    mag = float(request.args['mag'])
    temp = float(request.args['temp'])
    seeing = float(request.args['seeing'])
    SN = int(request.args['SN'])

    inst = Instrument(instrument_name)
    sky = Sky(seeing=seeing)
    star = Target(mag, 'VEGAMAG', [4700,6900], temp=temp)
    ob = Observation(star, sky, inst)
    ob.TimefromSN(SN)
    fig = makeplots(ob, 'Time')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



if __name__ == '__main__':
    app.run()
