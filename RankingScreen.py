import os
import json
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from ctypes import windll

TeamsHistory = "teams.json"

#Funções utilizadas no código-----------------------------------------------

def clear():
    os.system('cls')

def load_teams():
    if os.path.exists(TeamsHistory):
        with open(TeamsHistory, "r") as f:
            return json.load(f)
    return []

def save_teams(teams):
    with open(TeamsHistory, "w") as f:
        json.dump(teams, f)

def create_teams(names):
    return {"nome": names, "pontos": 0}

def get_team_names():
    teams = load_teams()
    return [t['nome'] for t in teams] if teams else ["Nenhuma equipe"]

def open_admin():
    teams = load_teams()

    admin = ctk.CTkToplevel(app)
    admin.title("Painel do Admin")
    admin.geometry("600x800")
    admin.configure(fg_color="#e6e6e6")

    scroll = ctk.CTkScrollableFrame(admin, fg_color="#e6e6e6")
    scroll.pack(fill="both", expand=True, padx=20, pady=20)

    #Título----------------------------------------
    ctk.CTkLabel(
        scroll, text="ADMIN",
        font=("Press Start 2P", 22),
        text_color="#ff0000"
    ).pack(pady=(20, 30))

    #Registrar Equipe----------------------------
    ctk.CTkLabel(scroll, text="REGISTRAR EQUIPE",
        font=("Press Start 2P", 11), text_color="#ff0000"
    ).pack(anchor="w", pady=(0, 6))

    team_entry = ctk.CTkEntry(
        scroll, placeholder_text="Nome da equipe",
        height=40, corner_radius=0,
        fg_color="white", border_color="#ff0000",
        text_color="#000000", font=("Press Start 2P", 11)
    )
    team_entry.pack(fill="x", pady=(0, 6))

    def register_team():
        name = team_entry.get().strip()
        if not name:
            messagebox.showwarning("Atenção", "Digite um nome!")
            return
        teams = load_teams()
        teams.append(create_teams(name))
        save_teams(teams)
        team_entry.delete(0, "end")
        refresh_dropdowns()
        messagebox.showinfo("✅", f"Equipe '{name}' registrada!")

    ctk.CTkButton(
        scroll, text="Registrar",
        command=register_team,
        font=("Press Start 2P", 11),
        height=40, corner_radius=0,
        fg_color="transparent", border_width=2,
        border_color="#ff0000", text_color="#ff0000",
        hover_color="#ffcccc"
    ).pack(fill="x", pady=(0, 25))

    #Adicionar Pontos-------------------------------
    ctk.CTkLabel(scroll, text="ADICIONAR PONTOS",
        font=("Press Start 2P", 11), text_color="#ff0000"
    ).pack(anchor="w", pady=(0, 6))

    add_team_var = ctk.StringVar(value="Selecione...")
    add_team_menu = ctk.CTkOptionMenu(
        scroll, variable=add_team_var,
        values=get_team_names(),
        font=("Press Start 2P", 10),
        fg_color="white", button_color="#ff0000",
        button_hover_color="#cc0000", text_color="#000000",
        dropdown_fg_color="white", dropdown_text_color="#000000",
        corner_radius=0, height=40
    )
    add_team_menu.pack(fill="x", pady=(0, 6))

    add_points_entry = ctk.CTkEntry(
        scroll, placeholder_text="Pontos a adicionar",
        height=40, corner_radius=0,
        fg_color="white", border_color="#ff0000",
        text_color="#000000", font=("Press Start 2P", 11)
    )
    add_points_entry.pack(fill="x", pady=(0, 6))

    def add_points_gui():
        teams = load_teams()
        name = add_team_var.get()
        try:
            pts = int(add_points_entry.get())
        except ValueError:
            messagebox.showwarning("Atenção", "Digite um número válido!")
            return
        for team in teams:
            if team['nome'] == name:
                team['pontos'] += pts
                save_teams(teams)
                add_points_entry.delete(0, "end")
                messagebox.showinfo("✅", f"+{pts} pontos para {name}!")
                return
        messagebox.showwarning("Atenção", "Selecione uma equipe válida!")

    ctk.CTkButton(
        scroll, text="Adicionar",
        command=add_points_gui,
        font=("Press Start 2P", 11),
        height=40, corner_radius=0,
        fg_color="transparent", border_width=2,
        border_color="#ff0000", text_color="#ff0000",
        hover_color="#ffcccc"
    ).pack(fill="x", pady=(0, 25))

    #Editar Pontos-------------------------------------------
    ctk.CTkLabel(scroll, text="EDITAR PONTOS",
        font=("Press Start 2P", 11), text_color="#ff0000"
    ).pack(anchor="w", pady=(0, 6))

    edit_team_var = ctk.StringVar(value="Selecione...")
    edit_team_menu = ctk.CTkOptionMenu(
        scroll, variable=edit_team_var,
        values=get_team_names(),
        font=("Press Start 2P", 10),
        fg_color="white", button_color="#ff0000",
        button_hover_color="#cc0000", text_color="#000000",
        dropdown_fg_color="white", dropdown_text_color="#000000",
        corner_radius=0, height=40
    )
    edit_team_menu.pack(fill="x", pady=(0, 6))

    edit_points_entry = ctk.CTkEntry(
        scroll, placeholder_text="Nova pontuação",
        height=40, corner_radius=0,
        fg_color="white", border_color="#ff0000",
        text_color="#000000", font=("Press Start 2P", 11)
    )
    edit_points_entry.pack(fill="x", pady=(0, 6))

    def edit_points_gui():
        teams = load_teams()
        name = edit_team_var.get()
        try:
            pts = int(edit_points_entry.get())
        except ValueError:
            messagebox.showwarning("Atenção", "Digite um número válido!")
            return
        for team in teams:
            if team['nome'] == name:
                team['pontos'] = pts
                save_teams(teams)
                edit_points_entry.delete(0, "end")
                messagebox.showinfo("✅", f"Pontuação de {name} alterada para {pts}!")
                return
        messagebox.showwarning("Atenção", "Selecione uma equipe válida!")

    ctk.CTkButton(
        scroll, text="Salvar",
        command=edit_points_gui,
        font=("Press Start 2P", 11),
        height=40, corner_radius=0,
        fg_color="transparent", border_width=2,
        border_color="#ff0000", text_color="#ff0000",
        hover_color="#ffcccc"
    ).pack(fill="x", pady=(0, 25))

    #Maldição-------------------------------------------------
    ctk.CTkLabel(scroll, text="LANÇAR MALDICAO",
        font=("Press Start 2P", 11), text_color="#ff0000"
    ).pack(anchor="w", pady=(0, 6))

    curse_team_var = ctk.StringVar(value="Selecione...")
    curse_team_menu = ctk.CTkOptionMenu(
        scroll, variable=curse_team_var,
        values=get_team_names(),
        font=("Press Start 2P", 10),
        fg_color="white", button_color="#ff0000",
        button_hover_color="#cc0000", text_color="#000000",
        dropdown_fg_color="white", dropdown_text_color="#000000",
        corner_radius=0, height=40
    )
    curse_team_menu.pack(fill="x", pady=(0, 6))

    curse_entry = ctk.CTkEntry(
        scroll, placeholder_text="A maldição...",
        height=40, corner_radius=0,
        fg_color="white", border_color="#ff0000",
        text_color="#000000", font=("Press Start 2P", 11)
    )
    curse_entry.pack(fill="x", pady=(0, 6))

    curse_label = ctk.CTkLabel(scroll, text="", text_color="#ff0000",
        font=("Press Start 2P", 10), wraplength=500)
    curse_label.pack(pady=(0, 6))

    def launch_curse():
        name = curse_team_var.get()
        curse = curse_entry.get().strip()
        if not curse or name == "Selecione...":
            messagebox.showwarning("Atenção", "Selecione uma equipe e escreva a maldição!")
            return
        curse_label.configure(text=f"{name} foram amaldicoados a:\n{curse}")

    ctk.CTkButton(
        scroll, text="Lançar Maldicao!",
        command=launch_curse,
        font=("Press Start 2P", 11),
        height=40, corner_radius=0,
        fg_color="#ff0000", text_color="white",
        hover_color="#cc0000"
    ).pack(fill="x", pady=(0, 10))

    curse_points_entry = ctk.CTkEntry(
        scroll, placeholder_text="Pontos se cumprir",
        height=40, corner_radius=0,
        fg_color="white", border_color="#ff0000",
        text_color="#000000", font=("Press Start 2P", 11)
    )
    curse_points_entry.pack(fill="x", pady=(0, 6))

    def curse_completed():
        teams = load_teams()
        name = curse_team_var.get()
        try:
            pts = int(curse_points_entry.get())
        except ValueError:
            messagebox.showwarning("Atenção", "Digite os pontos ganhos!")
            return
        for team in teams:
            if team['nome'] == name:
                team['pontos'] += pts
                save_teams(teams)
                curse_points_entry.delete(0, "end")
                curse_label.configure(text="")
                messagebox.showinfo("✅", f"{name} cumpriu e ganhou {pts} pontos!")
                return

    ctk.CTkButton(
        scroll, text="Equipe Cumpriu!",
        command=curse_completed,
        font=("Press Start 2P", 11),
        height=40, corner_radius=0,
        fg_color="transparent", border_width=2,
        border_color="#ff0000", text_color="#ff0000",
        hover_color="#ffcccc"
    ).pack(fill="x", pady=(0, 30))

    def refresh_dropdowns():
        names = get_team_names()
        add_team_menu.configure(values=names)
        edit_team_menu.configure(values=names)
        curse_team_menu.configure(values=names)

#Criação da Interface------------------------------------------------------------------

windll.gdi32.AddFontResourceW("PressStart2P-Regular.ttf")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Ignis")
app.geometry("400x500")
app.configure(fg_color="#e6e6e6")

logo_image = ctk.CTkImage(
    light_image=Image.open("img/pngLogo.png"),
    dark_image=Image.open("img/pngLogo.png"),
    size=(400, 200)
)
ctk.CTkLabel(app, image=logo_image, text="").pack(pady=(40, 10))

ctk.CTkLabel(
    app, text="GameJam Management",
    font=("Press Start 2P", 14),
    text_color="#ff0000"
).pack(pady=(10, 20))

ctk.CTkButton(
    app, text="Painel do Admin",
    command=open_admin,
    font=("Press Start 2P", 12),
    height=50, width=300,
    fg_color="transparent", border_width=2,
    border_color="#ff0000", text_color="#ff0000",
    hover_color="#ffcccc", corner_radius=0
).pack(pady=8)

ctk.CTkButton(
    app, text="Painel do Ranking",
    font=("Press Start 2P", 12),
    height=50, width=300,
    fg_color="transparent", border_width=2,
    border_color="#ff0000", text_color="#ff0000",
    hover_color="#ffcccc", corner_radius=0
).pack(pady=8)

app.mainloop()