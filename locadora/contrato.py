"""Classe Contrato: associa Cliente e Veiculo e é o "todo" da composição com Condutor."""
from __future__ import annotations

import itertools
from datetime import date
from enum import Enum

from .cliente import Cliente
from .condutor import Condutor
from .veiculo import Veiculo


class StatusContrato(Enum):
    ATIVO = "ativo"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


class Contrato:
    """Contrato de locação.

    - Associação com ``Cliente`` e ``Veiculo``: o contrato aponta para eles,
      mas nenhum dos dois depende do contrato para existir.
    - Composição com ``Condutor``: o condutor é criado dentro do contrato e
      deixa de existir quando o contrato é excluído.
    """

    _contador = itertools.count(1)

    def __init__(self, cliente: Cliente, veiculo: Veiculo,
                 data_inicio: date, data_termino_prevista: date,
                 nome_condutor: str, cnh_condutor: str) -> None:
        if data_termino_prevista < data_inicio:
            raise ValueError("A data de término não pode ser anterior ao início.")
        self.numero = next(Contrato._contador)
        self.cliente = cliente
        self.veiculo = veiculo
        self.data_inicio = data_inicio
        self.data_termino_prevista = data_termino_prevista
        self._status = StatusContrato.ATIVO
        self._excluido = False

        # Composição: o Contrato cria o seu Condutor.
        self._condutor = Condutor(nome_condutor, cnh_condutor, self)
        self.valor_total = self.calcular_valor_total()

        veiculo._reservar(self)  # falha se o veículo já tem contrato ativo
        cliente._registrar_contrato(self)

    @property
    def status(self) -> StatusContrato:
        return self._status

    @property
    def ativo(self) -> bool:
        return self._status is StatusContrato.ATIVO

    @property
    def condutor(self) -> Condutor:
        return self._condutor

    def duracao_dias(self) -> int:
        """Número de diárias (mínimo de 1)."""
        return max((self.data_termino_prevista - self.data_inicio).days, 1)

    def calcular_valor_total(self) -> float:
        bruto = self.duracao_dias() * self.veiculo.calcular_diaria()
        return round(bruto * (1 - self.cliente.desconto()), 2)

    def finalizar(self) -> None:
        self._exigir_ativo()
        self._status = StatusContrato.FINALIZADO
        self.veiculo._liberar(self)

    def cancelar(self) -> None:
        self._exigir_ativo()
        self._status = StatusContrato.CANCELADO
        self.veiculo._liberar(self)

    def excluir(self) -> None:
        """Exclui o contrato: o condutor deixa de existir junto com ele."""
        if self._excluido:
            raise RuntimeError("Este contrato já foi excluído.")
        self.veiculo._liberar(self)
        self.cliente._remover_contrato(self)
        self._condutor._invalidar()
        self._excluido = True

    def _exigir_ativo(self) -> None:
        if not self.ativo:
            raise RuntimeError(f"O contrato {self.numero} não está ativo.")

    def __str__(self) -> str:
        return (f"Contrato #{self.numero} [{self._status.value}] - {self.cliente.nome} / "
                f"{self.veiculo.placa} - {self.data_inicio:%d/%m/%Y} a "
                f"{self.data_termino_prevista:%d/%m/%Y} - R$ {self.valor_total:.2f}")