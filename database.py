"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: database.py
 Descrição...: Gerenciamento do banco SQLite
 Versão......: 0.6
=========================================================
"""

import sqlite3
from datetime import datetime


class Database:

    def __init__(self):

        self.nome_banco = "smart_rack.db"

        self.criar_tabelas()

        self.atualizar_banco()

        self.criar_rack_inicial()

        self.criar_posicoes_maquina()

        self.criar_configuracoes_empilhadeira()


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

        # ---------------------------------------------
        # POSIÇÕES DO RACK
        # ---------------------------------------------

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

                pallet TEXT,

                x REAL DEFAULT 0.0,

                y REAL DEFAULT 0.0,

                z REAL DEFAULT 0.0
            )
            """
        )

        # ---------------------------------------------
        # HISTÓRICO
        # ---------------------------------------------

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

        # ---------------------------------------------
        # POSIÇÕES ESPECIAIS DA MÁQUINA
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS machine_positions
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL UNIQUE,

                x REAL DEFAULT 0.0,

                y REAL DEFAULT 0.0,

                z REAL DEFAULT 0.0
            )
            """
        )

        # ---------------------------------------------
        # CONFIGURAÇÕES DA EMPILHADEIRA
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS forklift_settings
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL UNIQUE,

                valor REAL DEFAULT 0.0
            )
            """
        )

        conexao.commit()

        conexao.close()


    # =================================================
    # ATUALIZAÇÃO DO BANCO EXISTENTE
    # =================================================

    def atualizar_banco(self):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            PRAGMA table_info(rack_positions)
            """
        )

        colunas = cursor.fetchall()

        nomes_colunas = [
            coluna[1]
            for coluna in colunas
        ]

        # ---------------------------------------------
        # ADICIONA X
        # ---------------------------------------------

        if "x" not in nomes_colunas:

            cursor.execute(
                """
                ALTER TABLE rack_positions
                ADD COLUMN x REAL DEFAULT 0.0
                """
            )

        # ---------------------------------------------
        # ADICIONA Y
        # ---------------------------------------------

        if "y" not in nomes_colunas:

            cursor.execute(
                """
                ALTER TABLE rack_positions
                ADD COLUMN y REAL DEFAULT 0.0
                """
            )

        # ---------------------------------------------
        # ADICIONA Z
        # ---------------------------------------------

        if "z" not in nomes_colunas:

            cursor.execute(
                """
                ALTER TABLE rack_positions
                ADD COLUMN z REAL DEFAULT 0.0
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

        for estante in [
            "A",
            "B"
        ]:

            for nivel in range(
                1,
                4
            ):

                for coluna in range(
                    1,
                    5
                ):

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
                                coluna,
                                ocupado,
                                pallet,
                                x,
                                y,
                                z
                            )

                            VALUES (
                                ?,
                                ?,
                                ?,
                                ?,
                                0,
                                NULL,
                                0.0,
                                0.0,
                                0.0
                            )

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
    # CRIAR POSIÇÕES DA MÁQUINA
    #
    # RECEBIMENTO
    # EXPEDICAO
    # Z_TRANSPORTE
    # =================================================

    def criar_posicoes_maquina(self):

        conexao = self.conectar()

        cursor = conexao.cursor()

        posicoes = [
            "RECEBIMENTO",
            "EXPEDICAO",
            "Z_TRANSPORTE"
        ]

        for nome in posicoes:

            cursor.execute(
                """
                SELECT nome

                FROM machine_positions

                WHERE nome = ?

                """,
                (
                    nome,
                )
            )

            existe = cursor.fetchone()

            if existe is None:

                cursor.execute(
                    """
                    INSERT INTO machine_positions
                    (
                        nome,
                        x,
                        y,
                        z
                    )

                    VALUES (?, 0.0, 0.0, 0.0)

                    """,
                    (
                        nome,
                    )
                )

        conexao.commit()

        conexao.close()


    # =================================================
    # CONFIGURAÇÕES DA EMPILHADEIRA
    #
    # Z_LEVANTAR
    # Z_APOIAR
    # =================================================

    def criar_configuracoes_empilhadeira(self):

        conexao = self.conectar()

        cursor = conexao.cursor()

        configuracoes = [
            (
                "Z_LEVANTAR",
                10.0
            ),
            (
                "Z_APOIAR",
                10.0
            )
        ]

        for nome, valor in configuracoes:

            cursor.execute(
                """
                SELECT nome

                FROM forklift_settings

                WHERE nome = ?

                """,
                (
                    nome,
                )
            )

            existe = cursor.fetchone()

            if existe is None:

                cursor.execute(
                    """
                    INSERT INTO forklift_settings
                    (
                        nome,
                        valor
                    )

                    VALUES (?, ?)

                    """,
                    (
                        nome,
                        valor
                    )
                )

        conexao.commit()

        conexao.close()


    # =================================================
    # OBTER CONFIGURAÇÃO DA EMPILHADEIRA
    # =================================================

    def obter_configuracao_empilhadeira(
        self,
        nome
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT valor

            FROM forklift_settings

            WHERE nome = ?

            """,
            (
                nome,
            )
        )

        resultado = cursor.fetchone()

        conexao.close()

        if resultado is None:

            return None

        return float(
            resultado[0] or 0.0
        )


    # =================================================
    # OBTER TODAS AS CONFIGURAÇÕES DA EMPILHADEIRA
    # =================================================

    def listar_configuracoes_empilhadeira(self):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                nome,
                valor

            FROM forklift_settings

            ORDER BY id
            """
        )

        dados = cursor.fetchall()

        conexao.close()

        return dados


    # =================================================
    # SALVAR CONFIGURAÇÃO DA EMPILHADEIRA
    # =================================================

    def salvar_configuracao_empilhadeira(
        self,
        nome,
        valor
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE forklift_settings

            SET
                valor = ?

            WHERE nome = ?

            """,
            (
                float(valor),
                nome
            )
        )

        atualizado = (
            cursor.rowcount > 0
        )

        conexao.commit()

        conexao.close()

        return atualizado


    # =================================================
    # LISTAR POSIÇÕES DO RACK
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
    # LISTAR COORDENADAS
    # =================================================

    def listar_coordenadas(self):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT

                endereco,
                x,
                y,
                z

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
    # OBTER COORDENADAS
    # =================================================

    def obter_coordenadas(
        self,
        endereco
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT

                x,
                y,
                z

            FROM rack_positions

            WHERE endereco = ?

            """,
            (
                endereco,
            )
        )

        resultado = cursor.fetchone()

        conexao.close()

        if resultado is None:

            return None

        return {
            "X": float(
                resultado[0] or 0.0
            ),

            "Y": float(
                resultado[1] or 0.0
            ),

            "Z": float(
                resultado[2] or 0.0
            )
        }


    # =================================================
    # SALVAR COORDENADAS
    # =================================================

    def salvar_coordenadas(
        self,
        endereco,
        x,
        y,
        z
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE rack_positions

            SET

                x = ?,

                y = ?,

                z = ?

            WHERE endereco = ?

            """,
            (
                float(x),
                float(y),
                float(z),
                endereco
            )
        )

        atualizado = (
            cursor.rowcount > 0
        )

        conexao.commit()

        conexao.close()

        return atualizado


    # =================================================
    # LISTAR POSIÇÕES DA MÁQUINA
    # =================================================

    def listar_posicoes_maquina(self):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT

                nome,
                x,
                y,
                z

            FROM machine_positions

            ORDER BY id

            """
        )

        dados = cursor.fetchall()

        conexao.close()

        return dados


    # =================================================
    # OBTER POSIÇÃO DA MÁQUINA
    # =================================================

    def obter_posicao_maquina(
        self,
        nome
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT

                x,
                y,
                z

            FROM machine_positions

            WHERE nome = ?

            """,
            (
                nome,
            )
        )

        resultado = cursor.fetchone()

        conexao.close()

        if resultado is None:

            return None

        return {
            "X": float(
                resultado[0] or 0.0
            ),

            "Y": float(
                resultado[1] or 0.0
            ),

            "Z": float(
                resultado[2] or 0.0
            )
        }


    # =================================================
    # SALVAR POSIÇÃO DA MÁQUINA
    # =================================================

    def salvar_posicao_maquina(
        self,
        nome,
        x,
        y,
        z
    ):

        conexao = self.conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE machine_positions

            SET

                x = ?,

                y = ?,

                z = ?

            WHERE nome = ?

            """,
            (
                float(x),
                float(y),
                float(z),
                nome
            )
        )

        atualizado = (
            cursor.rowcount > 0
        )

        conexao.commit()

        conexao.close()

        return atualizado


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
