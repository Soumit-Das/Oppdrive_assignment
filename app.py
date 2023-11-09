import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json 
from sqlalchemy import text

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Soumit'


app.config['SECRET_KEY'] = 'your-secret-key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:SOUMIT4119@localhost:3306/travel_planner_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)
CORS(app)




class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    itinerary = db.relationship('Itinerary', backref='destination', uselist=False, lazy=True)

    expenses = db.relationship('Expense', backref='destination', lazy=True)

    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location


class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), unique=True, nullable=False)
    activities = db.Column(db.Text, nullable=False)

    expenses = db.relationship('Expense', backref='itinerary', lazy=True)

    def __init__(self, destination_id, activities):
        self.destination_id = destination_id
        self.activities = activities




class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    expenses = db.Column(db.Text, nullable=False)

    def __init__(self, destination_id, itinerary_id, expenses):
        self.destination_id = destination_id
        self.itinerary_id = itinerary_id
        self.expenses = expenses




with app.app_context():
    db.create_all()





@app.route('/addDestinations', methods=['POST'])
def create_destination():
    data = request.get_json()
    name = data['name']
    description = data['description']
    location = data['location']

    new_destination = Destination(name=name, description=description, location=location)

    try:
        db.session.add(new_destination)
        db.session.commit()
        return jsonify({'message': 'Destination created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create destination', 'details': str(e)})



@app.route('/getAlldestinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    destination_list = []
    for dest in destinations:
        destination_list.append({'id': dest.id, 'name': dest.name, 'description': dest.description, 'location': dest.location})
    return jsonify(destination_list)



@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        return jsonify({'id': destination.id, 'name': destination.name, 'description': destination.description, 'location': destination.location})
    else:
        return jsonify({'error': 'Destination not found'})



@app.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id)

    if destination is not None:
        destination.name = data['name']
        destination.description = data['description']
        destination.location = data['location']

        try:
            db.session.commit()
            return jsonify({'message': 'Destination updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update destination', 'details': str(e)})
    else:
        return jsonify({'error': 'Destination not found'})


@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)

    if destination is not None:
        try:
            db.session.delete(destination)
            db.session.commit()
            return jsonify({'message': 'Destination deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to delete destination', 'details': str(e)})
    else:
        return jsonify({'error': 'Destination not found'})








@app.route('/itineraries/<int:destination_id>/activities', methods=['POST'])
def create_activity(destination_id):
    data = request.get_json()
    destination = db.session.query(Destination).get(destination_id)

    if destination is not None:
        activities = data.get('activities', [])

        activities_text = json.dumps(activities)

        new_itinerary = Itinerary(destination_id=destination.id, activities=activities_text)

        try:
            db.session.add(new_itinerary)
            db.session.commit()
            return jsonify({'message': 'Activity added to the itinerary successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to add activity to the itinerary', 'details': str(e)})
    else:
        return jsonify({'error': 'Destination not found'})






@app.route('/itineraries/<int:destination_id>/activities', methods=['PUT'])
def update_activities(destination_id):
    data = request.get_json()

    destination = db.session.query(Destination).get(destination_id)

    if destination is not None:
        activities = data.get('activities', [])

        activities_text = json.dumps(activities)

        itinerary = Itinerary.query.filter_by(destination_id=destination_id).first()

        if itinerary:
            itinerary.activities = activities_text
        else:
            new_itinerary = Itinerary(destination_id=destination_id, activities=activities_text)
            db.session.add(new_itinerary)

        try:
            db.session.commit()
            return jsonify({'message': 'Activities updated in the itinerary successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update activities in the itinerary', 'details': str(e)})
    else:
        return jsonify({'error': 'Destination not found'})




@app.route('/itineraries/<int:destination_id>', methods=['DELETE'])
def delete_itinerary(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        itinerary = Itinerary.query.filter_by(destination_id=destination_id).first()

        if itinerary is not None:
            try:
                db.session.delete(itinerary)
                db.session.commit()
                return jsonify({'message': 'Itinerary deleted successfully'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to delete itinerary', 'details': str(e)})
        else:
            return jsonify({'error': 'Itinerary not found'})
    else:
        return jsonify({'error': 'Destination not found'})


@app.route('/itineraries/destination/<int:destination_id>', methods=['GET'])
def get_itinerary_by_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        itinerary = Itinerary.query.filter_by(destination_id=destination_id).first()
        if itinerary:
            return jsonify({'itinerary_id': itinerary.id, 'activities': itinerary.activities})
        else:
            return jsonify({'message': 'Itinerary not found for the destination'})
    else:
        return jsonify({'error': 'Destination not found'})





@app.route('/itineraries/<int:itinerary_id>/expenses', methods=['POST'])
def create_expense_for_itinerary(itinerary_id):
    data = request.get_json()
    
    itinerary = db.session.query(Itinerary).get(itinerary_id)
    
    if itinerary is not None:
        destination_id = itinerary.destination_id
        expenses = data.get('expenses', [])

        expenses_text = json.dumps(expenses)

        new_expense = Expense(destination_id=destination_id, itinerary_id=itinerary_id, expenses=expenses_text)

        try:
            db.session.add(new_expense)
            db.session.commit()
            return jsonify({'message': 'Expense recorded successfully for itinerary'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to record expense for itinerary', 'details': str(e)})
    else:
        return jsonify({'error': 'Itinerary not found'})



@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expense_list = []
    for expense in expenses:

        expense_data = json.loads(expense.expenses)
        for item in expense_data:
            expense_list.append({
                'id': expense.id,
                'description': item.get('description'),
                'category': item.get('category'),
                'amount': item.get('amount')
            })
    return jsonify(expense_list)




@app.route('/expenses/<int:itinerary_id>', methods=['PUT'])
def update_expense(itinerary_id):
    data = request.get_json()

    existing_expense = Expense.query.filter_by(itinerary_id=itinerary_id).first()

    if existing_expense is not None:

        new_expenses = data.get('expenses', [])

        new_expenses_text = json.dumps(new_expenses)

        existing_expense.expenses = new_expenses_text

        try:
            db.session.commit()
            return jsonify({'message': 'Expenses updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update expenses', 'details': str(e)})
    else:
        return jsonify({'error': 'Expense not found'})




@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)

    if expense is not None:
        try:
            db.session.delete(expense)
            db.session.commit()
            return jsonify({'message': 'Expense deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to delete expense', 'details': str(e)})
    else:
        return jsonify({'error': 'Expense not found'})


@app.route('/expenses/itinerary/<int:itinerary_id>', methods=['GET'])
def get_expense_by_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if itinerary is not None:
        expense = Expense.query.filter_by(itinerary_id=itinerary_id).first()
        if expense:
            expenses_data = json.loads(expense.expenses)

            first_expense = expenses_data[0]
            return jsonify({
                'expense_id': expense.id,
                'description': first_expense.get('description', ''),
                'category': first_expense.get('category', ''),
                'amount': first_expense.get('amount', 0.0)
            })
        else:
            return jsonify({'message': 'Expense not found for the itinerary'})
    else:
        return jsonify({'error': 'Itinerary not found'})



@app.route('/expenses/destination/<int:destination_id>', methods=['GET'])
def get_expense_by_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        itinerary = Itinerary.query.filter_by(destination_id=destination_id).first()
        if itinerary:
            expense = Expense.query.filter_by(itinerary_id=itinerary.id).first()
            if expense:
                expenses_data = json.loads(expense.expenses)

                first_expense = expenses_data[0]
                return jsonify({
                    'expense_id': expense.id,
                    'description': first_expense.get('description', ''),
                    'category': first_expense.get('category', ''),
                    'amount': first_expense.get('amount', 0.0)
                })
            else:
                return jsonify({'message': 'Expense not found for the itinerary of the destination'})
        else:
            return jsonify({'message': 'Itinerary not found for the destination'})
    else:
        return jsonify({'error': 'Destination not found'})








if __name__ == '__main__':
    app.run()