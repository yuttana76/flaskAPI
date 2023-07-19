from flask import Flask
# from flask_restful import Api,Resource,abort
from flask_restful import Api,Resource,abort
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///city.db"
api=Api(app)

class CityModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    temp=db.Column(db.String(100),nullable=False)
    weather=db.Column(db.String(100),nullable=False)
    populate=db.Column(db.String(100),nullable=False)

    # def __repr__(self):
    #     return f"City(name={self.name},temp{self.temp},weather={self.weather},populate={self.populate})"

db.create_all()

mycity={
    1:{"name":"chonburi","weather":"Cold","populate":100},
    2:{"name":"Bangkok","weather":"Cloud","populate":200},
    3:{"name":"Chiangmai","weather":"So hot","populate":300},
}

# Validate
def notFoundCityId(cityid):
    if cityid not in mycity:
        abort(404,message="not fond city id:{}".format(cityid))

# design
class WeatherCity(Resource):
    def get(self,cityid):
        notFoundCityId(cityid)
        return mycity[cityid]
    
    def post(self,name):
        return {"data":"Data weather post."+name}

#call
api.add_resource(WeatherCity,"/weather/<int:cityid>")

if __name__ == "__main__":
    app.run(debug=True)