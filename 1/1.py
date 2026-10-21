import json
from dataclasses import dataclass

@dataclass
class Venda:
    vendedor: str
    valor: float

    def comissao(self) -> float:
        if self.valor < 100:
            return 0
        elif self.valor < 500:
            return self.valor * 0.01
        else:
            return self.valor * 0.05

if __name__ == '__main__':
    try:
        # leitura do JSON de entrada
        with open('entrada.json', 'r') as f:
            dados = json.load(f)
    except ValueError as e:
        print(f'Erro ao ler JSON: {e}')

    vendas_json = dados.get("vendas", [])
    vendas = [Venda(**v) for v in vendas_json]

    vendedores = {}
    
    for v in vendas:
        vendedores[v.vendedor] = vendedores.get(v.vendedor, 0) + v.comissao()


    for k, v in vendedores.items():
        print(f'Vendedor: {k:<15} | Comissão: R${v:.2f}')
