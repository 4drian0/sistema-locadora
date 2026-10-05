"""Hierarquia de veículos e o lado "todo" da composição com Manutencao."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING, Optional

from .manutencao import Manutencao

if TYPE_CHECKING:
    from .contrato import Contrato


class Veiculo(ABC):
    """Superclasse de Carro, Moto e Caminhao.

    Reúne o que todo veículo tem em comum (placa, modelo, ano, valor da
    diária) e é o "todo" da composição com ``Manutencao``.
    """

    def __init__(self, placa: str, modelo: str, ano: int, valor_diaria: float) -> None:
        if valor_diaria <= 0:
            raise ValueError("O valor da diária deve ser maior que zero.")
        self.placa = placa
        self.modelo = modelo
        self.ano = ano
        self.valor_diaria = valor_diaria
        self._manutencoes: list[Manutencao] = []
        self._contrato_ativo: Optional[Contrato] = None
        self._baixado = False

    # ---- Comportamento polimórfico ---------------------------------------
    @property
    @abstractmethod
    def tipo(self) -> str:
        """Nome do tipo de veículo (Carro, Moto, Caminhão)."""

    def calcular_diaria(self) -> float:
        """Valor cobrado por dia. Subclasses podem acrescentar adicionais."""
        return self.valor_diaria

    # ---- Disponibilidade (um veículo, um contrato ativo) -----------------
    @property
    def contrato_ativo(self) -> Optional[Contrato]:
        return self._contrato_ativo

    def esta_disponivel(self) -> bool:
        return not self._baixado and self._contrato_ativo is None

    def _reservar(self, contrato: Contrato) -> None:
        """Chamado apenas pelo Contrato ao ser aberto."""
        if not self.esta_disponivel():
            raise RuntimeError(f"O veículo {self.placa} não está disponível.")
        self._contrato_ativo = contrato

    def _liberar(self, contrato: Contrato) -> None:
        """Chamado apenas pelo Contrato ao ser finalizado, cancelado ou excluído."""
        if self._contrato_ativo is contrato:
            self._contrato_ativo = None

    # ---- Composição: Veiculo <>-- Manutencao -----------------------------
    def registrar_manutencao(self, data: date, tipo_servico: str, custo: float) -> Manutencao:
        if self._baixado:
            raise RuntimeError("Um veículo baixado não pode receber manutenções.")
        manutencao = Manutencao(data, tipo_servico, custo, self)
        self._manutencoes.append(manutencao)
        return manutencao

    def historico_manutencoes(self) -> tuple[Manutencao, ...]:
        return tuple(self._manutencoes)

    def custo_total_manutencao(self) -> float:
        return sum(m.custo for m in self._manutencoes)

    def baixar(self) -> None:
        """Retira o veículo do sistema: o histórico de manutenções some junto."""
        if self._contrato_ativo is not None:
            raise RuntimeError("Não é possível baixar um veículo com contrato ativo.")
        for manutencao in self._manutencoes:
            manutencao._invalidar()
        self._manutencoes.clear()
        self._baixado = True

    def __str__(self) -> str:
        situacao = "disponível" if self.esta_disponivel() else "indisponível"
        return (f"{self.tipo} {self.modelo} ({self.ano}) - placa {self.placa} - "
                f"R$ {self.calcular_diaria():.2f}/dia - {situacao}")


class Carro(Veiculo):
    """Carro: acrescenta número de portas e ar-condicionado."""

    def __init__(self, placa: str, modelo: str, ano: int, valor_diaria: float,
                 portas: int = 4, ar_condicionado: bool = True) -> None:
        super().__init__(placa, modelo, ano, valor_diaria)
        self.portas = portas
        self.ar_condicionado = ar_condicionado

    @property
    def tipo(self) -> str:
        return "Carro"


class Moto(Veiculo):
    """Moto: acrescenta cilindradas e partida elétrica."""

    def __init__(self, placa: str, modelo: str, ano: int, valor_diaria: float,
                 cilindradas: int = 160, partida_eletrica: bool = True) -> None:
        super().__init__(placa, modelo, ano, valor_diaria)
        self.cilindradas = cilindradas
        self.partida_eletrica = partida_eletrica

    @property
    def tipo(self) -> str:
        return "Moto"


class Caminhao(Veiculo):
    """Caminhão: acrescenta capacidade de carga, que gera adicional na diária."""

    ADICIONAL_POR_TONELADA = 15.0

    def __init__(self, placa: str, modelo: str, ano: int, valor_diaria: float,
                 capacidade_toneladas: float = 5.0, eixos: int = 2) -> None:
        super().__init__(placa, modelo, ano, valor_diaria)
        self.capacidade_toneladas = capacidade_toneladas
        self.eixos = eixos

    @property
    def tipo(self) -> str:
        return "Caminhão"

    def calcular_diaria(self) -> float:
        return self.valor_diaria + self.capacidade_toneladas * self.ADICIONAL_POR_TONELADA