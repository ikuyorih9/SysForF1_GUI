from tkinter import *
from tkinter import ttk

# FUNÇÕES PARA CRIAÇÃO DE LABELS

def cria_label(parent, text, fontsize, fontstyle):
    return Label(parent, text=text, compound="right", bg="#2C3E50", fg="#ECF0F1", font=("Montserrat", fontsize, fontstyle))
    
def cria_label_image(parent, text, fontsize, formattype, image):
    return Label(parent, text=text, image=image, compound="right", bg="#2C3E50", fg="#ECF0F1", font=("Montserrat", fontsize, formattype))

# FUNÇÕES PARA CRIAÇÃO DE BOTÕES

def cria_botao(parent, text, fontsize, command):
    return  Button(parent, text=text, command=command, bg="#3498DB", fg="white", font=("Montserrat", fontsize), relief=GROOVE)

# FUNÇÃO PARA CRIAÇÃO DE FRAME SCROLLAVEL
def cria_scrollable_frame(parent):
    # Evento para atualizar o tamanho do canvas quando os widgets são adicionados.
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(scrollable_frame_id, width=canvas.winfo_width())
    
    # Evento para permitir rolagem com o mouse
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Cria um canvas para a rolagem à esquerda.
    canvas = Canvas(parent, bg="#2C3E50")
    canvas.pack(side="left", fill="both", expand=True)

    # Cria uma barra de rolagem à direita.
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Coneta uma barra de rolagem ao canvas.
    canvas.configure(yscrollcommand=scrollbar.set)

    # Cria um frame geral para conter os widgets
    scrollableFrame = Frame(canvas, bg="#2C3E50")
    scrollable_frame_id = canvas.create_window((0,0), window=scrollableFrame, anchor="nw")
    scrollableFrame.bind("<Configure>", update_scroll_region)
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    return scrollableFrame
