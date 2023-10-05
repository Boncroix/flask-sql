from datetime import date
import sqlite3


class DBManager:
    '''
    Clase para interactuar con la base de datos SQLite
    '''

    def __init__(self, ruta):
        self.ruta = ruta

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

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
        sql = 'DELETE FROM movimientos WHERE id=?'  # consulta ha realizar
        # crear la conexión con la base de datos
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()                  # preparar cursor

        resultado = False
        try:
            # pasar la consulta e indicarle como parámetro el id
            cursor.execute(sql, (id,))
            conexion.commit()                       # borrar fila del id que le hemos pasado
            resultado = True
        except:
            # Si nos da error hacer comand z para retrocceder
            conexion.rollback()
            resultado = False

        conexion.close()                            # Cerrar conexión
        return resultado

    def obtenerMovimiento(self, id):
        # consulta que queremos realizar
        sql = 'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id=?'
        conexion = sqlite3.connect(self.ruta)  # conectar con la base de datos
        cursor = conexion.cursor()  # preparar el cursor
        # pasarle la consulta y como parámetros en una tupla el id del movimiento
        cursor.execute(sql, (id,))
        datos = cursor.fetchone()  # leer una fila cursor.fechall lee todos los movimientos
        resultado = None
        if datos:
            nombres_columnas = []
            for columna in cursor.description:
                nombres_columnas.append(columna[0])

            movimiento = {}                         #
            indice = 0                              # Crear diccionario con los datos leidos
            for nombre in nombres_columnas:         #
                movimiento[nombre] = datos[indice]
                indice += 1

            movimiento['fecha'] = date.fromisoformat(movimiento['fecha'])
            resultado = movimiento

        conexion.close()
        return resultado

    def consultaConParametros(self, consulta, params):
        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return resultado
