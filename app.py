from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

vegetables = {
    "Brinjal": {"quantity": 10, "price": 40, "cost": 20},
    "Tomato": {"quantity": 15, "price": 25, "cost": 15},
    "Onion": {"quantity": 20, "price": 15, "cost": 10}
}

total_amount = 0

@app.route('/')
def home():
    return render_template('index.html', vegetables=vegetables)

@app.route('/buy', methods=['POST'])
def buy():
    global total_amount
    item = request.form['item']
    quantity = float(request.form['quantity'])
    
    if item in vegetables:
        available_quantity = vegetables[item]['quantity']
        if quantity <= available_quantity:
            amount = quantity * vegetables[item]['price']
            total_amount += amount
            vegetables[item]['quantity'] -= quantity
            return render_template('checkout.html', item=item, quantity=quantity, amount=amount, total_amount=total_amount)
        else:
            return f"Sorry, we only have {available_quantity} kgs of {item}."
    else:
        return "Invalid item selected."

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', total_amount=total_amount)

@app.route('/close')
def close_shop():
    return render_template('close_shop.html', vegetables=vegetables)

@app.route('/report')
def report():
    total_cost = sum(veg['cost'] for veg in vegetables.values())
    profit = total_amount - total_cost
    return render_template('report.html', vegetables=vegetables, profit=profit)

if __name__ == "__main__":
    app.run(debug=True)
