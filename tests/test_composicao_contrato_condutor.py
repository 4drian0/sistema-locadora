import unittest
from datetime import date

from locadora.cliente import PessoaFisica, PessoaJuridica
from locadora.contrato import Contrato, StatusContrato
from locadora.veiculo import Carro


def novo_contrato(cliente, veiculo, dias=3):
    return Contrato(cliente, veiculo, date(2026, 10, 1), date(2026, 10, 1 + dias),
                    "Carlos Lima", "12345678901")


class TestComposicaoContratoCondutor(unittest.TestCase):
    def setUp(self):
        self.pf = PessoaFisica("Ana Souza", "123.456.789-00", "8199990000")
        self.pj = PessoaJuridica("Alfa Ltda", "12.345.678/0001-90", "8133330000")
        self.carro = Carro("AAA-1111", "Onix", 2022, 100)

    def test_contrato_cria_o_condutor(self):
        c = novo_contrato(self.pf, self.carro)
        self.assertTrue(c.condutor.ativo)
        self.assertIs(c.condutor.contrato, c)
        self.assertEqual(c.condutor.cnh, "12345678901")

    def test_excluir_contrato_destroi_condutor(self):
        c = novo_contrato(self.pf, self.carro)
        condutor = c.condutor
        c.excluir()
        self.assertFalse(condutor.ativo)
        with self.assertRaises(RuntimeError):
            condutor.dados_para_contrato()

    def test_excluir_libera_veiculo_e_remove_do_cliente(self):
        c = novo_contrato(self.pf, self.carro)
        c.excluir()
        self.assertTrue(self.carro.esta_disponivel())
        self.assertEqual(self.pf.listar_contratos(), ())

    def test_excluir_duas_vezes(self):
        c = novo_contrato(self.pf, self.carro)
        c.excluir()
        with self.assertRaises(RuntimeError):
            c.excluir()

    def test_cnh_invalida(self):
        with self.assertRaises(ValueError):
            Contrato(self.pf, self.carro, date(2026, 10, 1), date(2026, 10, 3), "X", "123")
        self.assertTrue(self.carro.esta_disponivel())


class TestAssociacaoContrato(unittest.TestCase):
    def setUp(self):
        self.pf = PessoaFisica("Ana Souza", "123.456.789-00", "8199990000")
        self.pj = PessoaJuridica("Alfa Ltda", "12.345.678/0001-90", "8133330000")
        self.carro = Carro("AAA-1111", "Onix", 2022, 100)

    def test_veiculo_nao_pode_ter_dois_contratos_ativos(self):
        novo_contrato(self.pf, self.carro)
        with self.assertRaises(RuntimeError):
            novo_contrato(self.pj, self.carro)

    def test_veiculo_volta_a_ficar_disponivel_ao_finalizar(self):
        c = novo_contrato(self.pf, self.carro)
        c.finalizar()
        self.assertEqual(c.status, StatusContrato.FINALIZADO)
        self.assertTrue(self.carro.esta_disponivel())
        novo_contrato(self.pj, self.carro)

    def test_cancelar(self):
        c = novo_contrato(self.pf, self.carro)
        c.cancelar()
        self.assertEqual(c.status, StatusContrato.CANCELADO)
        with self.assertRaises(RuntimeError):
            c.finalizar()

    def test_valor_total_pessoa_fisica_e_juridica(self):
        self.assertEqual(novo_contrato(self.pf, self.carro, dias=3).valor_total, 300.0)
        outro = Carro("BBB-2222", "Gol", 2021, 100)
        self.assertEqual(novo_contrato(self.pj, outro, dias=3).valor_total, 270.0)

    def test_cliente_lista_seus_contratos(self):
        c = novo_contrato(self.pf, self.carro)
        self.assertEqual(self.pf.listar_contratos(), (c,))
        self.assertEqual(self.pf.contratos_ativos(), (c,))
        c.finalizar()
        self.assertEqual(self.pf.contratos_ativos(), ())

    def test_cliente_e_veiculo_sobrevivem_ao_contrato(self):
        c = novo_contrato(self.pf, self.carro)
        c.excluir()
        self.assertEqual(self.pf.nome, "Ana Souza")
        self.assertEqual(self.carro.placa, "AAA-1111")

    def test_datas_invalidas(self):
        with self.assertRaises(ValueError):
            Contrato(self.pf, self.carro, date(2026, 10, 5), date(2026, 10, 1),
                     "X", "12345678901")

    def test_nao_baixa_veiculo_com_contrato_ativo(self):
        novo_contrato(self.pf, self.carro)
        with self.assertRaises(RuntimeError):
            self.carro.baixar()


if __name__ == "__main__":
    unittest.main()