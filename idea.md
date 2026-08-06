Quiero construir un proyecto backend para mi portafolio de GitHub: un 
servicio que permite subir, almacenar y servir archivos a través de un 
CDN (ej. AWS S3 + CloudFront, o Cloudflare R2).

Stack propuesto: Python + FastAPI + PostgreSQL (para metadatos de archivos) 
+ el proveedor de CDN que recomiendes. Soy desarrollador junior y busco 
tanto un proyecto de portafolio convincente como aprendizaje real de 
infraestructura.

Ayúdame a:
1. Definir el alcance mínimo viable (tipos de archivo, límites de tamaño, 
   quién puede subir/acceder)
2. Diseñar los endpoints (subida, descarga, listado, borrado) y el modelo 
   de datos para metadatos
3. Explicar cómo funciona la integración con el CDN elegido y qué necesito 
   configurar (buckets, políticas de acceso, URLs firmadas si aplica)
4. Señalar los riesgos de seguridad a los que debo prestar atención (ej. 
   no exponer credenciales, validar tipos de archivo, control de acceso)
5. Listar los pasos de implementación en orden, del más simple al más avanzado
No escribas código todavía, solo el plan.