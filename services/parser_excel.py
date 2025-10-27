import pandas as pd
from model.models import Cliente, Empresa, Gestor

def carregar_dados_excel(caminho_arquivo: str):
    df = pd.read_excel(caminho_arquivo)
    df.dropna(how="all", inplace=True)

    gestores = {}
    empresas = {}
    clientes = []

    def parse_num(valor):
        if pd.isna(valor):
            return 0.0
        valor = str(valor).replace("R$", "").replace(".", "").replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            return 0.0

    # Primeiro, cria todas as empresas
    for _, row in df.iterrows():
        nome_empresa = str(row.get("Empresa", "")).strip()
        if not nome_empresa:
            continue

        # Cria ou recupera gestor da empresa
        nome_gestor = str(row.get("Gestor Responsável (LUX)", "")).strip()
        if nome_gestor:
            if nome_gestor not in gestores:
                gestores[nome_gestor] = Gestor(
                    nome=nome_gestor,
                    telefone="5151-2525",
                    email=f"{nome_gestor.lower().replace(' ', '')}@luxenergia.com.br"
                )
            gestor_empresa = gestores[nome_gestor]
        else:
            gestor_empresa = None

        if nome_empresa not in empresas:
            empresas[nome_empresa] = Empresa(
                nome=nome_empresa,
                cnpj=str(row.get("CNPJ", "")).strip(),
                razao_social=str(row.get("Razão Social", "")).strip(),
                rua=str(row.get("Endereço - Rua", "")).strip(),
                numero=str(row.get("Endereço - Numero", "")).strip(),
                estado=str(row.get("Endereço - Estado", "")).strip(),
                cidade=str(row.get("Endereço - Cidade", "")).strip(),
                cep=str(row.get("Endereço - CEP", "")).strip(),
                distribuidora=str(row.get("Distribuidora", "")).strip(),
                modalidade=str(row.get("Modalidade Tarifária", "")).strip(),
                consumo_ponta=parse_num(row.get("Consumo Ponta (kWh)", 0)),
                consumo_fora_ponta=parse_num(row.get("Consumo Fora Ponta (kWh)", 0)),
                valor_medio=parse_num(row.get("Valor Médio da Fatura (R$)", 0)),
                gestor=gestor_empresa  # associa o gestor à empresa
            )

    # Depois, cria os clientes e associa à empresa e gestor da empresa
    for _, row in df.iterrows():
        tipo = str(row.get("Identificador", "")).strip()
        nome_cliente = str(row.get("Nome", "")).strip()
        if not nome_cliente:
            continue

        cargo = str(row.get("Cargo", "")).strip()
        telefone = str(row.get("Telefone", "")).strip()
        email = str(row.get("e-mail", "")).strip()
        nome_empresa = str(row.get("Empresa", "")).strip()

        cliente = Cliente(
            identificador=tipo,
            nome=nome_cliente,
            cargo=cargo,
            telefone=telefone,
            email=email
        )

        if nome_empresa in empresas:
            empresa_obj = empresas[nome_empresa]
            cliente.empresa = empresa_obj
            empresa_obj.clientes.append(cliente)

            # Cliente herda gestor da empresa
            if empresa_obj.gestor:
                empresa_obj.gestor.add_cliente(cliente)
                empresa_obj.gestor.add_empresa(empresa_obj)

        clientes.append(cliente)

    return clientes, list(empresas.values()), list(gestores.values())
