# MindScape

MindScape es un software de mapeo emocional que utiliza el análisis del lenguaje natural y el reconocimiento facial para rastrear las emociones del usuario a lo largo del tiempo. El objetivo es ayudar a los usuarios a entender sus patrones emocionales y a identificar desencadenantes o tendencias. Esto podría ser especialmente útil en el contexto de la salud mental, ayudando a los usuarios a manejar el estrés, la ansiedad, etc. El software se desarrollará como una aplicación web utilizando Python y FastAPI para el backend, y se almacenará la información del usuario en una base de datos PostgreSQL. La privacidad y la seguridad de los datos del usuario son una prioridad, por lo que se implementarán medidas sólidas para proteger la privacidad y seguridad del usuario.

## Estructura del Proyecto

El proyecto sigue la Arquitectura de Cebolla y tiene la siguiente estructura de carpetas:

```
MindScape/
├── app/
│   ├── env/
│   ├── domain/
│   │   ├── models.py
│   │   └── services.py
│   ├── application/
│   │   ├── interfaces.py
│   │   └── services.py
│   ├── infrastructure/
│   │   ├── database.py
│   │   └── repositories.py
│   └── api/
│       └── routers/
│           ├── users.py
│           ├── emotions.py
│           └── entries.py
├── main.py
└── README.md
```

## Base de datos

El proyecto utiliza una base de datos PostgreSQL para almacenar los datos del usuario y los resultados del análisis de emociones.

### Entidades

- **Usuario**: Representa a un usuario individual de la aplicación. Tiene atributos como nombre, correo electrónico, contraseña y fecha de registro.
- **Emocion**: Representa una emoción específica que puede ser detectada por la aplicación. Tiene atributos como nombre y descripción.
- **Entrada**: Representa una entrada en el diario emocional del usuario. Tiene atributos como fecha y hora, texto, imagen y emoción detectada.
- **Configuracion**: Representa la configuración del usuario para la aplicación. Tiene atributos como la frecuencia con la que se le recuerda al usuario que haga una entrada en su diario emocional y si desea recibir notificaciones.

### Relaciones

- **Usuario-Entrada**: Cada entrada está asociada a un usuario en particular.
- **Entrada-Emocion**: Cada entrada está asociada a una o más emociones detectadas.
- **Usuario-Configuracion**: Cada usuario tiene una configuración asociada.

## Instalación

Instrucciones para instalar el proyecto.

## Uso

Instrucciones para usar el proyecto.
