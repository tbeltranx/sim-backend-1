from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import plotly.graph_objs as go
from plotly.io import to_json

app = Flask(__name__)
CORS(app)

# Función de predicción
def predict_lnS(temperature, pressure, LHSV, H2_HC):
    lnS = np.log(temperature) * 0.2 - np.log(pressure) * 0.3 + np.log(LHSV) * 0.5 - np.log(H2_HC) * 0.1
    return lnS

# Generar la gráfica
def generate_plot(temperature, pressure, LHSV, H2_HC):
    prediction = predict_lnS(temperature, pressure, LHSV, H2_HC)

    fig = go.Figure()
    temp_values = np.linspace(323.4, 366.6, 100)
    fig.add_trace(go.Scatter(
        x=temp_values, 
        y=predict_lnS(temp_values, pressure, LHSV, H2_HC), 
        mode='lines',
        name='ln(S) vs. Temperatura'
    ))
    fig.add_trace(go.Scatter(
        x=[temperature, temperature], 
        y=[-1, 1], 
        mode='lines', 
        line=dict(color='red', dash='dot'),
        name='Temperatura seleccionada'
    ))
    
    fig.update_layout(
        title="Simulador de Comportamiento",
        xaxis_title="Temperatura",
        yaxis_title="ln(S)"
    )
    return to_json(fig), prediction

@app.route('/api/plot', methods=['POST'])
def plot():
    data = request.json
    temperature = data.get('temperature', 345.0)
    pressure = data.get('pressure', 50.5)
    LHSV = data.get('LHSV', 1.9)
    H2_HC = data.get('H2_HC', 3234)

    # Generar gráfica y obtener predicción
    plot_json, prediction = generate_plot(temperature, pressure, LHSV, H2_HC)

    # Incluir predicción en la respuesta
    return jsonify({
        "plot": plot_json,
        "prediction": prediction
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
