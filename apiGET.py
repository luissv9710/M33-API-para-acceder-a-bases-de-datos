from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# Configuración de la conexión a MySQL
def get_db_connection():
    return pymysql.connect(
        host='195.179.238.58',      # Cambia esto según sea necesario
        user='u927419088_admin',
        password='#Admin12345#',
        db='u927419088_testing_sql',
        cursorclass=pymysql.cursors.DictCursor
    )

# Ruta para obtener todos los registros de la tabla "Curso"
@app.route('/api/cursos/', methods=['GET'])
def get_cursos():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM curso"
            cursor.execute(sql)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()

# Ruta para obtener un curso específico por ID
@app.route('/api/cursos/<int:curso_id>', methods=['GET'])
def get_curso(curso_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM curso WHERE idCurso = %s"
            cursor.execute(sql, (curso_id,))
            result = cursor.fetchone()
            if result:
                return jsonify(result)
            else:
                return jsonify({"error": "Curso no encontrado"}), 404
    finally:
        connection.close()


# Ruta para actualizar un curso por ID (usando método POST)
@app.route('/api/cursos/<int:curso_id>', methods=['POST'])
def actualizar_curso(curso_id):
    datos = request.json
    nuevo_asignatura = datos.get('nAsignaturas')
    nuevo_descripcion = datos.get('nombreDescriptivo')

    if not (nuevo_asignatura or nuevo_descripcion):
        return jsonify({"error": "Faltan parámetros de actualización"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE curso SET"
            updates = []
            params = []

            if nuevo_asignatura:
                updates.append(" nAsignaturas = %s")
                params.append(nuevo_asignatura)
            if nuevo_descripcion:
                updates.append(" nombreDescriptivo = %s")
                params.append(nuevo_descripcion)

            sql += ",".join(updates)
            sql += " WHERE idCurso = %s"
            params.append(curso_id)

            cursor.execute(sql, tuple(params))
            connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"message": "Curso actualizado correctamente"})
            else:
                return jsonify({"error": "Curso no encontrado o sin cambios"}), 404
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)