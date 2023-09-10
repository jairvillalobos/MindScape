from sqlalchemy import ARRAY, Boolean, Column, Integer, String, DateTime, ForeignKey
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
    emotion_id = Column(Integer, ForeignKey("emotions.id"))

    emotion = relationship("Emotion")

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reminder_frequency = Column(Integer)
    notifications_enabled = Column(Boolean)

    user = relationship("User")


class EntryEmotion(Base):
    __tablename__ = "entry_emotion"

    entrada_id = Column(Integer, ForeignKey("entries.id"), primary_key=True)
    emocion_id = Column(Integer, ForeignKey("emotions.id"), primary_key=True)
    intensidad = Column(Integer)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    mensaje = Column(String)
    fecha_hora = Column(DateTime)

class AdvancedAnalysis(Base):
    __tablename__ = "advanced_analysis"

    id = Column(Integer, primary_key=True, index=True)
    entrada_id = Column(Integer, ForeignKey("entries.id"))
    resultado = Column(String)

class Customization(Base):
    __tablename__ = "customization"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    emociones_rastreadas = Column(ARRAY(String))
    presentacion_datos = Column(String)

class EmotionHistory(Base):
    __tablename__ = "emotion_history"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    emocion_id = Column(Integer, ForeignKey("emotions.id"))
    fecha_hora = Column(DateTime)
    intensidad = Column(Integer)
