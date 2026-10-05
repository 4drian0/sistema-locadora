import unittest

from locadora.cliente import Cliente, PessoaFisica, PessoaJuridica


class TestHerancaCliente(unittest.TestCase):
    def setUp(self):
        self.pf = PessoaFisica("Ana Souza", "123.456.789-00", "(81) 99999-0000")
        self.pj = PessoaJuridica("Transportes Alfa Ltda", "12.345.678/0001-90", "(81) 3333-0000")

    def test_subclasses_sao_clientes(self):
        self.assertIsInstance(self.pf, Cliente)
        self.assertIsInstance(self.pj, Cliente)

    def test_cliente_e_abstrato(self):
        with self.assertRaises(TypeError):
            Cliente("X", "000", "0")

    def test_documentos(self):
        self.assertEqual(self.pf.cpf, "123.456.789-00")
        self.assertEqual(self.pj.cnpj, "12.345.678/0001-90")
        self.assertEqual(self.pj.razao_social, "Transportes Alfa Ltda")

    def test_documento_invalido(self):
        with self.assertRaises(ValueError):
            PessoaFisica("Ana", "123", "1")
        with self.assertRaises(ValueError):
            PessoaJuridica("Alfa", "123.456.789-00", "1")

    def test_desconto_polimorfico(self):
        self.assertEqual(self.pf.desconto(), 0.0)
        self.assertEqual(self.pj.desconto(), 0.10)

    def test_atualizar_telefone(self):
        self.pf.atualizar_telefone("(81) 98888-1111")
        self.assertEqual(self.pf.telefone, "(81) 98888-1111")


if __name__ == "__main__":
    unittest.main()