"""Demonstração do sistema de locadora de veículos."""
import sys
from datetime import date

from locadora.cliente import PessoaFisica, PessoaJuridica
from locadora.contrato import Contrato
from locadora.veiculo import Caminhao, Carro, Moto

# Garante UTF-8 no terminal (evita "�" no Windows / Code Runner)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def demo_heranca() -> None:
    titulo("HERANÇA: Veículo e Cliente")
    veiculos = [
        Carro("ABC-1D23", "Chevrolet Onix", 2022, 150.0),
        Moto("DEF-4E56", "Honda CG 160", 2023, 70.0, cilindradas=160),
        Caminhao("GHI-7F89", "Volvo FH", 2021, 400.0, capacidade_toneladas=10),
    ]
    for v in veiculos:
        print(" -", v)

    clientes = [
        PessoaFisica("Ana Souza", "123.456.789-00", "(81) 99999-0000"),
        PessoaJuridica("Transportes Alfa Ltda", "12.345.678/0001-90", "(81) 3333-0000"),
    ]
    for c in clientes:
        print(f" - {c} (desconto: {c.desconto():.0%})")


def demo_composicao_contrato_condutor() -> None:
    titulo("COMPOSIÇÃO: Contrato e Condutor")
    ana = PessoaFisica("Ana Souza", "123.456.789-00", "(81) 99999-0000")
    onix = Carro("ABC-1D23", "Chevrolet Onix", 2022, 150.0)

    contrato = Contrato(ana, onix, date(2026, 10, 10), date(2026, 10, 15),
                        "Carlos Lima", "12345678901")
    print(contrato)
    condutor = contrato.condutor
    print(" -", condutor)

    print("Tentando alugar o mesmo carro para outro cliente:")
    alfa = PessoaJuridica("Transportes Alfa Ltda", "12.345.678/0001-90", "(81) 3333-0000")
    try:
        Contrato(alfa, onix, date(2026, 10, 11), date(2026, 10, 12), "Rui Melo", "10987654321")
    except RuntimeError as erro:
        print(" - Bloqueado:", erro)

    contrato.excluir()
    print("Depois de excluir o contrato:")
    print(" -", condutor)
    print(" - veículo disponível?", onix.esta_disponivel())


def demo_composicao_manutencao() -> None:
    titulo("COMPOSIÇÃO: Veículo e Manutenção")
    moto = Moto("DEF-4E56", "Honda CG 160", 2023, 70.0)
    m1 = moto.registrar_manutencao(date(2026, 3, 12), "Troca de óleo", 120.0)
    moto.registrar_manutencao(date(2026, 8, 2), "Troca de pneus", 650.0)
    print("Histórico:")
    for m in moto.historico_manutencoes():
        print(" -", m)
    print(f"Custo total: R$ {moto.custo_total_manutencao():.2f}")

    moto.baixar()
    print("Depois de baixar a moto:")
    print(" -", m1)


if __name__ == "__main__":
    demo_heranca()
    demo_composicao_contrato_condutor()
    demo_composicao_manutencao()