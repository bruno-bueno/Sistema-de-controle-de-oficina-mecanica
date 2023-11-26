from app import mysql
import hashlib

def md5(texto):
    hash_md5 = hashlib.md5()
    hash_md5.update(texto.encode('utf-8'))
    return hash_md5.hexdigest()

class Usuarios:
    def criarUsuario(self, nome, senha):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Usuarios (nome, senha) VALUES (%s, %s)", (nome, md5(senha)))
        mysql.connection.commit()
        cursor.close()

    def autenticarLogin(self, nome, senha):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE nome = %s AND senha = %s", (nome, md5(senha)))
        user = cursor.fetchone()
        cursor.close()
        return user
