from typing import List, Optional

class Gestor:
    def __init__(self, nome: str, telefone: str, email: str):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.clientes: List["Cliente"] = []
        self.empresas: List["Empresa"] = []

    def add_cliente(self, cliente: "Cliente"):
        if cliente not in self.clientes:
            self.clientes.append(cliente)
            cliente.gestor = self  # Cliente herda gestor da empresa

    def add_empresa(self, empresa: "Empresa"):
        if empresa not in self.empresas:
            self.empresas.append(empresa)
            empresa.gestor = self  # Empresa conhece seu gestor

class Empresa:
    def __init__(self, nome: str, cnpj: str, razao_social: str,
                 rua: str, numero: str, estado: str, cidade: str, cep: str,
                 distribuidora: Optional[str] = None, modalidade: Optional[str] = None,
                 consumo_ponta: Optional[float] = None, consumo_fora_ponta: Optional[float] = None,
                 valor_medio: Optional[float] = None,
                 gestor: Optional[Gestor] = None):
        self.nome = nome
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.rua = rua
        self.numero = numero
        self.estado = estado
        self.cidade = cidade
        self.cep = cep
        self.distribuidora = distribuidora
        self.modalidade = modalidade
        self.consumo_ponta = consumo_ponta
        self.consumo_fora_ponta = consumo_fora_ponta
        self.valor_medio = valor_medio
        self.clientes: List["Cliente"] = []
        self.gestor: Optional[Gestor] = gestor  # referência ao gestor

    def add_cliente(self, cliente: "Cliente"):
        if cliente not in self.clientes:
            self.clientes.append(cliente)
            cliente.empresa = self
            # Cliente herda o gestor da empresa
            if self.gestor:
                self.gestor.add_cliente(cliente)

class Cliente:
    def __init__(self, identificador: str, nome: str, cargo: str, telefone: str, email: str):
        self.identificador = identificador
        self.nome = nome
        self.cargo = cargo
        self.telefone = telefone
        self.email = email
        self.gestor: Optional[Gestor] = None
        self.empresa: Optional[Empresa] = None
