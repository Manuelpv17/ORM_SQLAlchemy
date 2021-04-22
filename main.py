from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50))
    assignment = relationship("Assignment", back_populates="student")


class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('student.id'))
    project_id = Column(Integer, ForeignKey('project.id'))
    student = relationship("Student", back_populates="assignment")
    project = relationship("Project", back_populates="assignment")


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    weight = Column(Integer)
    advanceTask = Column(Boolean)
    assignment = relationship("Assignment", back_populates="project")


engine = create_engine("mysql+mysqldb:pass//root@localhost/db")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

newUser = User(name="Manuel", email="manuel@manuel.com")
session.add(newUser)

newProject = Project(name="SQL", weight=1, advanceTask=True)
newProject = Project(name="Alchemy", weight=2, advanceTask=True)
session.add(newProject)
session.commit()

newAssignment = Assignment(user_id=newUser.id, project_id=newProject.id)
session.add(newAssignment)
session.commit()

our_user = session.query(User).filter_by(name=newUser.name).first()
print(our_user.assignment[0].user.name)

our_assignment = session.query(Assignment).filter_by(
    id=newAssignment.id).first()
print(our_assignment.user.name)
print(our_assignment.project.name)


session.close()
