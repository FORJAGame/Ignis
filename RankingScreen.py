import os
import json

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


    
#Código principal----------------------------------------------------------

teams = load_teams()

clear()

print("=== LevelUp!Jam! ===")
print("\nO que deseja fazer?\n \n1.Lançar Desafios! \n2.Pontuar Equipes")

menuAnswear = input("\nDigite sua resposta: ")

if menuAnswear == '1':

    if len(teams) == 0:
        answear = input("\nNenhuma equipe registrada, deseja registrar equipes? (S/N): ")
        if answear == 'S' or answear == 's':
            print("\nVamos registrar nossas equipes!")
            
            while True:
                name = input("Digite o nome da equipe (ou 'sair' para terminar): ")
                if name.lower() == 'sair':
                    break
                newTeam = create_teams(name)
                teams.append(newTeam)
            
            save_teams(teams)
            print("Equipes registradas com sucesso!")
            add_points(teams)
        else:
            print("Até mais!")
    else:
        launch_challenge(teams)

elif menuAnswear == '2':


    if len(teams) == 0:
        answear = input("\nNenhuma equipe registrada, deseja registrar equipes? (S/N): ")
        if answear == 'S' or answear == 's':
            print("\nVamos registrar nossas equipes!")
            
            while True:
                name = input("Digite o nome da equipe (ou 'sair' para terminar): ")
                if name.lower() == 'sair':
                    break
                newTeam = create_teams(name)
                teams.append(newTeam)
            
            save_teams(teams)
            print("Equipes registradas com sucesso!")
            add_points(teams)
        else:
            print("Até mais!")
    else:
        print("\nEquipes registradas:")
        for i, team in enumerate(teams, start=1):
            print(f"  {i}. {team['nome']} - {team['pontos']} pontos")
        
        answear = input("\nDeseja continuar a pontuação dessas equipes? (S/N): ")
        if answear == 'S' or answear == 's':
            print("Continuando pontuação!")
            add_points(teams)
        else:
            print("Até mais!")

    
