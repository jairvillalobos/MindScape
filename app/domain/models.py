from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    registration_date = Column(DateTime)

    entries = relationship("Entry", back_populates="user")
    configuration = relationship("Configuration", uselist=False, back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    customization = relationship("Customization", uselist=False, back_populates="user")
    emotion_history = relationship("EmotionHistory", back_populates="user")

class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    text = Column(String)
    image = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="entries")
    emotions = relationship("EntryEmotion", back_populates="entry")
    advanced_analysis = relationship("AdvancedAnalysis", uselist=False, back_populates="entry")

class EntryEmotion(Base):
    __tablename__ = "entry_emotion"

    entry_id = Column(Integer, ForeignKey("entries.id"), primary_key=True)
    emotion_id = Column(Integer, ForeignKey("emotions.id"), primary_key=True)
    intensity = Column(Integer)

    entry = relationship("Entry", back_populates="emotions")
    emotion = relationship("Emotion")

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reminder_frequency = Column(Integer)
    notifications_enabled = Column(Boolean)

    user = relationship("User", back_populates="configuration")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="notifications")

class AdvancedAnalysis(Base):
    __tablename__ = "advanced_analysis"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id"))
    result = Column(String)

    entry = relationship("Entry", back_populates="advanced_analysis")

class Customization(Base):
    __tablename__ = "customization"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class EmotionHistory(Base):
   __tablename__= "emotion_history"
   
   id=Column(Integer, primary_key=True,index=True)
   user_id=Column(Integer,ForeignKey('users.id'))
   emotion_id=Column(Integer,ForeignKey('emotions.id'))
   timestamp=Column(DateTime)
   intensity=Column(Integer)

   user=relationship('User',back_populates='emotion_history')
   emotion=relationship('Emotion')
