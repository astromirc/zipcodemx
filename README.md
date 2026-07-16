**ZipCodeMX:** API REST para consultar códigos postales de México.

Este proyecto expone una API que permite buscar un código postal y obtener todos los datos referentes a él, como la colonia, estado, municipio, entre otros.

## Requisitos

- Docker

## Instalación (Build de contenedores)

```bash
# Desarrollo
$ docker compose -f local.yml build

# Producción
$ docker compose -f production.yml build
```

## Configuración

1. Copiar el archivo `env.template` y guardarlo con el nombre `.env`.
2. Ajustar las variables de entorno del archivo `.env` según sea necesario.

> **Nota:** En modo de desarrollo, define las siguientes variables de entorno en tu archivo `.env` para que la aplicación pueda conectarse a PostgreSQL:
>
> ```env
> POSTGRES_HOST=postgres
> POSTGRES_PORT=5432
> POSTGRES_USER=zipcodemx
> POSTGRES_PASSWORD=zipcodemx
> POSTGRES_DB=zipcodemx
> ```

3. Aplicar las migraciones pendientes (ver sección de comandos).


## Comandos de la aplicación

```bash
# Iniciar aplicación
$ docker compose -f [compose_file].yml up

# Detener aplicación
$ docker compose -f [compose_file].yml down

# Generar nueva migración
$ docker compose -f [compose_file].yml run --rm backend migration generate "nombre de la migración"

# Aplicar migraciones pendientes
$ docker compose -f [compose_file].yml run --rm backend migration upgrade

# Ejecutar pruebas
$ docker compose -f [compose_file].yml run --rm backend tests

# Formatear y checar el código
$ docker compose -f [compose_file].yml run --rm backend linter
```

> **Nota:** Remplaza `[compose_file]` por `local` o `production`, dependiendo del entorno donde se ejecute la aplicación.

## Conexión a PostgreSQL desde la máquina anfitriona

Puedes conectarte a PostgreSQL desde tu máquina anfitriona utilizando `localhost` como host. Esto permite acceder a la base de datos mediante herramientas como gestores de bases de datos o clientes SQL.

## Stack Tecnológico

Principales tecnologías utilizadas en el proyecto:

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Migraciones**: Alembic
- **Base de datos**: PostgreSQL
- **Testing**: Pytest
