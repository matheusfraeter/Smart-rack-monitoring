"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: database.py
 Descrição...: Gerenciamento do banco SQLite
=========================================================
"""

import sqlite3


class Database:


    def __init__(self):

        self.nome_banco = "smart_rack.db"

        self.criar_tabelas()



    def conectar(self):

        return sqlite3.connect(
            self.nome_banco
        )



    def criar_tabelas(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        # =====================================
        # POSIÇÕES DO RACK
        # =====================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rack_positions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                endereco TEXT NOT NULL,

                ocupado INTEGER DEFAULT 0,

                pallet TEXT

            )
            """
        )



        # =====================================
        # HISTÓRICO DE MOVIMENTAÇÕES
        # =====================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                origem TEXT,

                destino TEXT,

                data TEXT,

                status TEXT

            )
            """
        )



        conexao.commit()

        conexao.close()



    def inserir_posicao(
            self,
            endereco
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()


        cursor.execute(
            """
            INSERT INTO rack_positions
            (endereco)

            VALUES (?)
            """,
            (
                endereco,
            )
        )


        conexao.commit()

        conexao.close()