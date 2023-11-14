from mini_steam import MotorBuscaJogos

motor = MotorBuscaJogos()
galeria = motor.gerar_catalogo(1024)
motor.inserir_jogos(galeria)

def buscar_por_genero(motor):
    genero = input('Gênero: ')
    return motor.buscar_por_genero(genero)

def buscar_por_preco(motor):
    try:
        preco = int(input('Preço: '))
    except:
        print('Preço inválido')
        return None

    return motor.buscar_por_preco(preco)

def buscar_por_faixa_preco(motor):
    try:
        preco_minimo = int(input('Preço mínimo: '))
        preco_maximo = int(input('Preço máximo: '))
    except:
        print('Preço inválido')
        return None

    return motor.buscar_por_faixa_preco(preco_minimo, preco_maximo)


while(True):    
    print('1 - Buscar por preço')
    print('2 - Buscar por faixa de preço')
    print('3 - Buscar por gênero')
    print('4 - Mostrar todos os jogos')
    print('5 - Sair')
    
    try:
        opcao = int(input('Opção: '))
    
    except:
        print('Opção inválida')
        continue
    
    match opcao:
        case 1:
            jogos = buscar_por_preco(motor)
            motor.mostrar_jogos(jogos)
        
        case 2: 
            jogos = buscar_por_faixa_preco(motor)
            motor.mostrar_jogos(jogos)
        
        case 3:
            jogos = buscar_por_genero(motor)
            motor.mostrar_jogos(jogos)

        case 4:
            motor.mostrar_arvore(motor.catalogo_jogos.raiz)

        case 5:
            break

        case _:
            print('Opção inválida')
            