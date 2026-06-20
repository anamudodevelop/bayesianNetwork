from flask import Flask, render_template, request
from pgmpy.readwrite import BIFReader
from pgmpy.inference import VariableElimination

app = Flask(__name__)
reader = BIFReader('C:\\Users\\User\\Desktop\\MASTERS WLV\\Application of Intelligent agent\\Assignment\\project\\engine_fault_model.bif')
model = reader.get_model()
infer = VariableElimination(model)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Example prediction logic - replace with actual implementation
    rpm = request.form["rpm"]
    oil = request.form["oil"]
    coolant = request.form["coolant"]
    intakepressure = request.form["intakepressure"]
    intaketemperature = request.form["intaketemperature"]
    transmissionoilpressure = request.form["transmissionoilpressure"]
    transmissionoiltemperature = request.form["transmissionoiltemperature"]
    machinespeed = request.form["machinespeed"]
    result = infer.query(
        variables=["status"],
        evidence={
            "RPM_Level": rpm,
            "Engine_Oil_Press_level": oil,
            "Engine_Coolant_Temp_level": coolant,
            "Engine_Intake_Manifold_Press_level": intakepressure,
            "Engine_Intake_Manifold_Temp_level": intaketemperature,
            "Transmission_Oil_Press_level": transmissionoilpressure,
            "Transmission_Oil_Temp_level": transmissionoiltemperature,
            "Machine_Speed_Level": machinespeed
        }
    )
    fault_index = list(
        model.get_cpds("status").state_names["status"]
    ).index("Fault")

    fault_probability = float(
        result.values[fault_index]
    )

    return {
        "fault_probability": round(
            fault_probability,
            4
        )
    }

if __name__ == "__main__":
    app.run(debug=True)
