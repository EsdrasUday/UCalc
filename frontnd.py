import customtkinter as ctk
import sys
from PIL import Image
from backend import s
from CTkMessagebox import CTkMessagebox

class Calculadora:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.roxo = "#2C001E"
        self.laranja = "#E95420"
        self.branco = "#FFFFFF"
        self.cinza = "#525252"
        self.app = ctk.CTk()
        self.app.title("UCalculator")
        self.app.geometry("420x600")
        self.app.minsize(width=420, height=460)
        self.app.configure(fg_color=self.roxo)
        self.Tela()
        
    def Tela(self):
        if sys.platform == "win32":
            try:
                self.app.iconbitmap("IMG/logo.ico")
            except:
              pass
        try:
            imagem = ctk.CTkImage(light_image=Image.open("IMG/Logo.png"), size=(110, 110))
            label_imagem = ctk.CTkLabel(self.app, image=imagem, text="")
            label_imagem.pack(pady=5)
        except:
            pass
        
        title_label = ctk.CTkLabel(self.app, text="Calculadora Estatística", font=("Arial", 16, "bold"), text_color=self.branco)
        title_label.pack(pady=5)
        
        self.entry = ctk.CTkEntry(self.app, placeholder_text="Digite números separados por vírgula", width=300)
        self.entry.pack(pady=10)
        
        frame_botoes = ctk.CTkFrame(self.app, fg_color="transparent", width=350)
        frame_botoes.pack(pady=5)

        self.pasta_button = ctk.CTkButton(frame_botoes, text="Exportar Excel",command=self.exportar, fg_color=self.cinza,state="disabled", hover_color='#b33205', text_color=self.branco)
        self.pasta_button.pack(side="right", expand=True, padx=5, pady=5)

        botao_calcular = ctk.CTkButton(frame_botoes, text="Calcular", fg_color=self.laranja,command=lambda:[self.ativar_botao(),self.calcular()], hover_color='#b33205', text_color=self.branco)
        botao_calcular.pack(side="right", expand=True, padx=5, pady=5)
        
        self.resultado_label = ctk.CTkLabel(self.app, text="Resultados aparecerão aqui!",font=("Roboto", 12, "bold"), wraplength=480)
        self.resultado_label.pack(pady=10)

        dev_label = ctk.CTkLabel(self.app, text="Developer Esdras Uday Da Silveira Maracajá", font=("Roboto", 9, "bold"), text_color="grey")
        dev_label.pack(side='bottom', pady=1)

        self.tabela_frame = ctk.CTkScrollableFrame(self.app,fg_color="transparent",height=300,width=430,scrollbar_button_color=self.roxo,scrollbar_button_hover_color=self.roxo)
        self.tabela_frame.pack(padx=40,pady=10)
        
    def iniciar(self):
        self.app.mainloop()

    def ativar_botao(self):
        if self.entry.get().strip():
            self.pasta_button.configure(fg_color=self.laranja, state="normal")
        else:
            self.pasta_button.configure(fg_color=self.cinza, state="disabled") 

    def calcular(self):
        try:
            dados = list(map(float, self.entry.get().strip().split(',')))
            media, mediana, moda, desvio_padrao, coef_variancia = s.calcular_estatisticas(dados)
            intervalos = s.calcular_intervalo_classes(dados)
            fi, Fi, fri, Fri = s.calcular_frequencia(dados, intervalos)
            fri_percent = {k: v * 100 for k, v in fri.items()}
            Fri_percent = {k: v * 100 for k, v in Fri.items()}
            self.intervalos = intervalos
            self.fi = fi
            self.Fi = Fi
            self.fri = fri
            self.Fri = Fri
            self.fri_percent = fri_percent
            self.Fri_percent = Fri_percent
            self.resultado_label.configure(text=(
                f"Rol: {sorted(dados)}\n"
                f"Média: {media:.2f}\n"
                f"Mediana: {mediana:.2f}\n"
                f"Moda: {moda}\n"
                f"Desvio Padrão: {desvio_padrao:.2f}\n"
                f"Coeficiente de Variação: {coef_variancia:.2f}%\n"
                f"Intervalo de Classe: {len(intervalos)}"))
            
            self.exibir_tabela(intervalos, fi, Fi, fri, Fri, fri_percent, Fri_percent)
        except ValueError:
            self.resultado_label.configure(text="Erro: Insira números válidos separados por vírgula.")

    def exibir_tabela(self, intervalos, fi, Fi, fri, Fri, fri_percent, Fri_percent):
        for widget in self.tabela_frame.winfo_children():
            widget.destroy()
        
        titulos = ["Intervalo", "fi", "Fi", "fri", "fri %", "Fri", "Fri %"]
        for colulnas, titulo in enumerate(titulos):
            label = ctk.CTkLabel(self.tabela_frame, text=titulo, font=("Arial", 12, "bold"))
            label.grid(row=0, column=colulnas, padx=10, pady=5,sticky="nsew")
        
        for linha, (intervalo, frequencia, Fi_valor, fri_valor, fri_percentual, Fri_valor, Fri_percentual) in enumerate(zip(intervalos, fi.values(), Fi.values(), fri.values(), fri_percent.values(), Fri.values(), Fri_percent.values()), start=1):
            tabela_intervalo = f"{intervalo[0]} ➝ {intervalo[1]}"
            valores = [tabela_intervalo, frequencia, Fi_valor, fri_valor, f"{fri_percentual:.2f}%", Fri_valor, f"{Fri_percentual:.2f}%"]
            
            for coluna, val in enumerate(valores):
                label = ctk.CTkLabel(self.tabela_frame, text=f"{val}", font=("Arial", 12))
                label.grid(row=linha, column=coluna, padx=10, pady=5)

    def exportar(self):
        try:
            s.exportar_para_excel(self.intervalos, self.fi, self.Fi, self.fri, self.Fri, self.fri_percent, self.Fri_percent)
            CTkMessagebox(title="Sucesso", message="Tabela exportada com sucesso!", icon="check")
        except AttributeError:
            CTkMessagebox(title="Erro", message="Calcule os dados antes de exportar!", icon="cancel")


if __name__ == "__main__":
    app = Calculadora()
    app.iniciar()

