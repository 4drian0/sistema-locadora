"""Classe Manutencao: parte da composição Veiculo <>-- Manutencao."""
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .veiculo import Veiculo


class Manutencao:
    """Registro de manutenção de um veículo.

    Não deve ser instanciada diretamente: quem cria o registro é o
    ``Veiculo.registrar_manutencao``. Cada manutenção pertence a um único
    veículo e deixa de existir junto com ele.
    """

    def __init__(self, data: date, tipo_servico: str, custo: float,
                 veiculo: Veiculo) -> None:
        if custo < 0:
            raise ValueError("O custo da manutenção não pode ser negativo.")
        self.data = data
        self.tipo_servico = tipo_servico
        self.custo = custo
        self._veiculo: Optional[Veiculo] = veiculo

    @property
    def veiculo(self) -> Optional[Veiculo]:
        return self._veiculo

    @property
    def ativa(self) -> bool:
        """O registro só existe enquanto pertence a um veículo."""
        return self._veiculo is not None

    def descricao(self) -> str:
        if not self.ativa:
            return f"Manutenção '{self.tipo_servico}' (inexistente: veículo baixado)"
        return (f"{self.data:%d/%m/%Y} - {self.tipo_servico} - "
                f"R$ {self.custo:.2f} - {self._veiculo.placa}")

    def eh_cara(self, limite: float = 1000.0) -> bool:
        return self.custo > limite

    def _invalidar(self) -> None:
        """Chamado apenas pelo Veiculo quando ele é baixado do sistema."""
        self._veiculo = None

    def __str__(self) -> str:
        return self.descricao()