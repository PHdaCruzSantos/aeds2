import tkinter as tk
import random
import time
import os

class Ingresso:
    def __init__(self, data_compra, valor_ingresso):
        self.data_compra = data_compra
        self.valor_ingresso = valor_ingresso

class Cliente:
    def __init__(self, cod, nome, cpf, ingresso):
        self.cod = cod
        self.nome = nome
        self.cpf = cpf
        self.ingresso = ingresso

codigos_disponiveis = list(range(10000))

def criar_cliente_aleatorio():
    if codigos_disponiveis:
        cod = random.choice(codigos_disponiveis)
        codigos_disponiveis.remove(cod)
        nome = f"Cliente {cod}"
        cpf = str(random.randint(10000000000, 99999999999))
        dia = random.randint(1, 31)
        mes = random.randint(1, 12)
        ano = random.randint(2022, 2023)
        data_compra = f"{dia:02d}/{mes:02d}/{ano}"
        valor_ingresso = random.randint(2000, 10000)

        ingresso = Ingresso(data_compra, valor_ingresso)
        cliente = Cliente(cod, nome, cpf, ingresso)
        return cliente
    else:
        return None

def criar_arquivo_clientes():
    quantidade = 10000

    clientes = []

    for _ in range(quantidade):
        cliente = criar_cliente_aleatorio()
        if cliente:
            clientes.append(cliente)

    with open('clientes.txt', 'w') as arquivo:
        for cliente in clientes:
            arquivo.write(f"Código: {cliente.cod}\n"
                          f"Nome: {cliente.nome}\n"
                          f"CPF: {cliente.cpf}\n"
                          f"Data de Compra: {cliente.ingresso.data_compra}\n"
                          f"Valor: {cliente.ingresso.valor_ingresso}\n\n")

    atualizar_lista_clientes()

def atualizar_lista_clientes():
    text_clientes.delete("1.0", tk.END)
    with open('clientes.txt', 'r') as arquivo:
        clientes = arquivo.read()
    text_clientes.insert(tk.END, clientes)

def buscar_cliente_sequencial(cod):
    comp = 0
    start_time = time.time()

    encontrado = False
    cliente_encontrado = None
    with open('clientes.txt', 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith("Código:"):
                func_cod = int(linha.split(":")[1].strip())
                comp += 1
                if func_cod == int(cod):
                    encontrado = True
                    nome = arquivo.readline().split(":")[1].strip()
                    cpf = arquivo.readline().split(":")[1].strip()
                    data_compra = arquivo.readline().split(":")[1].strip()
                    valor_ingresso = arquivo.readline().split(":")[1].strip()
                    cliente_encontrado = Cliente(func_cod, nome, cpf, Ingresso(data_compra, valor_ingresso))
                    break

    end_time = time.time()
    elapsed_time = end_time - start_time
    return encontrado, elapsed_time, comp, cliente_encontrado

def buscar_cliente_binaria(cod):
    comp = 0
    start_time = time.time()

    encontrado = False
    cliente_encontrado = None

    with open('clientes.txt', 'r') as arquivo:
        clientes = arquivo.readlines()

    esquerda = 0
    direita = len(clientes) // 6 - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        comp += 1
        linha_meio = clientes[meio * 6]  # Pular 6 linhas para acessar o próximo código
        func_cod = int(linha_meio.split(":")[1].strip())
        if func_cod == int(cod):
            encontrado = True
            nome = clientes[meio * 6 + 1].split(":")[1].strip()
            cpf = clientes[meio * 6 + 2].split(":")[1].strip()
            data_compra = clientes[meio * 6 + 3].split(":")[1].strip()
            valor_ingresso = clientes[meio * 6 + 4].split(":")[1].strip()
            ingresso = Ingresso(data_compra, valor_ingresso)
            cliente_encontrado = Cliente(func_cod, nome, cpf, ingresso)
            break
        elif func_cod < int(cod):
            esquerda = meio + 1
        else:
            direita = meio - 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    return encontrado, elapsed_time, comp, cliente_encontrado

def ordenar_clientes():
    comp = 0
    start_time = time.time()

    clientes = []

    with open('clientes.txt', 'r') as arquivo:
        lines = arquivo.readlines()
        for i in range(0, len(lines), 6):
            cod = int(lines[i].split(":")[1].strip())
            nome = lines[i + 1].split(":")[1].strip()
            cpf = lines[i + 2].split(":")[1].strip()
            data_compra = lines[i + 3].split(":")[1].strip()
            valor_ingresso = lines[i + 4].split(":")[1].strip()

            ingresso = Ingresso(data_compra, valor_ingresso)
            cliente = Cliente(cod, nome, cpf, ingresso)
            clientes.append(cliente)

    clientes.sort(key=lambda c: c.cod)

    with open('clientes.txt', 'w') as arquivo:
        for cliente in clientes:
            arquivo.write(f"Código: {cliente.cod}\n"
                          f"Nome: {cliente.nome}\n"
                          f"CPF: {cliente.cpf}\n"
                          f"Data de Compra: {cliente.ingresso.data_compra}\n"
                          f"Valor: {cliente.ingresso.valor_ingresso}\n\n")

    end_time = time.time()
    elapsed_time = end_time - start_time
    return clientes, elapsed_time, comp

def criar_arquivo_ordenado():
    clientes, elapsed_time, comp = ordenar_clientes()
    atualizar_lista_clientes()

    text_info.delete("1.0", tk.END)
    text_info.insert(tk.END, f"Ordenação concluída em {elapsed_time:.6f} segundos\n"
                              f"Número de comparações: {comp}\n")

def mostrar_informacoes_cliente(cliente):
    text_clientes.delete("1.0", tk.END)
    if cliente:
        text_clientes.insert(tk.END, f"Código: {cliente.cod}\n"
                                     f"Nome: {cliente.nome}\n"
                                     f"CPF: {cliente.cpf}\n"
                                     f"Data de Compra: {cliente.ingresso.data_compra}\n"
                                     f"Valor: {cliente.ingresso.valor_ingresso}\n")
    else:
        text_clientes.insert(tk.END, "Cliente não encontrado.\n")

def buscar_cliente():
    cod = entry_search.get()

    metodo = var_metodo_busca.get()

    if metodo == "Sequencial":
        encontrado, tempo, comp, cliente_encontrado = buscar_cliente_sequencial(cod)
    else:
        encontrado, tempo, comp, cliente_encontrado = buscar_cliente_binaria(cod)

    mostrar_informacoes_cliente(cliente_encontrado)

    text_info.delete("1.0", tk.END)
    text_info.insert(tk.END, f"Tempo de busca: {tempo:.6f} segundos\n"
                              f"Número de comparações: {comp}\n")
    
def atualizar_codigos_disponiveis():
    global codigos_disponiveis
    new_range = entry_codigos_disponiveis.get()
    try:
        start, end = map(int, new_range.split('-'))
        codigos_disponiveis = list(range(start, end + 1))
        entry_codigos_disponiveis.delete(0, tk.END)
        entry_codigos_disponiveis.insert(0, new_range)
    except ValueError:
        print("Erro: Insira um intervalo válido no formato 'início-fim' (exemplo: '10000-19999')")

def gerar_arquivo_ordenado_selecao_por_substituicao(tamanho_particao=1000):
    with open('clientes.txt', 'r') as arquivo:
        lines = arquivo.readlines()

    num_particoes = len(lines) // (tamanho_particao * 6) + 1
    for i in range(num_particoes):
        inicio = i * tamanho_particao * 6
        fim = (i + 1) * tamanho_particao * 6
        registros_particao = lines[inicio:fim]

        num_particao_saida = i
        arquivo_saida = open(f"clientes_ordenados_particao_{num_particao_saida}.txt", 'w')

        m = min(tamanho_particao, len(registros_particao) // 6)
        registros_em_memoria = registros_particao[:m * 6]
        registros_congelados = [False] * m

        while any(registros_em_memoria):
            menor_chave = None
            indice_menor_chave = None
            for i in range(0, len(registros_em_memoria), 6):
                if not registros_congelados[i // 6]:
                    chave = int(registros_em_memoria[i].split(":")[1].strip())
                    if menor_chave is None or chave < menor_chave:
                        menor_chave = chave
                        indice_menor_chave = i

            for j in range(6):
                arquivo_saida.write(registros_em_memoria[indice_menor_chave + j])

            indice_proximo_registro = m * 6 + indice_menor_chave + 1
            if indice_proximo_registro >= len(registros_particao):
                registros_congelados[indice_menor_chave // 6] = True
            else:
                for j in range(6):
                    registros_em_memoria[indice_menor_chave + j] = registros_particao[indice_proximo_registro + j]

            if not registros_congelados[indice_menor_chave // 6]:
                proximo_registro = registros_em_memoria[indice_menor_chave]
                chave_proximo_registro = int(proximo_registro.split(":")[1].strip())
                if chave_proximo_registro <= menor_chave:
                    registros_congelados[indice_menor_chave // 6] = True

            if all(registros_congelados):
                arquivo_saida.close()

                registros_congelados = [False] * m

                num_particao_saida += 1
                arquivo_saida = open(f"clientes_ordenados_particao_{num_particao_saida}.txt", 'w')

                registros_em_memoria = registros_particao[m * 6 * num_particao_saida : m * 6 * (num_particao_saida + 1)]

        arquivo_saida.close()

    return num_particao_saida

def intercalacao_otima(num_particoes):
    arquivos_entrada = [open(f"clientes_ordenados_particao_{i}.txt", 'r') for i in range(num_particoes)]

    arquivo_saida = open("clientes_ordenados_intercalados.txt", 'w')

    proximos_registros = []
    for arquivo in arquivos_entrada:
        try:
            proximos_registros.append(arquivo.readline())
        except EOFError:
            proximos_registros.append(None)

    while any(proximos_registros):
        menor_chave = None
        indice_menor_chave = None

        for i, registro in enumerate(proximos_registros):
            if registro:
                chave = int(registro.split(":")[1].strip())
                if menor_chave is None or chave < menor_chave:
                    menor_chave = chave
                    indice_menor_chave = i

        for j in range(6):
            arquivo_saida.write(proximos_registros[indice_menor_chave])
            try:
                proximos_registros[indice_menor_chave] = arquivos_entrada[indice_menor_chave].readline()
            except EOFError:
                proximos_registros[indice_menor_chave] = None

    arquivo_saida.close()
    for arquivo in arquivos_entrada:
        arquivo.close()

    return "clientes_ordenados_intercalados.txt"

def criar_arquivo_ordenado_com_selecao_substituicao():
    tamanho_particao = 10  # Altere aqui o tamanho das partições.
    num_particoes = gerar_arquivo_ordenado_selecao_por_substituicao(tamanho_particao)
    arquivo_intercalado = intercalacao_otima(num_particoes)
    atualizar_lista_clientes()

    text_info.delete("1.0", tk.END)
    text_info.insert(tk.END, f"Arquivo ordenado criado e intercalado.\n")




window = tk.Tk()
window.title("Gerenciamento de Clientes")
window.geometry("500x600")

label_codigos_disponiveis = tk.Label(window, text="Códigos Disponíveis (início-fim):")
label_codigos_disponiveis.pack()

entry_codigos_disponiveis = tk.Entry(window)
entry_codigos_disponiveis.pack()

button_atualizar_codigos = tk.Button(window, text="Atualizar Códigos Disponíveis", command=atualizar_codigos_disponiveis)
button_atualizar_codigos.pack()

button_adicionar = tk.Button(window, text="Criar Arquivo de Clientes", command=criar_arquivo_clientes)
button_adicionar.pack()

label_search = tk.Label(window, text="Buscar Cliente (Código):")
label_search.pack()

entry_search = tk.Entry(window)
entry_search.pack()

var_metodo_busca = tk.StringVar(value="Sequencial")

radio_sequencial = tk.Radiobutton(window, text="Busca Sequencial", variable=var_metodo_busca, value="Sequencial")
radio_sequencial.pack()

radio_binaria = tk.Radiobutton(window, text="Busca Binária", variable=var_metodo_busca, value="Binária")
radio_binaria.pack()

button_buscar = tk.Button(window, text="Buscar", command=buscar_cliente)
button_buscar.pack()

label_clientes = tk.Label(window, text="Clientes:")
label_clientes.pack()

text_clientes = tk.Text(window, height=15, width=60)
text_clientes.pack()

button_ordenar = tk.Button(window, text="Criar Arquivo Ordenado", command=criar_arquivo_ordenado)
button_ordenar.pack()

button_ordenar_com_selecao_substituicao = tk.Button(window, text="Criar Arquivo Ordenado (com Seleção por Substituição)",
                                                   command=criar_arquivo_ordenado_com_selecao_substituicao)
button_ordenar_com_selecao_substituicao.pack()


label_info = tk.Label(window, text="Informações:")
label_info.pack()

text_info = tk.Text(window, height=3, width=60)
text_info.pack()

window.mainloop()