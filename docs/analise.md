# Análise do estudo de caso: Locadora de Veículos

## 1. Identificação de classes

`Veiculo` (abstrata), `Carro`, `Moto`, `Caminhao`, `Cliente` (abstrata),
`PessoaFisica`, `PessoaJuridica`, `Contrato`, `Condutor`, `Manutencao`
e a enumeração `StatusContrato` (ativo, finalizado, cancelado).

## 2. Atributos e métodos

| Classe          | Atributos                                                    | Métodos                                                                                     |
|-----------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Veiculo         | placa, modelo, ano, valor_diaria                             | calcular_diaria, esta_disponivel, registrar_manutencao, historico_manutencoes, custo_total_manutencao, baixar |
| Carro           | (herdados) + portas, ar_condicionado                         | tipo                                                                                        |
| Moto            | (herdados) + cilindradas, partida_eletrica                   | tipo                                                                                        |
| Caminhao        | (herdados) + capacidade_toneladas, eixos                     | tipo, calcular_diaria (acrescenta adicional por tonelada)                                   |
| Cliente         | nome, documento, telefone                                    | desconto, listar_contratos, contratos_ativos, atualizar_telefone                            |
| PessoaFisica    | (herdados) + cpf                                             | tipo                                                                                        |
| PessoaJuridica  | (herdados) + razao_social, cnpj                              | tipo, desconto (10% para empresas)                                                          |
| Contrato        | numero, cliente, veiculo, data_inicio, data_termino_prevista, valor_total, status | duracao_dias, calcular_valor_total, finalizar, cancelar, excluir        |
| Condutor        | nome, cnh                                                    | descricao, dados_para_contrato                                                              |
| Manutencao      | data, tipo_servico, custo                                    | descricao, eh_cara                                                                          |

## 3. Herança

Há duas hierarquias de generalização/especialização:

- **Veiculo → Carro, Moto, Caminhao.** O enunciado diz que os três tipos
  "compartilham informações básicas como placa, modelo, ano e valor da
  diária" e têm "características próprias". Os atributos comuns ficam na
  superclasse e cada subclasse acrescenta os seus (portas, cilindradas,
  capacidade de carga). O caminhão ainda especializa `calcular_diaria`
  (polimorfismo).
- **Cliente → PessoaFisica, PessoaJuridica.** Ambos têm nome/razão social,
  documento e telefone; mudam o tipo de documento (CPF ou CNPJ) e a regra de
  desconto.

## 4. Relacionamentos entre classes

| Par de classes        | Tipo       | Cardinalidade | Justificativa                                                                                          |
|-----------------------|------------|---------------|--------------------------------------------------------------------------------------------------------|
| Cliente — Contrato    | Associação | 1 — 0..*      | O contrato aponta para exatamente um cliente, mas o cliente existe antes e depois de qualquer contrato. Nenhum é "parte" do outro. |
| Veiculo — Contrato    | Associação | 1 — 0..*      | O contrato vincula um veículo específico (e ele não pode estar em dois contratos ativos), mas o veículo tem vida própria. |
| Contrato — Condutor   | Composição | 1 — 1         | O condutor é cadastrado na locação, só existe associado a um contrato e, se o contrato é excluído, seus dados perdem o sentido. |
| Veiculo — Manutencao  | Composição | 1 — 0..*      | Cada manutenção pertence a um único veículo e compõe o histórico dele; sem o veículo, o registro não faz sentido. |

Observação: o enunciado diz que "cada veículo possui um condutor
responsável", mas que o condutor "só existe associado a um contrato". Por
isso o condutor foi ligado ao **contrato** (não diretamente ao veículo): o
veículo chega ao condutor pelo contrato ativo.

## 5. Implementação parcial

Relacionamento principal: **Contrato ◆— Condutor** (composição), em
`locadora/contrato.py` e `locadora/condutor.py`. O `Contrato` instancia o
`Condutor` dentro do próprio construtor e, em `excluir()`, invalida o
condutor. Também foi implementada, como complemento, a composição
**Veiculo ◆— Manutencao**.