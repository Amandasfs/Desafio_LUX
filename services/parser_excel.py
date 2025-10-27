#/services/parser_excel.py
import pandas as pd
from model.models import Cliente, Empresa, Gestor


def carregar_dados_excel(caminho_arquivo: str):
    """
    Lê um arquivo Excel com dados brutos e converte em objetos do modelo.
    Retorna (clientes, empresas, gestores)
    """
    try:
        df = pd.read_excel(caminho_arquivo)
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo Excel: {e}")

    gestores = {}
    empresas = {}
    clientes = []

    # Remover linhas completamente vazias
    df.dropna(how="all", inplace=True)

    for _, row in df.iterrows():
        try:
            # === Gestor ===
            nome_gestor = str(row.get("Gestor Responsável (LUX)", "")).strip()
            if nome_gestor:
                if nome_gestor not in gestores:
                    gestores[nome_gestor] = Gestor(
                        nome=nome_gestor,
                        telefone="5151-2525",  # pode vir do Excel se houver
                        email=f"{nome_gestor.lower().replace(' ', '')}@luxenergia.com.br"
                    )

            # === Empresa ===
            nome_empresa = str(row.get("Empresa", "")).strip()
            if nome_empresa:
                if nome_empresa not in empresas:
                    # Conversões seguras
                    def parse_num(valor):
                        if pd.isna(valor):
                            return 0.0
                        valor = str(valor).replace("R$", "").replace(".", "").replace(",", ".")
                        try:
                            return float(valor)
                        except ValueError:
                            return 0.0

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
                        valor_medio=parse_num(row.get("Valor Médio da Fatura (R$)", 0))
                    )

            # === Cliente ===
            identificador = str(row.get("Identificador", "")).strip()
            nome_cliente = str(row.get("Nome", "")).strip()
            if nome_cliente:
                cliente = Cliente(
                    identificador=identificador,
                    nome=nome_cliente,
                    cargo=str(row.get("Cargo", "")).strip(),
                    telefone=str(row.get("Telefone", "")).strip(),
                    email=str(row.get("e-mail", "")).strip()
                )

                # Relacionamentos
                if nome_empresa in empresas:
                    cliente.empresa = empresas[nome_empresa]

                if nome_gestor in gestores:
                    gestores[nome_gestor].add_cliente(cliente)

                clientes.append(cliente)

        except Exception as e:
            print(f"[Aviso] Erro ao processar linha: {e}")

    return clientes, list(empresas.values()), list(gestores.values())

def carregar_dados():
    # Facilita o uso no dashboard
    _, empresas, gestores = carregar_dados_excel("./dados_brutos.xlsx")
    import pandas as pd

    # Recarrega também o DataFrame para visualização direta
    df = pd.read_excel("./dados_brutos.xlsx")
    return df
