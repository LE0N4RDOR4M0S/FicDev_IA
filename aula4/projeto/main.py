import imc_utils


def main():
    print("=" * 50)
    print(" CALCULADORA DE IMC")
    print(" Índice de Massa Corporal — OMS")
    print("=" * 50)
    
    nome, peso_str, altura_str = imc_utils.coletar_dados()

    peso = float(peso_str)
    altura = float(altura_str)
    imc = imc_utils.calcular_imc(peso, altura)
    classificacao, recomendacao = imc_utils.classificar_imc(imc)
    print(imc_utils.formatar_resultado(
        nome=nome,
        peso=peso,
        altura=altura,
        imc=imc,
        classificacao=classificacao,
        recomendacao=recomendacao
    ))
    
main()