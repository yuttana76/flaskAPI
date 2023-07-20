from flask import Flask,jsonify,request
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy

# from .model.expense import Expense, ExpenseSchema
# from .model.income import Income, IncomeSchema
# from .model.transaction_type import TransactionType

app=Flask(__name__)

# transactions = [
#     Income('Salary', 5000),
#     Income('Dividends', 200),
#     Expense('pizza', 50),
#     Expense('Rock Concert', 100)
# ]

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///city.db"
db = SQLAlchemy(app)

api=Api(app)

class CityModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    temp=db.Column(db.String(100),nullable=False)
    weather=db.Column(db.String(100),nullable=False)
    populate=db.Column(db.String(100),nullable=False)
    region=db.Column(db.String(100),nullable=False)

    # def __repr__(self):
    #     return f"City(name={self.name},temp{self.temp},weather={self.weather},populate={self.populate})"

db.create_all()

resource_field ={
    "id":fields.Integer,
    "name":fields.String,
    "temp":fields.String,
    "weather":fields.String,
    "populate":fields.String,
    "region":fields.String,
}

# Add request parser
city_add_args = reqparse.RequestParser()
city_add_args.add_argument("name",type=str,required=True,help="Please input name.")
city_add_args.add_argument("temp",type=str,required=True,help="Please input temp.")
city_add_args.add_argument("weather",type=str,required=True,help="Please input weather.")
city_add_args.add_argument("populate",type=str,required=True,help="Please input populate.")
city_add_args.add_argument("region",type=str,required=True,help="Please input region.")

#Update request parser
city_update_args = reqparse.RequestParser()
city_update_args.add_argument("name",type=str,help="Please input name.")
city_update_args.add_argument("temp",type=str,help="Please input temp.")
city_update_args.add_argument("weather",type=str,help="Please input weather.")
city_update_args.add_argument("populate",type=str,help="Please input populate.")
city_update_args.add_argument("region",type=str,help="Please input region.")

# design
class WeatherCity(Resource):
    @marshal_with(resource_field)
    def get(self,city_id):
        city = CityModel.query.filter_by(id=city_id).first()
        if not city:
            abort(404,message="Not fond city id:{}".format(city_id))

        return city
    
    @marshal_with(resource_field)
    def post(self,city_id):

        # Check id have?
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409,message="Already have city id:{}".format(city_id))

        args = city_add_args.parse_args()
        city= CityModel(id=city_id,name=args["name"],temp=args["temp"],weather=args["weather"],populate=args["populate"],region=args["region"])
        db.session.add(city)
        db.session.commit()
        return city,201
    
    @marshal_with(resource_field)
    def patch(self,city_id):
        # Check id have?
        args = city_update_args.parse_args()
        city = CityModel.query.filter_by(id=city_id).first()
        if not city:
            abort(404,message="Not fond city id:{}".format(city_id))

        if args["name"]:
            city.name=args["name"]  
        if args["temp"]:
            city.temp=args["temp"]
        if args["weather"]:
            city.weather=args["weather"]
        if args["populate"]:
            city.populate=args["populate"]
        if args["region"]:
            city.region=args["region"]

        db.session.commit()
        return city

#call
api.add_resource(WeatherCity,"/weather/<int:city_id>")

# Sample2
@app.route('/city')
@marshal_with(resource_field)
def get_incomes():
    city = CityModel.query.all() #OK
    # city = CityModel.query.all()[0:]  #OK
    return city,200

# # Sample3
# @app.route('/incomes')
# def get_incomes():
#     schema = IncomeSchema(many=True)
#     incomes = schema.dump(
#         filter(lambda t: t.type == TransactionType.INCOME, transactions)
#     )
#     return jsonify(incomes)


# @app.route('/incomes', methods=['POST'])
# def add_income():
#     income = IncomeSchema().load(request.get_json())
#     transactions.append(income)
#     return "", 204


# @app.route('/expenses')
# def get_expenses():
#     schema = ExpenseSchema(many=True)
#     expenses = schema.dump(
#         filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
#     )
#     return jsonify(expenses)


# @app.route('/expenses', methods=['POST'])
# def add_expense():
#     expense = ExpenseSchema().load(request.get_json())
#     transactions.append(expense)
#     return "", 204


if __name__ == "__main__":
    app.run(debug=True)