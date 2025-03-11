from typing import Any, Dict
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
	pass

class SQLab:

	db_url : str
	engine = None
	Session : sessionmaker
	
	@classmethod
	def connect(cls, db_url):
		cls.db_url = db_url
		cls.engine = create_engine(db_url, poolclass=NullPool, pool_pre_ping=True)
		cls.Session = sessionmaker(bind=cls.engine)()
		Base.metadata.create_all(cls.engine)

	@classmethod
	def select_from(cls, 
				 _from : Base, 
				 _select : Base | Any = None, 
				 _where : Any = None, _orderby = None, 
				 _limit : int = None, 
				 is_query : bool = False) -> Any | None:
		try:
			select = _select if isinstance(_select, list) or _select is None else [_select]
			with cls.Session as session:
				if select is not None:
					result_query = session.query(*select)
				else:
					result_query = session.query(_from)
			
			if _where is not None:
				result_query = result_query.filter(_where)

			if _orderby is not None:
				if not isinstance(_orderby, list):
					orderby = [_orderby]
				else:
					orderby = _orderby
				
				if len(orderby) > 0:
					result_query = result_query.order_by(*orderby)

			if _limit is not None:
				result_query = result_query.limit(_limit)
			
			if is_query:
				return result_query

			return result_query.all()

		except Exception as e:
			print("select - ", e)
			return None

	@classmethod
	def create(cls, new_object : Base) -> None:
		try:
			unique_fields = []
			for field in new_object.__table__.__dict__["_columns"]:
				if field.primary_key or field.unique:
					unique_fields.append(field)

			check_object_in_db = cls.select_from(
				_from = new_object.__table__, 
				_where = or_(field == getattr(new_object,field.name) for field in unique_fields)
			)

			if check_object_in_db == []:
				with cls.Session as session:
					try:
						session.add(new_object)

					except Exception as e:
						session.rollback()

					else:
						session.commit()

		except Exception as e:
			print("create - ", e)

	@classmethod
	def update(cls, table_name : Base, new_values : Dict[str, Any], _where : Any) -> None:
		with cls.Session as session:
			try:
				objects_to_update = cls.select_from(_from=table_name, _where=_where, is_query=True)
				objects_to_update.update(new_values)

			except Exception as e:
				print("update - ", e)
				session.rollback()

			else:
				session.commit()


	@classmethod
	def delete(cls, table_name : Base, _where : Any = None) -> None:
		with cls.Session as session:
			try:
				objects_to_delete = cls.select_from(_from = table_name, _where=_where, is_query=True)
				objects_to_delete.delete()

			except Exception as e:
				print("delete - ", e)
				session.rollback()

			else:
				session.commit()