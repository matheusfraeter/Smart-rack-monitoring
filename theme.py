"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: theme.py
 Descrição...: Tema visual da aplicação
 Autor.......: Matheus Henrique Fraeter da Cruz
=========================================================
"""


class Theme:
    """
    Classe responsável por armazenar todas as cores
    e estilos da aplicação.
    """

    # =====================================================
    # PALETA DE CORES
    # =====================================================

    BACKGROUND = "#1E1E2E"
    SIDEBAR = "#181825"
    HEADER = "#313244"
    CARD = "#45475A"

    PRIMARY = "#89B4FA"
    SUCCESS = "#A6E3A1"
    WARNING = "#F9E2AF"
    ERROR = "#F38BA8"

    TEXT = "#CDD6F4"
    TEXT_SECONDARY = "#BAC2DE"

    BORDER = "#585B70"

    # =====================================================
    # ESTILO GERAL
    # =====================================================

    @staticmethod
    def application():

        return f"""
        QWidget {{
            background-color: {Theme.BACKGROUND};
            color: {Theme.TEXT};
            font-family: Segoe UI;
            font-size: 10pt;
        }}
        """

    # =====================================================
    # MENU LATERAL
    # =====================================================

    @staticmethod
    def sidebar():

        return f"""
        QFrame {{
            background-color: {Theme.SIDEBAR};
            border: none;
        }}
        """

    # =====================================================
    # BOTÕES
    # =====================================================

    @staticmethod
    def button():

        return f"""
        QPushButton {{

            background-color: transparent;

            color: {Theme.TEXT};

            border: none;

            text-align: left;

            padding: 12px;

            border-radius: 8px;

            font-size: 11pt;

        }}

        QPushButton:hover {{

            background-color: {Theme.PRIMARY};
            color: black;

        }}

        QPushButton:pressed {{

            background-color: #74C7EC;

        }}
        """

    # =====================================================
    # TÍTULOS
    # =====================================================

    @staticmethod
    def title():

        return f"""
        QLabel {{

            font-size: 22pt;
            font-weight: bold;
            color: {Theme.TEXT};

        }}
        """

    # =====================================================
    # STATUS BAR
    # =====================================================

    @staticmethod
    def statusbar():

        return f"""
        QStatusBar {{

            background-color: {Theme.HEADER};

            color: {Theme.TEXT};

        }}
        """