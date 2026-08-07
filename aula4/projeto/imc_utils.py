def validar_peso(peso_str: float) -> bool:
    """Valida o peso informado pelo usuário.
    Args:
        peso_str (float): Peso informado pelo usuário.
    Returns:
        bool: True se o peso for válido, False caso contrário.
    """
    
    try:
        peso = float(peso_str)
        return 0 < peso < 500
    except ValueError:
        print("Peso inválido. Informe um valor numérico.")
        return False

def validar_altura(altura_str: float) -> bool:
    """Valida a altura informada pelo usuário.
    Args:
        altura_str (float): Altura informada pelo usuário.
    Returns:
        bool: True se a altura for válida, False caso contrário.
    """
    try:
        altura = float(altura_str)
        return 0.5 < altura < 3.0
    except ValueError:
        print("Altura inválida. Informe um valor numérico.")
        return False

def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o índice de massa corporal
    Args:
        peso (float): Peso em kg.
        altura (float): Altura em metros.
    Returns:
        float: Índice de massa corporal (IMC), calculado como peso / (altura ** 2).
    """
    
    return peso / (altura ** 2)

def classificar_imc(imc: float) -> tuple[str, str]:
    """Classifica o índice de massa corporal (IMC) de acordo com a tabela da OMS.
    Args:
        imc (float): Índice de massa corporal.
    Returns:
        tuple[str, str]: Classificação do IMC e recomendação correspondente.
    """
    
    if imc < 18.5:
        return "Abaixo do peso", "Consulte um nutricionista para avaliação."
    elif imc < 25.0:
        return "Peso normal", "Excelente! Continue mantendo hábitos saudáveis."
    elif imc < 30.0:
        return "Sobrepeso", "Atenção: considere ajustes na dieta e exercícios."
    elif imc < 35.0:
        return "Obesidade Grau I", "Recomendado acompanhamento médico."
    elif imc < 40.0:
        return "Obesidade Grau II", "Importante: procure orientação médica."
    else:
        return "Obesidade Grau III", "Urgente: consulte um médico imediatamente."
    
def formatar_resultado(**resultados) -> str:
    """Formata o resultado do cálculo do IMC para exibição.
    Args:
        **resultados: Resultados do cálculo do imc, incluindo nome, peso, altura, imc, classificação e recomendação.
    Returns:
        str: Resultado formatado para exibição.
    """
    resultado_formatado = "\n" + "=" * 50 + "\n"
    for chave, valor in resultados.items():
        resultado_formatado += f"{chave} : {valor}\n"
    resultado_formatado += "=" * 50 + "\n"
    return resultado_formatado

def coletar_dados() -> tuple[str, float, float]:
    """Coleta todos os dados necessários do usuaŕio
    Returns:
        tuple[str, float, float]: Nome, peso e altura do usuário.
    """
    nome = input("\nDigite seu nome: ").strip().capitalize()
    while True:
        peso_str = input("Peso em kg (ex: 70.5): ")
        if validar_peso(peso_str):
            break
        print("Peso inválido. Informe um valor numérico válido.")
    while True:
        altura_str = input("Altura em metros (ex: 1.75): ")
        if validar_altura(altura_str):
            break
        print("Altura inválida. Informe um valor numérico válido.")
    
    return nome, peso_str, altura_str