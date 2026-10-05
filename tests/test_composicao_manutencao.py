import unittest
from datetime import date

from locadora.veiculo import Carro


class TestComposicaoVeiculoManutencao(unittest.TestCase):
    def setUp(self):
        self.carro = Carro("AAA-1111", "Onix", 2022, 150)

    def test_veiculo_cria_manutencao_e_e_dono_dela(self):
        m = self.carro.registrar_manutencao(date(2026, 1, 10), "Troca de óleo", 250)
        self.assertIs(m.veiculo, self.carro)
        self.assertEqual(self.carro.historico_manutencoes(), (m,))

    def test_varias_manutencoes_no_historico(self):
        self.carro.registrar_manutencao(date(2026, 1, 10), "Troca de óleo", 250)
        self.carro.registrar_manutencao(date(2026, 3, 5), "Freios", 800)
        self.assertEqual(len(self.carro.historico_manutencoes()), 2)
        self.assertEqual(self.carro.custo_total_manutencao(), 1050)

    def test_baixar_veiculo_destroi_manutencoes(self):
        m = self.carro.registrar_manutencao(date(2026, 1, 10), "Troca de óleo", 250)
        self.carro.baixar()
        self.assertFalse(m.ativa)
        self.assertEqual(self.carro.historico_manutencoes(), ())

    def test_veiculo_baixado_nao_recebe_manutencao(self):
        self.carro.baixar()
        with self.assertRaises(RuntimeError):
            self.carro.registrar_manutencao(date(2026, 1, 10), "Freios", 800)

    def test_custo_negativo(self):
        with self.assertRaises(ValueError):
            self.carro.registrar_manutencao(date(2026, 1, 10), "Freios", -1)

    def test_eh_cara(self):
        m = self.carro.registrar_manutencao(date(2026, 1, 10), "Motor", 3000)
        self.assertTrue(m.eh_cara())


if __name__ == "__main__":
    unittest.main()