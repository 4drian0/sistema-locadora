"""Hierarquia de clientes: pessoa física e pessoa jurídica."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .contrato import Contrato


def _so_digitos(texto: str) -> str:
    return "".join(c for c in texto if c.isdigit())


class Cliente(ABC):
    """Superclasse de PessoaFisica e PessoaJuridica.

    Cliente e Contrato são uma associação: o cliente existe independente de
    ter ou não contratos.
    """

    DIGITOS_DOCUMENTO = 0

    def __init__(self, nome: str, documento: str, telefone: str) -> None:
        if len(_so_digitos(documento)) != self.DIGITOS_DOCUMENTO:
            raise ValueError(
                f"Documento inválido: esperado {self.DIGITOS_DOCUMENTO} dígitos.")
        self.nome = nome
        self.documento = documento
        self.telefone = telefone
        self._contratos: list[Contrato] = []

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Pessoa Física ou Pessoa Jurídica."""

    def desconto(self) -> float:
        """Percentual de desconto (0 a 1) aplicado ao valor do contrato."""
        return 0.0

    def listar_contratos(self) -> tuple[Contrato, ...]:
        return tuple(self._contratos)

    def contratos_ativos(self) -> tuple[Contrato, ...]:
        return tuple(c for c in self._contratos if c.ativo)

    def _registrar_contrato(self, contrato: Contrato) -> None:
        if contrato not in self._contratos:
            self._contratos.append(contrato)

    def _remover_contrato(self, contrato: Contrato) -> None:
        if contrato in self._contratos:
            self._contratos.remove(contrato)

    def atualizar_telefone(self, novo: str) -> None:
        self.telefone = novo

    def __str__(self) -> str:
        return f"{self.tipo}: {self.nome} - doc. {self.documento} - tel. {self.telefone}"


class PessoaFisica(Cliente):
    """Cliente identificado por CPF."""

    DIGITOS_DOCUMENTO = 11

    def __init__(self, nome: str, cpf: str, telefone: str) -> None:
        super().__init__(nome, cpf, telefone)

    @property
    def cpf(self) -> str:
        return self.documento

    @property
    def tipo(self) -> str:
        return "Pessoa Física"


class PessoaJuridica(Cliente):
    """Cliente identificado por CNPJ (razão social no lugar do nome)."""

    DIGITOS_DOCUMENTO = 14
    DESCONTO_EMPRESARIAL = 0.10

    def __init__(self, razao_social: str, cnpj: str, telefone: str) -> None:
        super().__init__(razao_social, cnpj, telefone)

    @property
    def razao_social(self) -> str:
        return self.nome

    @property
    def cnpj(self) -> str:
        return self.documento

    @property
    def tipo(self) -> str:
        return "Pessoa Jurídica"

    def desconto(self) -> float:
        return self.DESCONTO_EMPRESARIAL