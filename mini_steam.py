import random

class Jogo:
    def __init__(self, jogo_id, titulo, desenvolvedor, preco, generos):
        self.jogo_id = jogo_id
        self.titulo = titulo
        self.desenvolvedor = desenvolvedor
        self.preco = preco
        self.generos = generos # Lista, pois um jogo pode pertencer a múltiplos gêneros

class NoJogo:
    def __init__(self, jogo):
        self.jogo = jogo
        self.esquerda = None
        self.direita = None

class ArvoreJogos:
    def __init__(self):
        self.raiz = None

    def inserir(self, jogo):
        self.raiz = self._inserir(self.raiz, jogo)

    def _inserir(self, no_jogo, jogo):
        if no_jogo is None:
            return NoJogo(jogo)
        elif jogo.preco < no_jogo.jogo.preco:
            if no_jogo.esquerda is None:
                no_jogo.esquerda = NoJogo(jogo)
            else:
                no_jogo.esquerda = self._inserir(no_jogo.esquerda, jogo)
        else:
            if no_jogo.direita is None:
                no_jogo.direita = NoJogo(jogo)
            else:
                no_jogo.direita = self._inserir(no_jogo.direita, jogo)

        return self._balancear(no_jogo)

    def _altura(self, no_jogo):
        if no_jogo is None:
            return 0
        altura_esquerda = self._altura(no_jogo.esquerda)
        altura_direita = self._altura(no_jogo.direita)
        return max(altura_esquerda, altura_direita) + 1

    def _fator_equilibrio(self, no_jogo):
        if no_jogo is None:
            return 0
        altura_esquerda = self._altura(no_jogo.esquerda)
        altura_direita = self._altura(no_jogo.direita)
        return altura_esquerda - altura_direita

    def _rotacao_esquerda(self, x):
        if x is None or x.direita is None:
            return x

        y = x.direita
        T2 = y.esquerda

        y.esquerda = x
        x.direita = T2

        return y

    def _rotacao_direita(self, y):
        if y is None or y.esquerda is None:
            return y
        
        x = y.esquerda
        T2 = x.direita

        x.direita = y
        y.esquerda = T2

        return x

    def _balancear(self, no_jogo):
        if no_jogo is None:
            return no_jogo

        fator_equilibrio = self._fator_equilibrio(no_jogo)

        if fator_equilibrio > 1 and no_jogo.jogo.preco < no_jogo.esquerda.jogo.preco:
            return self._rotacao_direita(no_jogo)

        if fator_equilibrio < -1 and no_jogo.jogo.preco > no_jogo.direita.jogo.preco:
            return self._rotacao_esquerda(no_jogo)

        if fator_equilibrio > 1 and no_jogo.jogo.preco > no_jogo.esquerda.jogo.preco:
            no_jogo.esquerda = self._rotacao_esquerda(no_jogo.esquerda)
            return self._rotacao_direita(no_jogo)

        if fator_equilibrio < -1 and no_jogo.jogo.preco < no_jogo.direita.jogo.preco:
            no_jogo.direita = self._rotacao_direita(no_jogo.direita)
            return self._rotacao_esquerda(no_jogo)

        return no_jogo

    def buscar_por_preco(self, preco, no_jogo):
        jogos = []
        if no_jogo is not None:
            if no_jogo.jogo.preco == preco:
                jogos.append(no_jogo.jogo)
                jogos.extend(self.buscar_por_preco(preco, no_jogo.direita))
                jogos.extend(self.buscar_por_preco(preco, no_jogo.esquerda))
            elif no_jogo.jogo.preco < preco:
                jogos.extend(self.buscar_por_preco(preco, no_jogo.direita))
            else :
                jogos.extend(self.buscar_por_preco(preco, no_jogo.esquerda))
    
        return jogos

    def buscar_por_faixa_preco(self, preco_minimo, preco_maximo, no_jogo):
        jogos = []
        if no_jogo is not None:
            if no_jogo.jogo.preco >= preco_minimo and no_jogo.jogo.preco <= preco_maximo:
                jogos.append(no_jogo.jogo)
                jogos.extend(self.buscar_por_faixa_preco(preco_minimo, preco_maximo, no_jogo.direita))
                jogos.extend(self.buscar_por_faixa_preco(preco_minimo, preco_maximo, no_jogo.esquerda))
            elif no_jogo.jogo.preco < preco_minimo:
                jogos.extend(self.buscar_por_faixa_preco(preco_minimo, preco_maximo, no_jogo.direita))
            else :
                jogos.extend(self.buscar_por_faixa_preco(preco_minimo, preco_maximo, no_jogo.esquerda))

        return jogos

class HashGeneros:
    def __init__(self):
        self.genero_para_jogos = {}
    def adicionar_jogo(self, jogo):
        if jogo.generos is not None:
            for genero in jogo.generos:
                if genero in self.genero_para_jogos:
                    self.genero_para_jogos[genero].append(jogo)
                else:
                    self.genero_para_jogos[genero] = [jogo]

    def obter_jogos(self, genero):
        if genero in self.genero_para_jogos:
            return self.genero_para_jogos[genero]
        else:
            return []

class NoJogoTrie:
    def __init__(self, letra):
        self.letra = letra
        self.filhos = {}
        self.jogo = None
    
class ArvoreTrie:
    def __init__(self):
        self.raiz = NoJogoTrie("")

    def inserir(self, jogo):
        nodo_atual = self.raiz
        for letra in jogo.titulo:
            if letra not in nodo_atual.filhos:
                nodo_atual.filhos[letra] = NoJogoTrie(letra)
            nodo_atual = nodo_atual.filhos[letra]
        nodo_atual.jogo = jogo

    def pesquisar(self, titulo):
        nodo_atual = self.raiz
        for letra in titulo:
            if letra not in nodo_atual.filhos:
                return None
            nodo_atual = nodo_atual.filhos[letra]
        return nodo_atual.jogo



class MotorBuscaJogos:
    def __init__(self):
        self.catalogo_jogos = ArvoreJogos()
        self.generos = HashGeneros()

    def gerar_catalogo(self, quantidade_jogos):
        palavras = ['Liga das Legendas', 'Bom de Guerra 2', 'redenção do morto vermelho', 'grande roubo de carros 5', 'preciso de velocidade mais procurado', 'residencia maligna', 'inquilimo mal', 'trombada de guenshin', 'contra ataque 2 ofensiva global', 'não morra de fome junto', 'engrenagem metalica solída 5 a dor fantasma', 'cinco noitadas no freddys', 'chora longe primata', 'mod do gary', 'meia vida 2', 'linha quente de miami', 'choque biologico infinito', 'esquerda pra matar', 'a vida é estrnha', 'rapazes que caem', 'festa dura', 'engrenagens da guerra', 'medo de fantasma', 'risco da chuva 2', 'o diabo talvez vá chorar', 'assistindo cachorros', 'o bruxo 3 caçada selvagem', 'cabeça de xícara', 'final fantasia xv', 'cai fora', 'anel pristino', 'pato pato ganso', 'lutadores de rua 5']
        generos = ['RPG', 'FPS', 'Estratégia', 'Estratégia por Turno', 'Estratégia em tempo real', 'Simulação', 'Corrida', 'Tiro', 'Plataforma', 'Competitivo']
        desenvolvedores = ['Tencent', 'Electronic Arts', 'Activision', 'Ubisoft', 'Square Enix', 'Bandai Namco', 'Konami', 'Namco']

        catalogo = []
        for i in range (quantidade_jogos):
            jogo_id = i
            jogo_titulo = random.choice(palavras)
            jogo_desenvolvedor = random.choice(desenvolvedores)
            jogo_preco = random.randint(0, 1000)
            jogo_generos = random.sample(generos, random.randint(1, 3))
            catalogo.append(Jogo(jogo_id, jogo_titulo, jogo_desenvolvedor, jogo_preco, jogo_generos))

        return catalogo
    
    def mostrar_jogo(self, jogo):
        print(f'Titulo: {jogo.titulo} | Id: {jogo.jogo_id}')
        print(f'Desenvolvedor: {jogo.desenvolvedor} \nPreço: {jogo.preco}')
        print('Gêneros:')
        for genero in jogo.generos:
            print(f'\t- {genero}')

    def mostrar_arvore(self, no_jogo):
        if no_jogo is not None:
            self.mostrar_arvore(no_jogo.esquerda)
            self.mostrar_jogo(no_jogo.jogo)
            self.mostrar_arvore(no_jogo.direita)

    def mostrar_jogos(self, game_list):
        for jogo in game_list:
            self.mostrar_jogo(jogo)

    def inserir_jogos(self, catalogo):
        for jogo in catalogo:
            self.catalogo_jogos.inserir(jogo)
            self.generos.adicionar_jogo(jogo)

    def buscar_por_preco(self, preco):
        return self.catalogo_jogos.buscar_por_preco(preco, self.catalogo_jogos.raiz)

    def buscar_por_faixa_preco(self, preco_minimo, preco_maximo):
        return self.catalogo_jogos.buscar_por_faixa_preco(preco_minimo, preco_maximo, self.catalogo_jogos.raiz)

    def buscar_por_genero(self, genero):
        return self.generos.obter_jogos(genero)
