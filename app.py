"""Web interface for the calculator using Flask."""

from flask import Flask, request, render_template_string
import calculator


app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Calculator</title>
<h1>Calculator</h1>
<form method="post" action="/calculate">
  <input type="number" step="any" name="x" placeholder="First number" required>
  <select name="operation">
    <option value="add">+</option>
    <option value="sub">-</option>
    <option value="mul">*</option>
    <option value="div">/</option>
  </select>
  <input type="number" step="any" name="y" placeholder="Second number" required>
  <button type="submit">Compute</button>
</form>
{% if result is not none %}
<p>Result: {{ result }}</p>
{% endif %}
{% if error %}
<p style="color: red;">Error: {{ error }}</p>
{% endif %}
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE, result=None, error=None)


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        x = float(request.form["x"])
        y = float(request.form["y"])
        op = request.form["operation"]
        func = {
            "add": calculator.add,
            "sub": calculator.subtract,
            "mul": calculator.multiply,
            "div": calculator.divide,
        }[op]
        result = func(x, y)
        return render_template_string(HTML_TEMPLATE, result=result, error=None)
    except Exception as exc:
        return render_template_string(HTML_TEMPLATE, result=None, error=str(exc)), 400


if __name__ == "__main__":
    app.run(debug=True)
