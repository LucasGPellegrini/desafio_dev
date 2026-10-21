import uuid
import json
from dataclasses import dataclass, field
from time import sleep
import os

def _CLEAR():
    os.system('cls' if os.name == 'nt' else 'clear')

@dataclass 
class Movimentacao:
    descricao_movimentacao: str
    quantidade: int
    id_unico: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Produto:
    codigo_produto: int
    descricao_produto: str
    estoque: int

    @classmethod
    def from_dict(cls, d: dict) -> Produto:
        return cls(
            codigo_produto=d["codigoProduto"],
            descricao_produto=d["descricaoProduto"],
            estoque=d["estoque"],
        )

REPOR = "Repor estoque"
REMOVER = "Remover do estoque"
 
def movimentar_produto(
    estoque: dict[int, Produto], 
    movimentacoes: list[Movimentacao]
) -> None:
    _CLEAR()
    try:
        codigo = int(input("Qual o código do produto? "))
    except ValueError as _:
        print("Código inválido")
        sleep(2)
        return
 
    produto = estoque.get(codigo, None)
    if produto is None:
        print(f"Produto {codigo} não encontrado.")
        sleep(2)
        return
 
    confirma = None
    while confirma not in ["SIM", "NÃO"]:
        _CLEAR()
        print(produto)
        print("Deseja movimentar este produto? (SIM/NÃO)")
        confirma = input("[SIM/NÃO] ")

    if confirma == "NÃO":
        return
 
    tipo = None
    while tipo not in [REPOR, REMOVER]:
        _CLEAR()
        print(produto)
        print("Que tipo de movimentação deseja fazer?")
        print(f"A. {REPOR}")
        print(f"B. {REMOVER}")
        opcao = input()
        if opcao.upper() == 'A':
            tipo = REPOR
        elif opcao.upper() == 'B':
            tipo = REMOVER
        else:
            print("Operação inválida")
            sleep(2)

 
    if tipo == REPOR:
        try:
            quantidade = int(input("Qual a quantidade de produtos? "))
        except ValueError as _:
            print("Quantidade inválida")
            sleep(2)
            return
        if  quantidade < 1:
            print("Quantidade inválida")
            sleep(2)
            return
        produto.estoque += quantidade
    else:
        try:
            quantidade = int(input(f"Qual a quantidade de produtos? (máx. {produto.estoque}) "))
        except ValueError as _:
            print("Quantidade inválida")
            sleep(2)
            return
        if quantidade > produto.estoque or quantidade < 1:
            print("Quantidade inválida")
            sleep(2)
            return
        produto.estoque -= quantidade
 
    movimentacoes.append(
        Movimentacao(
            descricao_movimentacao = tipo,
            quantidade = quantidade
        )
    )
    print(f"Feito. Estoque atual: {produto.estoque}")
    sleep(2)
 
 
def main(
    estoque: dict[int, Produto], 
    movimentacoes: list[Movimentacao]
) -> None:
    while True:
        opcao = None
        while opcao not in ["A", "B", "C", "D"]:
            _CLEAR()
            print("O que deseja fazer agora?")
            print("A. Listar estoque")
            print("B. Movimentar produto")
            print("C. Listar movimentações")
            print("D. Sair")
            opcao = input().upper()

 
        if opcao == "A":
            print(estoque)
            sleep(5)
        elif opcao == "B":
            movimentar_produto(estoque, movimentacoes)
        elif opcao == "C":
            print(movimentacoes)
            sleep(5)
        else:
            break

if __name__ == '__main__':
    try:
        # leitura do JSON de entrada
        with open('entrada.json', 'r') as f:
            dados = json.load(f)
    except ValueError as e:
        print(f'Erro ao ler JSON: {e}')

    estoque_json = dados.get("estoque", [])
    estoque = [Produto.from_dict(p) for p in estoque_json]
    inventario = {p.codigo_produto : p for p in estoque}

    movimentacoes = []

    main(inventario, movimentacoes)
