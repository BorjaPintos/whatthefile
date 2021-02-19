# whatthefile

Extrae información de archivos pasando varios módulos especializados.
Pensado para forensics o CTFs

# Info shields

![](https://img.shields.io/github/issues-raw/borjapintos/whatthefile)

![](https://img.shields.io/github/last-commit/borjapintos/whatthefile)

![](https://img.shields.io/github/workflow/status/borjapintos/whatthefile/Master%20Workflow)

![](https://img.shields.io/badge/python-3.7-blue)
![](https://img.shields.io/badge/python-3.8-blue)


# Módulos
- **Básico**: Datos específicos del archivo, tipo, tamaño, uid, gid...
- **certificatereader**: Extrae información de los certificados tipo PEM y DER
- **commentExtractor**: Extrae comentarios de ficheros de cógido fuente, html, bash..
- **entropy**: Calcula la entropia de shannon
- **hashes**: Realiza diversos hashes
- **imagerecognitiontensorflow**: reconocimiento de imágenes usando tensorflow.
- **infoextractor**: extracción de emails, urls, iban de ficheros de texto.
- **metadata**: extracción de metadatos con Exiftool
- **ocrtesseract**: Extrae texto que se visualice en imágenes
- **qrbcreader**: Lector de código QR y Códigos de Barras
- **strings**: extracción de strings
- **tikaparser**: Obtención del texto de documentos offimáticos, pdfs...
- **virustotal**: Comprobación de infección enviando el hash a virustotal
- **zipextractor**: Extrae los ficheros de un zip, incluso aplicando fuerza bruta.

Si algún módulo crea nuevos ficheros lo harán en un directorio especial para no modificar evidencias, por ejemplo zipextractor, en ese caso luego cada ficheros será otra vez reanalizado.


# Requistos


- Linux
`pip install -r requirementesunix.txt`
- Windows
`pip install -r requirementeswindows.txt`

- MacOS
`pip install -r requirementesunix.txt`

Se necesita instalar la librería libmagic
En MacOS se puede hacer a través de Homebrew: (tambien sirve para Linux)
https://brew.sh

y una vez instalado:
`brew install libmagic`

### Módulos
Dentro de cada módulo se explican las instrucciones de sus dependencias, por lo general tienen un fichero requirements.txt

`pip install -r requirements.txt`

Algunos necesitan instalar algun software adicional de sistema operativo. Por ejemplo, exiftools

### Salidas disponibles

Existen varios tipos de salida del programa para obtener los resultados:

- **print**: salida normal por pantalla
- **file**: volcado a un fichero
- **list**: el resultado se mantiene en un objecto lista, ideal para exportar a otra librería
- **elasticsearch**: los resultados se envían a un elasticsearch o opendistro

### Requisitos para servidor

`pip install -r requirementsweb.txt`

# Ejecución

## Terminal
### Configuración

Todas las opciones están en el fichero `whatthefile.ini`

### Ejecución
`python whathefile.py whatthefile.ini <file_or_directory>`

## Servidor web

### Configuración
La configuración del servidor está en `application/web/settings.py` y en 
`application/web/whatthefile.ini`

## Ejecución
Para ejecutar el servidor web
`python runserverpro.py`

# Tests

`python -m pytest`

# Desarrollo de módulos

Los módulos deben estar siempre bajo la carpeta de `src/modules`
Tendrá su carpeta con un fichero llamado `main.py`
La clasedeberá llamarse `Constructor` y deberá implementar la interfaz `IModule`.

```python
# -*- coding: utf-8 -*-
from src.domain.targetpath import TargetPath
class Constructor(IModule):
    def __init__(self):
        super().__init__()

    def is_valid_for(self, target_file: TargetPath) -> bool:
        pass

    """También se admite la firma: 
    def run(self, target_file: TargetFile) -> dict:
    """
    def run(self, target_path: TargetPath, result_of_previos_modules: dict) -> dict:
        pass
```

- El método `is_valid_for` se debe implementar para saber cuándo se puede ejecutar el módulo, por ejemplo, solo para ficheros de tipo jpg, etc.
- El método `run` es la ejecución del módulo, y recibiendo ya un objeto adecuado, es decir, no es necesario volver a validarlo.
- También en el método `run`, se recibe el resultado de los anteriores módulos ejecutados en ese fichero, de tal forma que seacompatible con otros módulos. Por ejemplo infoextractor, que busca información en el resultado de otros módulos ya que por la naturaleza del fichero no se ejecutaría, por ejemplo: un pdf, que al pasar por tika tiene un contenido que luego es analizado finalmente por infoextractor.


## Docker
Para fácil ejecución, existe una carpeta con docker-compose para desplegar herramientas externas así como una versión del servidor web y una de la versión normal.
