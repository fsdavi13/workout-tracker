import customtkinter as ctk

from database.connection import inicializar_banco
from dao.alimento_dao import AlimentoDAO
from dao.corrida_dao import CorridaDAO
from dao.exercicio_dao import ExercicioDAO
from dao.serie_dao import SerieDAO


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        inicializar_banco()

        self.title("Workout Tracker")
        self.geometry("900x600")

        self.alimento_dao = AlimentoDAO()
        self.exercicio_dao = ExercicioDAO()
        self.serie_dao = SerieDAO()
        self.corrida_dao = CorridaDAO()

        self.criar_widgets()

    def criar_widgets(self):

        titulo = ctk.CTkLabel(
            self,
            text="🏋️ Workout Tracker",
            font=("Arial", 30, "bold")
        )

        titulo.pack(pady=20)

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        alimentos = self.alimento_dao.buscar_todos()
        exercicios = self.exercicio_dao.buscar_todos()
        series = self.serie_dao.buscar_todas()
        corridas = self.corrida_dao.buscar_todas()

        texto = (
            f"Alimentos cadastrados: {len(alimentos)}\n"
            f"Exercícios cadastrados: {len(exercicios)}\n"
            f"Séries cadastradas: {len(series)}\n"
            f"Corridas cadastradas: {len(corridas)}"
        )

        info = ctk.CTkLabel(
            frame,
            text=texto,
            font=("Arial", 18),
            justify="left"
        )

        info.pack(pady=20)

        botoes = ctk.CTkFrame(frame)

        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Listar Exercícios",
            command=self.listar_exercicios
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            botoes,
            text="Listar Alimentos",
            command=self.listar_alimentos
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            botoes,
            text="Fechar",
            command=self.destroy
        ).grid(row=0, column=2, padx=10)

        self.caixa = ctk.CTkTextbox(
            frame,
            width=800,
            height=300
        )

        self.caixa.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

    def listar_alimentos(self):

        self.caixa.delete("1.0", "end")

        alimentos = self.alimento_dao.buscar_todos()

        for alimento in alimentos:

            self.caixa.insert(
                "end",
                (
                    f"{alimento.id} - "
                    f"{alimento.nome}\n"
                    f"Calorias: {alimento.calorias_por_100g:.1f} kcal\n"
                    f"Proteína: {alimento.proteinas_g:.1f} g\n"
                    f"Carboidratos: {alimento.carboidratos_g:.1f} g\n"
                    f"Gorduras: {alimento.gorduras_g:.1f} g\n"
                    f"Categoria: {alimento.categoria}\n\n"
                )
            )

    def listar_exercicios(self):

        self.caixa.delete("1.0", "end")

        exercicios = self.exercicio_dao.buscar_todos()

        if len(exercicios) == 0:

            self.caixa.insert(
                "end",
                "Nenhum exercício cadastrado."
            )

            return

        for exercicio in exercicios:

            self.caixa.insert(
                "end",
                (
                    f"{exercicio.id} - "
                    f"{exercicio.nome}\n"
                    f"Grupo muscular: "
                    f"{exercicio.grupo_muscular}\n\n"
                )
            )


if __name__ == "__main__":

    app = App()

    app.mainloop()