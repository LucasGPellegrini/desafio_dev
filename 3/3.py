from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

TAXA = Decimal("0.025") # 2.5%

def calcular_atraso(
    vencimento: date, 
) -> int:
    hoje = date.today()
    return max((hoje - vencimento).days, 0)

def calcular_juros(
    valor: Decimal, 
    vencimento: date, 
) -> Decimal:
    dias_atraso = calcular_atraso(vencimento)
    juros = valor * TAXA * dias_atraso
    return juros.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ler_valor(prompt: str) -> Decimal:
    while True:
        texto = input(prompt).strip().replace(".", "").replace(",", ".")
        try:
            valor = Decimal(texto)
            if valor > 0:
                return valor
        except ArithmeticError:
            pass
        print("Valor inválido. Ex.: 1.250,90")


def ler_data(prompt: str) -> date:
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")


def brl(v: Decimal) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    valor = ler_valor("Valor da conta (XXXX,XX): ")
    vencimento = ler_data("Data de vencimento (dd/mm/aaaa): ")

    atraso = calcular_atraso(vencimento)
    juros = calcular_juros(valor, vencimento)

    print(f"Dias de atraso: {atraso}")
    print(f"Juros (2,5% ao dia): {brl(juros)}")
    print(f"Total a pagar hoje: {brl(valor + juros)}")


if __name__ == "__main__":
    main()
