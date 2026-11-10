# bucket-artifacts

Páginas estáticas (artifacts, explicadores, informes en HTML) publicadas con GitHub Pages, para que
no dependan del servicio donde se crearon.

Sitio: https://agustin130a.github.io/bucket-artifacts/

## Estructura

Una carpeta por tema o proyecto; adentro, una página por archivo:

```
tesis-inferhive/time-slicing.html
<tema>/<pagina>.html
<tema>/<pagina>/index.html   # si la página trae imágenes u otros archivos
```

Cada página es un HTML autocontenido (`<!doctype html>`, `<head>` con `<title>`). El `<title>` es
el nombre que aparece en el índice.

## Publicar

Hacer push a `main`. El workflow `pages` genera `index.html` con `scripts/build_index.py` y
despliega el sitio. Para ver el índice en local:

```bash
python3 scripts/build_index.py && python3 -m http.server
```

Todo lo que se sube acá es público: nada de secretos, datos de clientes ni infraestructura privada.
