import tkinter as tk
import random
import time
import os

class Funcionario:
    def __init__(self, cod, nome, cpf, data_nasc, salario):
        self.cod = cod
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.salario = salario

codigos_disponiveis = list(range(10000))

def criar_funcionario_aleatorio():
    if codigos_disponiveis:
        cod = random.choice(codigos_disponiveis)
        codigos_disponiveis.remove(cod)
        nome = f"Funcionário {cod}"
        cpf = str(random.randint(10000000000, 99999999999))
        data_nasc = f"{random.randint(1, 31)}/{random.randint(1, 12)}/{random.randint(1970, 2000)}"
        salario = str(random.randint(2000, 10000))

        func = Funcionario(cod, nome, cpf, data_nasc, salario)
        return func
    else:
        return None

def criar_arquivo_funcionarios():
    quantidade = 10000

    funcionarios = []

    for _ in range(quantidade):
        func = criar_funcionario_aleatorio()
        if func:
            funcionarios.append(func)

    with open('funcionarios.txt', 'w') as arquivo:
        for func in funcionarios:
            arquivo.write(f"Código: {func.cod}\n"
                          f"Nome: {func.nome}\n"
                          f"CPF: {func.cpf}\n"
                          f"Data de Nascimento: {func.data_nasc}\n"
                          f"Salário: {func.salario}\n\n")

    atualizar_lista_funcionarios()

def atualizar_lista_funcionarios():
    text_funcionarios.delete("1.0", tk.END)
    with open('funcionarios.txt', 'r') as arquivo:
        funcionarios = arquivo.read()
    text_funcionarios.insert(tk.END, funcionarios)

def buscar_funcionario_sequencial(cod):
    comp = 0
    start_time = time.time()

    encontrado = False
    funcionario_encontrado = None
    with open('funcionarios.txt', 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith("Código:"):
                func_cod = int(linha.split(":")[1].strip())
                comp += 1
                if func_cod == int(cod):
                    encontrado = True
                    nome = arquivo.readline().split(":")[1].strip()
                    cpf = arquivo.readline().split(":")[1].strip()
                    data_nasc = arquivo.readline().split(":")[1].strip()
                    salario = arquivo.readline().split(":")[1].strip()
                    funcionario_encontrado = Funcionario(func_cod, nome, cpf, data_nasc, salario)
                    break

    end_time = time.time()
    elapsed_time = end_time - start_time
    return encontrado, elapsed_time, comp, funcionario_encontrado

def buscar_funcionario_binaria(cod):
    comp = 0
    start_time = time.time()

    encontrado = False
    funcionario_encontrado = None

    with open('funcionarios.txt', 'r') as arquivo:
        funcionarios = arquivo.readlines()

    esquerda = 0
    direita = len(funcionarios) // 6 - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        comp += 1
        linha_meio = funcionarios[meio * 6]  # Pular 6 linhas para acessar o próximo código
        func_cod = int(linha_meio.split(":")[1].strip())
        if func_cod == int(cod):
            encontrado = True
            nome = funcionarios[meio * 6 + 1].split(":")[1].strip()
            cpf = funcionarios[meio * 6 + 2].split(":")[1].strip()
            data_nasc = funcionarios[meio * 6 + 3].split(":")[1].strip()
            salario = funcionarios[meio * 6 + 4].split(":")[1].strip()
            funcionario_encontrado = Funcionario(func_cod, nome, cpf, data_nasc, salario)
            break
        elif func_cod < int(cod):
            esquerda = meio + 1
        else:
            direita = meio - 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    return encontrado, elapsed_time, comp, funcionario_encontrado

def ordenar_funcionarios():
    comp = 0
    start_time = time.time()

    funcionarios = []

    with open('funcionarios.txt', 'r') as arquivo:
        lines = arquivo.readlines()
        for i in range(0, len(lines), 6):
            cod = int(lines[i].split(":")[1].strip())
            nome = lines[i+1].split(":")[1].strip()
            cpf = lines[i+2].split(":")[1].strip()
            data_nasc = lines[i+3].split(":")[1].strip()
            salario = lines[i+4].split(":")[1].strip()

            func = Funcionario(cod, nome, cpf, data_nasc, salario)
            funcionarios.append(func)

    funcionarios.sort(key=lambda func: func.cod)

    with open('funcionarios.txt', 'w') as arquivo:
        for func in funcionarios:
            arquivo.write(f"Código: {func.cod}\n"
                          f"Nome: {func.nome}\n"
                          f"CPF: {func.cpf}\n"
                          f"Data de Nascimento: {func.data_nasc}\n"
                          f"Salário: {func.salario}\n\n")

    end_time = time.time()
    elapsed_time = end_time - start_time
    return funcionarios, elapsed_time, comp

def criar_arquivo_ordenado():
    funcionarios, elapsed_time, comp = ordenar_funcionarios()
    atualizar_lista_funcionarios()

    text_info.delete("1.0", tk.END)
    text_info.insert(tk.END, f"Ordenação concluída em {elapsed_time:.6f} segundos\n"
                              f"Número de comparações: {comp}\n")

def mostrar_informacoes_funcionario(funcionario):
    text_funcionarios.delete("1.0", tk.END)
    if funcionario:
        text_funcionarios.insert(tk.END, f"Código: {funcionario.cod}\n"
                                         f"Nome: {funcionario.nome}\n"
                                         f"CPF: {funcionario.cpf}\n"
                                         f"Data de Nascimento: {funcionario.data_nasc}\n"
                                         f"Salário: {funcionario.salario}\n")
    else:
        text_funcionarios.insert(tk.END, "Funcionário não encontrado.\n")

def buscar_funcionario():
    cod = entry_search.get()

    metodo = var_metodo_busca.get()

    if metodo == "Sequencial":
        encontrado, tempo, comp, funcionario_encontrado = buscar_funcionario_sequencial(cod)
    else:
        encontrado, tempo, comp, funcionario_encontrado = buscar_funcionario_binaria(cod)

    mostrar_informacoes_funcionario(funcionario_encontrado)

    text_info.delete("1.0", tk.END)
    text_info.insert(tk.END, f"Tempo de busca: {tempo:.6f} segundos\n"
                              f"Número de comparações: {comp}\n")

# Interface gráfica
window = tk.Tk()
window.title("Gerenciamento de Funcionários")
window.geometry("500x600")

button_adicionar = tk.Button(window, text="Criar Arquivo de Funcionários", command=criar_arquivo_funcionarios)
button_adicionar.pack()

label_search = tk.Label(window, text="Buscar Funcionário (Código):")
label_search.pack()

entry_search = tk.Entry(window)
entry_search.pack()

var_metodo_busca = tk.StringVar(value="Sequencial")

radio_sequencial = tk.Radiobutton(window, text="Busca Sequencial", variable=var_metodo_busca, value="Sequencial")
radio_sequencial.pack()

radio_binaria = tk.Radiobutton(window, text="Busca Binária", variable=var_metodo_busca, value="Binária")
radio_binaria.pack()

button_buscar = tk.Button(window, text="Buscar", command=buscar_funcionario)
button_buscar.pack()

label_funcionarios = tk.Label(window, text="Funcionários:")
label_funcionarios.pack()

text_funcionarios = tk.Text(window, height=15, width=60)
text_funcionarios.pack()

button_ordenar = tk.Button(window, text="Criar Arquivo Ordenado", command=criar_arquivo_ordenado)
button_ordenar.pack()

label_info = tk.Label(window, text="Informações:")
label_info.pack()

text_info = tk.Text(window, height=3, width=60)
text_info.pack()

window.mainloop()
