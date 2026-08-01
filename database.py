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

        self.criar_rack_inicial()



    # =====================================
    # CONEXÃO COM BANCO
    # =====================================

    def conectar(self):

        return sqlite3.connect(
            self.nome_banco
        )



    # =====================================
    # CRIAÇÃO DAS TABELAS
    # =====================================

    def criar_tabelas(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        # ---------------------------------
        # POSIÇÕES DO RACK
        # ---------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rack_positions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                endereco TEXT NOT NULL UNIQUE,

                ocupado INTEGER DEFAULT 0,

                pallet TEXT

            )
            """
        )



        # ---------------------------------
        # HISTÓRICO DE MOVIMENTAÇÕES
        # ---------------------------------

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



    # =====================================
    # CRIA RACK INICIAL A1-D4
    # =====================================

    def criar_rack_inicial(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        linhas = [

            "A",
            "B",
            "C",
            "D"

        ]



        for letra in linhas:

            for numero in range(1, 5):

                endereco = f"{letra}{numero}"



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

                        (endereco)

                        VALUES (?)

                        """,
                        (
                            endereco,
                        )
                    )



        conexao.commit()

        conexao.close()



    # =====================================
    # INSERIR NOVA POSIÇÃO
    # =====================================

    def inserir_posicao(self, endereco):

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



    # =====================================
    # LISTAR POSIÇÕES DO RACK
    # =====================================

    def listar_posicoes(self):

        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            SELECT endereco, ocupado, pallet

            FROM rack_positions

            ORDER BY endereco

            """
        )



        dados = cursor.fetchall()



        conexao.close()



        return dados



    # =====================================
    # OCUPAR POSIÇÃO DO RACK
    # =====================================

    def ocupar_posicao(self, endereco, pallet):

        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            UPDATE rack_positions

            SET ocupado = 1,

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



    # =====================================
    # LIBERAR POSIÇÃO DO RACK
    # =====================================

    def liberar_posicao(self, endereco):

        conexao = self.conectar()

        cursor = conexao.cursor()



        cursor.execute(
            """
            UPDATE rack_positions

            SET ocupado = 0,

                pallet = NULL

            WHERE endereco = ?

            """,
            (
                endereco,
            )
        )



        conexao.commit()

        conexao.close()

    # =====================================
    # BUSCAR INFORMAÇÃO DA POSIÇÃO
    # =====================================

    def buscar_posicao(self, endereco):

        conexao = self.conectar()

        cursor = conexao.cursor()


        cursor.execute(
            """
            SELECT endereco, ocupado, pallet

            FROM rack_positions

            WHERE endereco = ?

            """,
            (
                endereco,
            )
        )


        dados = cursor.fetchone()


        conexao.close()


        return dados

    # =====================================
    # REGISTRAR MOVIMENTO
    # =====================================

    def registrar_movimento(
            self,
            origem,
            destino,
            status
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()


        cursor.execute(
            """
            INSERT INTO movimentos

            (
                origem,
                destino,
                data,
                status
            )

            VALUES
            (
                ?,
                ?,
                datetime('now'),
                ?
            )

            """,
            (
                origem,
                destino,
                status
            )
        )


        conexao.commit()

        conexao.close()

    # =====================================
    # LISTAR MOVIMENTOS
    # =====================================

    def listar_movimentos(self):

        conexao = self.conectar()

        cursor = conexao.cursor()


        cursor.execute(
            """
            SELECT 
                origem,
                destino,
                data,
                status

            FROM movimentos

            ORDER BY id DESC

            """
        )


        dados = cursor.fetchall()


        conexao.close()


        return dados

    # =====================================
    # LISTAR HISTÓRICO
    # =====================================

    def listar_movimentos(self):

        conexao = self.conectar()

        cursor = conexao.cursor()


        cursor.execute(
            """
            SELECT 
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