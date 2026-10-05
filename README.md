# Locadora de Veículos — Trabalho Prático 02

Disciplina: Arquitetura de Software — ADS, Bloco IV (2026.2)

Sistema de controle de aluguéis de uma locadora, com herança, associação e composição.

| Relação                | Tipo       |
|------------------------|------------|
| Veículo → Carro/Moto/Caminhão | Herança |
| Cliente → Pessoa Física/Jurídica | Herança |
| Cliente — Contrato     | Associação |
| Veículo — Contrato     | Associação |
| Contrato — Condutor    | Composição |
| Veículo — Manutenção   | Composição |

## Como executar (Python 3.9+)

```bash
python main.py                  # demonstração
python -m unittest discover -v  # testes
```

## Estrutura

```
locadora/   # classes do domínio
tests/      # testes unitários
docs/       # análise e diagrama UML
main.py     # demonstração
```

## Convenção de branches

- `feature/*` — novas funcionalidades
- `docs/*` — documentação

Cada branch é integrada à `main` com `git merge --no-ff`.