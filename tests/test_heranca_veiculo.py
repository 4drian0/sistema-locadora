import unittest

from locadora.veiculo import Caminhao, Carro, Moto, Veiculo


class TestHerancaVeiculo(unittest.TestCase):
    def test_subclasses_sao_veiculos(self):
        for v in (Carro("AAA-1111", "Onix", 2022, 150),
                  Moto("BBB-2222", "CG 160", 2023, 70),
                  Caminhao("CCC-3333", "Volvo FH", 2021, 400)):
            self.assertIsInstance(v, Veiculo)

    def test_veiculo_e_abstrato(self):
        with self.assertRaises(TypeError):
            Veiculo("XXX-0000", "Qualquer", 2020, 100)

    def test_atributos_comuns(self):
        c = Carro("AAA-1111", "Onix", 2022, 150)
        self.assertEqual((c.placa, c.modelo, c.ano, c.valor_diaria),
                         ("AAA-1111", "Onix", 2022, 150))

    def test_atributos_especificos(self):
        self.assertEqual(Moto("B", "CG", 2023, 70, cilindradas=250).cilindradas, 250)
        self.assertEqual(Carro("A", "Onix", 2022, 150, portas=2).portas, 2)

    def test_polimorfismo_da_diaria(self):
        self.assertEqual(Carro("A", "Onix", 2022, 150).calcular_diaria(), 150)
        self.assertEqual(Caminhao("C", "FH", 2021, 400, capacidade_toneladas=10).calcular_diaria(), 550)

    def test_tipo(self):
        self.assertEqual(Moto("B", "CG", 2023, 70).tipo, "Moto")

    def test_diaria_invalida(self):
        with self.assertRaises(ValueError):
            Carro("A", "Onix", 2022, 0)


if __name__ == "__main__":
    unittest.main()