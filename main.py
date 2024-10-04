import os
import csv
import json

# Arquivos de armazenamento
USERS_FILE = "users.csv"
SINTOMAS_FILE = "sintomas.json"
UPAS_FILE = "UPAs.json"

# Dicionários para sintomas e usuários
sintomas_doenca = {}
users = []
upas = {}

# pausa e limpa o terminal
def p_c():
    os.system('pause')
    os.system('cls')


# carrega as upas
def load_upas():
    global upas
    try:
        with open(UPAS_FILE, mode='r') as file:
            upas = json.load(file)
    except FileNotFoundError:
        upas = {}


# lista as zonas de UPA disponíveis
def list_zones():
    p_c()
    if upas:
        print("Zonas com UPAs disponíveis:")
        for i, zona in enumerate(upas.keys(), start=1):
            print(f"[{i}] {zona}")
    else:
        print("Nenhuma UPA cadastrada.")
    p_c()


# salva as novas upas
def save_upas():
    with open(UPAS_FILE, mode="w") as file:
        json.dump(upas, file, indent=4)


# encontra as UPAs por zona da cidade
def find_upas():
    p_c()
    zona = input("Digite a zona da cidade que deseja buscar UPAs (ex: Distrito Industrial, Jardim Magnólia, etc.): ")
    upas_source = upas.get(zona, [])

    if upas_source:
        print(f"UPAs na zona {zona}:")
        for upa in upas_source:
            print(f"Nome: {upa}")
    else:
        print(f"Nenhuma UPA encontrada na zona {zona}.")
    p_c()


# adiciona uma nova UPA
def add_upa():
    p_c()
    zona = input("Digite a zona da cidade para a nova UPA: ")
    nome_upa = input("Digite o nome e o endereço da nova UPA: ")

    if zona in upas:
        upas[zona].append(nome_upa)
    else:
        upas[zona] = [nome_upa]

    print("UPA adicionada com sucesso!")
    save_upas()
    p_c()


# atualiza uma UPA
def update_upa():
    p_c()
    zona = input("Digite a zona da cidade da UPA que deseja alterar: ")
    if zona not in upas:
        print(f"Nenhuma UPA encontrada na zona {zona}.")
        p_c()
        return

    print("UPAs atuais na zona:")
    for i, upa in enumerate(upas[zona], start=1):
        print(f"[{i}] {upa}")

    num_upa = int(input("Digite o número da UPA que deseja alterar: ")) - 1
    if num_upa < 0 or num_upa >= len(upas[zona]):
        print("Número inválido.")
        p_c()
        return

    new_upa = input("Digite o novo nome e o endereço da UPA: ")
    upas[zona][num_upa] = new_upa
    print("UPA alterada com sucesso!")
    save_upas()
    p_c()


# 


# carrega os dados dos usuários
def load_users():
    global users
    try:
        with open(USERS_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            users = list(reader)
    except FileNotFoundError:
        users = []


# salva os usuários carregados
def save_users():
    with open(USERS_FILE, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Nome", "E-mail", "Telefone"])
        writer.writeheader()
        writer.writerows(users)


# carrega os sintomas e, em caso de erro, mantém o dicionário vazio
def load_sint():
    global sintomas_doenca
    try:
        with open(SINTOMAS_FILE, mode='r') as file:
            sintomas_doenca = json.load(file)
    except FileNotFoundError:
        sintomas_doenca = {}


# salva os sintomas de doenças já inseridos
def save_sint():
    with open(SINTOMAS_FILE, mode="w") as file:
        json.dump(sintomas_doenca, file, indent=4)


# registra o usuário e guarda essas informações no users.csv através da função já criada "save_users()"
def register():
    p_c()
    user = {
        "Nome": input("Digite seu nome: "),
        "E-mail": input("Digite seu e-mail: "),
        "Telefone": input("Digite seu telefone: ")
    }
    users.append(user)
    print("Usuário registrado com sucesso!")
    save_users()
    p_c()


# lista os usuários do programa já registrados e suas respectivas informações
def list_users():
    p_c()
    if users:
        for user in users:
            print(f"Nome: {user['Nome']}\nE-mail: {user['E-mail']}\nTelefone: {user['Telefone']}\n{'-'*42}")
    else:
        print("Nenhum usuário registrado.")
    p_c()


# procura o usuário específico pelo email, se não for encontrado retorna None
def find_user(email):
    for user in users:
        if user['E-mail'].lower() == email.lower():
            return user
    return None


# altera as informações do usuário caso seja encontrado, em caso de não ser encontrado ele printa "Usuário não encontrado." e fecha a função.
def update_user():
    email = input("Digite o e-mail do usuário que deseja atualizar: ")
    user = find_user(email)  # aqui ou retorna o usuário ou retorna None
    if not user:
        print("Usuário não encontrado.")
        p_c()
        return
    # em caso de encontrar o usuário, o if não será executado e aqui começa a descrição
    print(f"Nome: {user['Nome']}\nE-mail: {user['E-mail']}\nTelefone: {user['Telefone']}")

    options = {"1": "Nome", "2": "E-mail", "3": "Telefone"}
    answ = input("[1] Atualizar Nome\n[2] Atualizar E-mail\n[3] Atualizar Telefone\n[0] Cancelar\nSua resposta: ")
    if answ in options:
        new_value = input(f"Digite o novo {options[answ]}: ")
        user[options[answ]] = new_value
        print(f"{options[answ]} atualizado para {new_value}")
        save_users()
    p_c()


# deleta um usuário específico através do email
def delete_user():
    email = input("Digite o e-mail do usuário que deseja excluir: ")
    user = find_user(email)
    if user:
        users.remove(user)
        print("Usuário excluído com sucesso!")
        save_users()
    else:
        print("Usuário não encontrado.")
    p_c()


# adiciona os sintomas e calcula a doença mais provável
def add_sintomas():
    p_c()
    symptoms = input("Digite seus sintomas separados por vírgulas: ").lower().split(", ")
    results = {}

    for doenca, doenca_sintomas_list in sintomas_doenca.items():
        match_count = len(set(symptoms) & set(doenca_sintomas_list))
        accuracy = match_count / len(doenca_sintomas_list) * 100 if doenca_sintomas_list else 0
        results[doenca] = accuracy

    print("\nResultados da consulta online:")
    for doenca, accuracy in results.items():
        print(f"{doenca}: {accuracy:.2f}% de precisão")
    p_c()


# menu secreto para administradores/programadores
def menu_adm():
    operation = int(input("O que deseja inserir/alterar/excluir?\n[1] Adicionar doença\n[2] Alterar doença\n[3] Adicionar UPA\n[4] Alterar UPA\n[0] Voltar\nSua resposta: "))
    if operation in [1, 2, 3, 4, 0]:
        match operation:
            case 1:
                return
            case 2:
                return
            case 3:
                add_upa()
            case 4:
                update_upa()
            case 0:
                return
    else:
        p_c()
        return menu_adm()


# menu principal
def menu():
    operation = None
    while operation != 0:
        operation = int(input("[1] Cadastrar usuário\n[2] Listar usuários\n[3] Atualizar usuário\n[4] Excluir usuário\n[5] Inserir sintomas\n[6] Listar zonas de UPA\n[7] Buscar UPA\n[0] Sair\nO que deseja fazer?: "))
        if operation in [1, 2, 3, 4, 5, 666, 6, 7, 0]:
            match operation:
                case 1:
                    register()
                case 2:
                    list_users()
                case 3:
                    update_user()
                case 4:
                    delete_user()
                case 5:
                    add_sintomas()
                case 666:
                    menu_adm()
                case 6:
                    list_zones()
                case 7:
                    find_upas()
                case 0:
                    return
        else:
            print("Insira uma operação válida.")
            p_c()


load_sint()  # carrega os sintomas
load_users()  # carrega os usuários
load_upas() # carrega as UPAs
menu()  # inicia o programa
save_sint()  # salva os sintomas ao final da execução
save_users()  # salva os usuários ao final da execução
save_upas() # salva as UPAs