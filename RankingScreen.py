import os
import json
import customtkinter as ctk
from tkinter import messagebox

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

def add_points(teams):
    while True:
        clear()
        print("=== PONTUAÇÃO ===")
        for i, team in enumerate(teams, start=1):
            print(f"  {i}. {team['nome']} - {team['pontos']} pontos")
        
        print("\nO que deseja fazer?")
        print("  1. Adicionar pontos")
        print("  2. Encerrar e ver ranking final")
        print("  3. Editar Pontos")
        print("  4. Lançar Maldição")
        
        option = input("\nEscolha uma opção: ")
        
        if option == '1':
            number = int(input("Digite o número da equipe: "))
            if 1 <= number <= len(teams):
                points = int(input("Quantos pontos?: "))
                teams[number - 1]['pontos'] += points
                save_teams(teams)
                print(f"Pontos adicionados com sucesso!")
            else:
                print("Equipe inválida!")
        
        elif option == '2':
            clear()
            print("=== RANKING FINAL ===")
            ranking = sorted(teams, key=lambda x: x['pontos'], reverse=True)
            for i, team in enumerate(ranking, start=1):
                print(f"  {i}. {team['nome']} - {team['pontos']} pontos")
            break
        elif option == '3':
            print("=== EDITANDO PONTOS ===")
            edit_points(teams)
        elif option == '4':
            print("\nHora de lançar maldições!")
            launch_challenge(teams)
        else:
            print("\nOpção inválida")

def edit_points(teams):
    clear()
    print("=== EDITANDO PONTOS ===")
    for i, team in enumerate(teams, start=1):
        print(f"  {i}. {team['nome']} - {team['pontos']} pontos")
    
    while True:
        try:
            number = int(input("\nDigite o número da equipe: "))
            break
        except ValueError:
            continue
    if 1 <= number <= len(teams):
        while True:
            try: 
                newPoints = int(input("Digite a nova pontuação da equipe: "))
                teams[number - 1]['pontos'] = newPoints
                save_teams(teams)
                print("Pontos alterados com sucesso!")
                break
            except ValueError:
                print ("Digite um número por favor")
                continue
    else:
        print("Equipe inválida!")

def launch_challenge(teams):
    clear()
    print("\nQual equipe você gostaria de amaldiçoar?\n")
    for i, team in enumerate(teams, start=1):
        print(f"  {i}. {team['nome']} - {team['pontos']} pontos")
    
    number = int(input("\nDigite o número da equipe: "))
    if 1 <= number <= len(teams):
        curse = input("Digite a maldição: ")
        print(f"A equipe {teams[number - 1]['nome']} foi amaldiçoada a: {curse}")
    
    print("A maldição foi concluída? (S/N): ")
    curseAnswear = input("Digite sua resposta: ")

    if curseAnswear == 'S' or curseAnswear == 's':
        add_points(teams)
    else:
        print("Equipe penalizada!")

#Criação da Interface------------------------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("LevelUp!Jam!")
app.geometry("500x600")

# (botões, labels, etc.)
# label = ctk.CTkLabel(app, text="Olá!")
# label.pack()

app.mainloop()
