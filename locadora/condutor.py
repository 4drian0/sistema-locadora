"""Classe Condutor: parte da composição Contrato <>-- Condutor."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .contrato import Contrato


class Condutor:
    """Condutor responsável pelo veículo durante a locação.

    Não deve ser instanciado diretamente: quem cria o condutor é o
    ``Contrato`` (no momento da locação). Sem contrato, os dados do condutor
    não têm mais motivo para existir.
    """

    def __init__(self, nome: str, cnh: str, contrato: Contrato) -> None:
        if not cnh.isdigit() or len(cnh) != 11:
            raise ValueError("A CNH deve ter 11 dígitos numéricos.")
        self.nome = nome
        self.cnh = cnh
        self._contrato: Optional[Contrato] = contrato

    @property
    def contrato(self) -> Optional[Contrato]:
        return self._contrato

    @property
    def ativo(self) -> bool:
        """O condutor só existe enquanto pertence a um contrato."""
        return self._contrato is not None

    def descricao(self) -> str:
        if not self.ativo:
            return f"Condutor {self.nome} (inexistente: contrato excluído)"
        return f"Condutor {self.nome} - CNH {self.cnh}"

    def dados_para_contrato(self) -> dict[str, str]:
        if not self.ativo:
            raise RuntimeError("Este condutor não existe mais no sistema.")
        return {"nome": self.nome, "cnh": self.cnh}

    def _invalidar(self) -> None:
        """Chamado apenas pelo Contrato quando ele é excluído."""
        self._contrato = None

    def __str__(self) -> str:
        return self.descricao()