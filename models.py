from database import Base, Column, Integer, String, Boolean

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    complete = Column(Boolean, default=False)