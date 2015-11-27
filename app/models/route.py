from app.models import base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import(
	Column,
        String,
	INTEGER,
	Boolean,
)

class Route(base):
	__tablename__='route'
	
	prefix='RI'

	time= Column
	route_type=Column(String(32))
	accessibility=Column(INTEGER)
	name=Column(String(32))
	origin_point=Column(String(55))
	destination_point=Column(String(55))
	

	define __init__(self,time,route_type,accessibility,name,origin_point,destination_point):
		self.time=time
		self.route_type=route_type
		self.accessibility=accessibility,
		self.name=name

		self.init()

	@classmethod
	def get_all_routes(cls):
		return cls.get_routes_query().all()

		
	
