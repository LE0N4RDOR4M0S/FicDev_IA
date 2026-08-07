# Uso de docstrings atua como uma documentação para ajudar os devs

# Argumentos sendo declarados como Type Hints, ou seja, o tipo de dado que a função espera receber e retornar
def calculo_de_imc(peso: float, altura: float) -> float:
    """Calcula o índice de massa corporal (IMC) com base no peso e altura de uma pessoa
    
    Args:
        peso (float): O peso em kilogramas.
        altura (float): A altura em metros.
        
    Returns:
        float: Índice de massa corporal já calculado.
    Examples:
        >>> calculo_de_imc(70, 1.75)
    """
    return peso / (altura ** 2)

help(calculo_de_imc)
print(calculo_de_imc.__doc__)

