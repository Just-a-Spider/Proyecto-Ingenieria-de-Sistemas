# Pasos para replicar

## Get the repo
```bash
git clone https://github.com/Just-a-Spider/Proyecto-Ingenieria-de-Sistemas.git
cd Proyecto-Ingenieria-de-Sistemas
```

## Crear entorno e Instalar dependencias
Windows
```bash
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Linux
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Crear el archivo .env
Para esto es solo seguir las instrucciones de ".env.example"

## Crear y correr las migraciones
Para correr las migraciones a la BD configurada en el archivo ".env"
```bash
flask db upgrade
```

Si se quiere hacer desde 0
```bash
flask db init
flask db migrate -m "Mensaje de Migración"
flask db upgrade
```

## Exportar variables y correr
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

