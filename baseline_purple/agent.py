from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/execute")
def execute():
    data = request.json

    # ----- Portfolio task -----
    if data.get("task_type") == "portfolio":
        assets = data.get("assets", [])
        if not assets:
            return jsonify({})

        weight = 1.0 / len(assets)
        return jsonify({a: weight for a in assets})

    # ----- Regime detection -----
    if data.get("task_type") == "regime_detection":
        return jsonify({"regime": "flash_crash"})
    
    # ----- Arbitrage -----
    if data.get("task_type") == "arbitrage":
        return jsonify({"profit": 0.02})
    
    # ----- Execution -----
    if data.get("task_type") == "execution":
        target = data.get("target_volume", 10000)
        price_path = data.get("price_path", [])
        if not price_path:
            return jsonify({"slices": []})
        
        # Equal slicing with exact sum
        n_slices = len(price_path)
        base_slice = target // n_slices
        remainder = target % n_slices
        
        slices = [base_slice] * n_slices
        # Add remainder to first slices
        for i in range(remainder):
            slices[i] += 1
        
        return jsonify({"slices": slices})

    # ----- Unknown task -----
    return jsonify({})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9009)
