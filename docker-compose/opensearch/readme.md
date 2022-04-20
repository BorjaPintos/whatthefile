# permisos

El directorio data que se usa en el volumen, necesita permisos del usuario 1000 (ya que es el que corre dentro del docker)

```bash
chown -R 1000:1000 ./data

```