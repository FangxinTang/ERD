from typing import List, Optional
from datetime import date, time, datetime
from sqlalchemy import create_engine, Integer, String, ForeignKey, Column, Table, DateTime
from sqlalchemy.orm import declarative_base, relationship, Mapped, sessionmaker, mapped_column

# Database connection and session creation
engine = create_engine('postgresql://postgres:postgres@localhost/SIST')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()





class Tour(Base):
    __tablename__ = 'tours'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(400))
    len_in_hours: Mapped[int] = mapped_column(nullable=False)
    fee: Mapped[float] = mapped_column(nullable=False)
    # Tour - Test: 1-m
    tests: Mapped[List["Test"]] = relationship(back_populates="tour")
    # Tour- TourLocation:1-m
    locations:Mapped[List["TourLocation"]]=relationship(back_populates="tour")
    # Tour-Outing: 1-many
    outings:Mapped[List["Outing"]]=relationship(back_populates="tour")


class Test(Base):
    __tablename__ = 'tests'
    id: Mapped[int] = mapped_column(primary_key=True)
    qualification: Mapped[str] = mapped_column(nullable=False)
    # Tour - Test: 1-m
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"))
    tour:Mapped["Tour"] = relationship(back_populates="tests")
    # Test-GuideWithTest:1-m
    guides_with_tests:Mapped[List["GuideWithTest"]] = relationship(back_populates="test")

class Guide(Base):
    __tablename__ = 'guides'
    employee_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    home_addr: Mapped[str] = mapped_column(String(150), nullable=False)
    date_hired: Mapped[date] = mapped_column(nullable=False)
    # Guide - GuideWithTest:1-m
    guides_with_tests:Mapped[List["GuideWithTest"]]=relationship(back_populates="guide")

class GuideWithTest(Base):
    __tablename__ = 'guides_with_tests'
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('guides.employee_id'))
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    date_completed: Mapped[date] = mapped_column(nullable=False)
    # Guide - GuideWithTest:1-m
    guide:Mapped["Guide"]=relationship(back_populates="guides_with_tests")
    # GuideWithTest - Test:m-1
    test:Mapped['Test']=relationship(back_populates="guides_with_tests")
    # Outing - guide with test:many-1
    outings:Mapped[List['Outing']]=relationship(back_populates="guide_with_test")



class Location(Base):
    __tablename__ = 'locations'
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    location_type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    # location(parent):tour location(children): one to many 
    tour_locations : Mapped[List['TourLocation']] = relationship(back_populates="location")


class TourLocation(Base):
    __tablename__ = 'tour_locations'
    tour_id: Mapped[int] = mapped_column(ForeignKey('tours.id'),primary_key=True)
    Location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'),primary_key=True)
    visit_order: Mapped[int] = mapped_column(nullable=False)
    # Tour- TourLocation:1-m
    tour: Mapped['Tour'] = relationship(back_populates='locations')
    # location(parent)- tourlocations(children): one-to-many
    location: Mapped['Location'] = relationship(back_populates="tour_locations")


# Tourist and Outing - many to many
outing_tourist_association = Table(
    "outing_tourist",
    Base.metadata,
    Column("tourist_id", ForeignKey("tourists.id"),primary_key=True),
    Column("outing_id", ForeignKey("outings.id"),primary_key=True),
)




class Tourist(Base):
    __tablename__ = 'tourists'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
#     # relationship with Outing: many to many
    outings: Mapped[List[Outing]] = relationship(secondary='outing_tourist_association',back_populates="tourists")

class Outing(Base):
    __tablename__ = 'outings'
    id: Mapped[int] = mapped_column(primary_key=True)
    tour_id:Mapped[int]=mapped_column(ForeignKey('tours.id'))
    guide_with_test_id:Mapped[int]=mapped_column(ForeignKey('guides_with_tests.id'))
    date_and_time: Mapped[datetime] = mapped_column(nullable=False)
#     # Tour-Outing: 1-many
    tour: Mapped['Tour'] = relationship(back_populates="outings")
    # Outing-guide with test:many-1
    guide_with_test: Mapped['GuideWithTest'] = relationship(back_populates="outings")
    #     # relationship with Outing: many to many
    tourists: Mapped[List[Tourist]] = relationship(secondary='outing_tourist_association',back_populates="outings")


Base.metadata.create_all(engine)