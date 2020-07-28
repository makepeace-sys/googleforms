# googleforms
Api

Google Forms

Se intenta recrear en su forma más básica el comportamiento de Google Forms.
Requerimientos
Se desea poder tener una creación de formularios donde a cada formulario el usuario creador le asigna un listado de preguntas, Los otros usuarios podrán dar respuesta a estos, para esta práctica todas las respuestas dadas a las preguntas serán de carácter numérico
Se requiere:
    • CRUD de Formularios con sus preguntas
        ◦ Las respuestas deben ser de campo númerico (ej: edad: 28)
        ◦ El formulario es creado por una persona autenticada.
    • Se necesitará autenticación:
        ◦ Para poder Crear Formularios
        ◦ Para poder ver los resultados
Reportes:
    • Para cada formulario, el usuario creador podrá ver
        ◦ Total de participantes (usuarios que respondieron al formulario)
        ◦ Promedio por respuestas (si el form tiene 5 preguntas, no se requiere el promedio de las 5, si no que el promedio de la pregunta 1, 2, 3, 4 y 5 según las veces que fueron contestadas respectivamente) (ej: edad promedio 25 años)
Un usuario no autenticado no debe poder ver ningún reporte
