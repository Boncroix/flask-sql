from datetime import date
import sqlite3


class DBManager:
    '''
    Clase para interactuar con la base de datos SQLite
    '''

    def __init__(self, ruta):
        self.ruta = ruta

    def consultaSQL(self, consulta):

        # 1. Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2. Abrir cursor
        cursor = conexion.cursor()

        # 3. Ejecutar la consulta
        cursor.execute(consulta)

        # 4. Tratar los datos
        # 4.1 Obtener los datos
        datos = cursor.fetchall()

        # 4.2 Los guardo localmente
        self.registros = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            movimiento = {}
            indice = 0
            for nombre in nombres_columna:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.registros.append(movimiento)

        # 5. Cerrar la conexión
        conexion.close()

        # 6. Devolver los resultados
        return self.registros

    def borrar(self, id):
        '''
        DELETE FROM movimientos WHERE id=?
        '''
        sql = 'DELETE FROM movimientos WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        resultado = False
        try:
            cursor.execute(sql, (id,))
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()
            resultado = False

        conexion.close()
        return resultado

    def editar(self, id):
        sql = 'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(sql, (id,))
        datos = cursor.fetchall()
        self.nombres_columna = []
        for columna in cursor.description:
            self.nombres_columna.append(columna[0])

        movimiento = {}
        indice = 0
        for nombre in self.nombres_columna:
            if nombre == 'fecha':
                movimiento[nombre] = date.fromisoformat(datos[0][indice])
            else:
                movimiento[nombre] = datos[0][indice]
            indice += 1
        return movimiento
