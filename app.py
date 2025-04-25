from flask import Flask, request, render_template, flash, redirect, url_for
from markupsafe import escape
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

MINIMUM_WAGES = {
    'India': 150,
    'Latvia': 620,
    'Germany': 1980,
    'USA': 1270,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        income_str = request.form.get('income', '').strip()
        country = request.form.get('country')
        errors = []

        # Validate income
        try:
            income = float(income_str)
            if income < 0:
                errors.append('Income must be a non-negative number.')
        except ValueError:
            errors.append('Please enter a valid numeric income.')

        # Validate country
        if country not in MINIMUM_WAGES:
            errors.append('Please select a valid country.')

        if errors:
            for err in errors:
                flash(err, 'error')
            return redirect(url_for('index'))

        # Logic
        min_wage = MINIMUM_WAGES[country]
        ratio = income / min_wage

        if ratio < 0.5:
            comment = 'Below half the minimum wage; consider boosting your income.'
        elif ratio < 1.0:
            comment = 'Below the minimum wage; watch your expenses closely.'
        elif ratio < 1.5:
            comment = 'Slightly above minimum wage; try to save 10–20%.'
        else:
            comment = 'Above minimum wage; great, time to plan a balanced budget!'

        # Budget logic
        budget_percent = {}
        if 0.5 <= ratio < 5:
            if ratio < 1.5:
                budget_percent = {
                    "Rent": 0.40,
                    "Groceries": 0.20,
                    "Transport": 0.10,
                    "Electricity etc.": 0.10,
                    "Other bills": 0.10,
                    "Entertainment": 0.00,
                    "Savings": 0.00,
                    "Relationship nonsense": 0.10,
                }
            else:
                budget_percent = {
                    "Rent": 0.30,
                    "Groceries": 0.15,
                    "Transport": 0.05,
                    "Electricity etc.": 0.05,
                    "Other bills": 0.03,
                    "Savings": 0.30,
                    "Entertainment": 0.10,
                    "Relationship nonsense": 0.02,
                }

        # Convert percentages to actual amounts
        budget_amounts = {k: round(income * v, 2) for k, v in budget_percent.items()}

        return render_template(
            'result.html',
            country=escape(country),
            income=round(income, 2),
            min_wage=round(min_wage, 2),
            ratio=round(ratio, 2),
            comment=comment,
            budget=budget_amounts
        )

    return render_template('index.html', countries=sorted(MINIMUM_WAGES.keys()))

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

