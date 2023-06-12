import cProfile


class Funcionario:
    def __init__(self, cod, nome, cpf, data_nasc, salario) -> None:
        self.cod = cod
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.salario = salario


def salva(func, out):
    with open(out, 'a') as f:
        f.write(f'{func.cod};{func.nome};{func.cpf};{func.data_nasc};{func.salario}\n')

def le(in_):
    with open(in_, 'r') as f:
        for line in f.readlines():
            cod, nome, cpf, data_nasc, salario = line.strip().split(';')
            func = Funcionario(cod, nome, cpf, data_nasc, salario)
            yield func

def tamanho_arquivo(in_):
    with open(in_, 'r') as f:
        return len(f.readlines())
    
def busca_binaria(cod, in_, tam):
    inicio = 0
    fim = tam - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        func = list(le(in_))[meio]
        if int(func.cod) == cod:
            return func
        elif int(func.cod) > cod:
            fim = meio - 1
        else:
            inicio = meio + 1
    return None

def busca_sequencial(cod, in_):
    for func in le(in_):
        if int(func.cod) == cod:
            return func
    return None

def initializate(file, numberRecords):
    with open(file, 'w') as f:
        for i in range(numberRecords):
            f.write(f'{i};nome{i};cpf{i};data_nasc{i};salario{i}\n')

def cria_arquivo(in_, out):
    with open(out, 'w') as f:
        for func in le(in_):
            f.write(f'{func.cod};{func.nome};{func.cpf};{func.data_nasc};{func.salario}\n')

def print_func(func):
    print(f'cod: {func.cod}\nnome: {func.nome}\ncpf: {func.cpf}\ndata_nasc: {func.data_nasc}\nsalario: {func.salario}\n')

def main_bb():
    in_ = 'funcionarios.txt'
    out = 'funcionarios_ordenados.txt'
    cod = 999999
    numberRecords = 1000000
    initializate(in_, numberRecords)
    cria_arquivo(in_, out)
    tam = tamanho_arquivo(out)
    func = busca_binaria(cod, out, tam)
    print('Busca Binaria:')
    print_func(func)

def main_bs():
    in_ = 'funcionarios.txt'
    cod = 999999
    func = busca_sequencial(cod, in_)
    print('Busca Sequencial:')
    print_func(func)


if __name__ == '__main__':
    cProfile.run('main_bb()')
    cProfile.run('main_bs()')
    