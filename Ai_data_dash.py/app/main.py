from flask import Flask, render_template, request, jsonify
import pandas as pd
import ollama

app = Flask(__name__, template_folder="templates", static_folder="static")

df_global = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    global df_global

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    try:

        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
            df = pd.read_excel(file)

        else:
            return jsonify({"error": "Unsupported file format"})

        df_global = df

        rows = df.shape[0]
        columns = df.shape[1]
        missing = int(df.isnull().sum().sum())

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            labels = df.index.astype(str).tolist()[:10]
            values = df[col].fillna(0).tolist()[:10]
        else:
            labels = ["A","B","C"]
            values = [5,10,15]

        return jsonify({
            "rows": rows,
            "columns": columns,
            "missing": missing,
            "labels": labels,
            "values": values
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/ai_insights")
def ai_insights():

    global df_global

    if df_global is None:
        return jsonify({"insights":"Upload dataset first"})

    summary = df_global.describe().to_string()

    prompt = f"""
    Analyze this dataset summary and give business insights:

    {summary}

    Explain trends and key observations.
    """

    response = ollama.chat(
        model="gemma3",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({"insights":response["message"]["content"]})


@app.route("/ask_ai", methods=["POST"])
def ask_ai():

    data = request.json
    question = data["question"]

    summary = df_global.describe().to_string()

    prompt = f"""
    Dataset summary:

    {summary}

    User Question: {question}

    Answer using dataset context.
    """

    response = ollama.chat(
        model="gemma3",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({"answer":response["message"]["content"]})


if __name__ == "__main__":
    app.run(debug=True)