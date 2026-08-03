"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: database.py
 Descrição...: Gerenciamento do banco SQLite
 Versão......: 0.3
=========================================================
"""

import sqlite3
from datetime import datetime



class Database:


    def __init__(self):

        self.nome_banco = "smart_rack.db"

        self.criar_tabelas()

        self.criar_rack_inicial()



    # =================================================
    # CONEXÃO
    # =================================================

    def conectar(self):

        return sqlite3.connect(
            self.nome_banco
        )



    # =================================================
    # CRIAÇÃO DAS TABELAS
    # =================================================

    def criar_tabelas(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rack_positions
            (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                endereco TEXT NOT NULL UNIQUE,

                estante TEXT NOT NULL,

                nivel INTEGER NOT NULL,

                coluna INTEGER NOT NULL,

                ocupado INTEGER DEFAULT 0,

                pallet TEXT

            )
            """
        )



        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentos
            (

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




    # =================================================
    # CRIAR RACK INICIAL
    #
    # A11 até A34
    # B11 até B34
    #
    # TOTAL 24 POSIÇÕES
    # =================================================

    def criar_rack_inicial(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        for estante in ["A", "B"]:


            for nivel in range(1,4):


                for coluna in range(1,5):


                    endereco = (
                        f"{estante}"
                        f"{nivel}"
                        f"{coluna}"
                    )


                    cursor.execute(
                        """
                        SELECT endereco

                        FROM rack_positions

                        WHERE endereco = ?

                        """,
                        (
                            endereco,
                        )
                    )


                    existe = cursor.fetchone()



                    if existe is None:


                        cursor.execute(
                            """
                            INSERT INTO rack_positions
                            (
                                endereco,
                                estante,
                                nivel,
                                coluna
                            )

                            VALUES (?, ?, ?, ?)

                            """,
                            (
                                endereco,
                                estante,
                                nivel,
                                coluna
                            )
                        )



        conexao.commit()

        conexao.close()




    # =================================================
    # LISTAR POSIÇÕES
    # =================================================

    def listar_posicoes(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            SELECT

                endereco,
                ocupado,
                pallet

            FROM rack_positions

            ORDER BY
                estante,
                nivel,
                coluna

            """
        )



        dados = cursor.fetchall()


        conexao.close()


        return dados




    # =================================================
    # BUSCAR POSIÇÃO
    # =================================================

    def buscar_posicao(
            self,
            endereco
    ):


        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            SELECT

                endereco,
                ocupado,
                pallet

            FROM rack_positions

            WHERE endereco = ?

            """,
            (
                endereco,
            )
        )


        resultado = cursor.fetchone()


        conexao.close()


        return resultado




    # =================================================
    # OCUPAR POSIÇÃO
    # =================================================

    def ocupar_posicao(
            self,
            endereco,
            pallet
    ):


        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            UPDATE rack_positions

            SET

                ocupado = 1,

                pallet = ?

            WHERE endereco = ?

            """,
            (
                pallet,
                endereco
            )
        )


        conexao.commit()

        conexao.close()




    # =================================================
    # LIBERAR POSIÇÃO
    # =================================================

    def liberar_posicao(
            self,
            endereco
    ):


        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            UPDATE rack_positions

            SET

                ocupado = 0,

                pallet = NULL

            WHERE endereco = ?

            """,
            (
                endereco,
            )
        )



        conexao.commit()

        conexao.close()




    # =================================================
    # REGISTRAR MOVIMENTO
    # =================================================

    def registrar_movimento(
            self,
            origem,
            destino,
            status
    ):


        conexao = self.conectar()

        cursor = conexao.cursor()



        data = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )



        cursor.execute(
            """
            INSERT INTO movimentos
            (
                origem,
                destino,
                data,
                status
            )

            VALUES (?, ?, ?, ?)

            """,
            (
                origem,
                destino,
                data,
                status
            )
        )


        conexao.commit()

        conexao.close()




    # =================================================
    # LISTAR HISTÓRICO
    # =================================================

    def listar_movimentos(self):


        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            SELECT

                id,
                data,
                origem,
                destino,
                status

            FROM movimentos

            ORDER BY id DESC

            """
        )



        dados = cursor.fetchall()


        conexao.close()


        return dados