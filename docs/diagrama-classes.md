# Diagrama de classes UML

Notação: seta vazada = herança, linha simples = associação, losango vazado =
agregação, losango preenchido = composição.

```mermaid
classDiagram
    direction LR

    class Veiculo {
        <<abstract>>
        -str placa
        -str modelo
        -int ano
        -float valor_diaria
        +calcular_diaria() float
        +esta_disponivel() bool
        +registrar_manutencao(data, tipo_servico, custo) Manutencao
        +historico_manutencoes() tuple
        +custo_total_manutencao() float
        +baixar()
    }
    class Carro {
        -int portas
        -bool ar_condicionado
    }
    class Moto {
        -int cilindradas
        -bool partida_eletrica
    }
    class Caminhao {
        -float capacidade_toneladas
        -int eixos
        +calcular_diaria() float
    }

    class Cliente {
        <<abstract>>
        -str nome
        -str documento
        -str telefone
        +desconto() float
        +listar_contratos() tuple
        +contratos_ativos() tuple
        +atualizar_telefone(novo)
    }
    class PessoaFisica {
        +cpf
    }
    class PessoaJuridica {
        +razao_social
        +cnpj
        +desconto() float
    }

    class Contrato {
        -int numero
        -date data_inicio
        -date data_termino_prevista
        -float valor_total
        -StatusContrato status
        +duracao_dias() int
        +calcular_valor_total() float
        +finalizar()
        +cancelar()
        +excluir()
    }
    class Condutor {
        -str nome
        -str cnh
        +descricao() str
        +dados_para_contrato() dict
    }
    class Manutencao {
        -date data
        -str tipo_servico
        -float custo
        +descricao() str
        +eh_cara() bool
    }

    Veiculo <|-- Carro
    Veiculo <|-- Moto
    Veiculo <|-- Caminhao
    Cliente <|-- PessoaFisica
    Cliente <|-- PessoaJuridica

    Cliente "1" -- "0..*" Contrato : realiza (associação)
    Veiculo "1" -- "0..*" Contrato : é alugado em (associação)
    Contrato "1" *-- "1" Condutor : possui (composição)
    Veiculo "1" *-- "0..*" Manutencao : tem histórico (composição)
```

O diagrama aparece renderizado direto no GitHub. Para exportar como imagem,
cole o código em https://mermaid.live.