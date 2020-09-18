# Introdução ao Desenvolvimento de Games 2D com PyGame

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Images/pygame.png)

<figure>
    <blockquote>
        <p>"Game creation keeps on expanding, just like the Universe. That is why I keep making games."</p>
        <footer>
            <cite>— Hideo Kojima</cite>
        </footer>
    </blockquote>
</figure>

## Introdução

**[Pygame](https://www.pygame.org/)** é um conjunto de módulos Python projetados para escrever vídeo-games. O Pygame adiciona funcionalidades à excelente [biblioteca SDL](https://www.libsdl.org/), que significa **Simple DirectMedia Layer**. SDL fornece acesso *cross-platform* aos componentes de hardware de multimídia de nosso sistema, como **som**, **vídeo**, **mouse**, **teclado** e **joystick**. Nos permitindo criar jogos completos e também programas multimídia na linguagem Python.

Pygame é altamente portátil e roda em quase todas as plataformas e sistemas operacionais.

## Instalação

Para instalarmos Pygame em nossa máquina, utilizaremos [pip](https://pypi.org/project/pip/), o instalador de pacotes tradicional do Python. Sendo assim, executaremos o seguinte comando em nosso terminal:

```
pip install pygame
```

Podemos verificar se instalação ocorreu corretamente carregando um dos exemplos embutidos com a biblioteca:

```
python3 -m pygame.examples.aliens
python3 -m pygame.examples.stars
python3 -m pygame.examples.chimp
python3 -m pygame.examples.fonty
python3 -m pygame.examples.eventlist
python3 -m pygame.examples.liquid
```

Se uma janela de jogo for exibida, isso índica Pygame está instalado corretamente! Se você tiver problemas, o [guia de primeiros passos](https://www.pygame.org/wiki/GettingStarted) descreve alguns problemas conhecidos e advertências para todas as plataformas.

Observe que cada exemplo apresenta uma funcionalidade que o Pygame nos proporciona. Para conhecer todos os exemplos disponíveis você pode visitar: [pygame.examples](https://www.pygame.org/docs/ref/examples.html)

## Conceitos Fundamentais

A biblioteca Pygame é composta de vários constructos Python, que incluem vários módulos diferentes. Esses módulos fornecem acesso abstrato ao hardware específico de nosso sistema, bem como métodos uniformes para trabalhar com esse hardware. Por exemplo, o **display** permite acesso uniforme à tela de vídeo, enquanto o **joystick** permite o controle abstrato do joystick.

### Inicialização e Módulos

Para usar os métodos da biblioteca Pygame, o módulo deve primeiro ser importado da seguinte forma:

```python
import pygame
```

A instrução **import** grava a versão do pygame e um link para o site do Pygame no console (como efeito colateral):

```
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
```

A instrução de importação do Pygame é sempre colocada no início do programa. Ela importa as classes, métodos e atributos do pygame para o espaço de nomes atual. Agora, esses novos métodos podem ser chamados via `pygame.metodo()`.

Por exemplo, agora podemos **inicializar** ou **sair** do pygame com os seguintes comandos:

```python
pygame.init()
pygame.quit()
```

- `pygame.init()`: Inicialize todos os módulos de pygame importados. Podemos sempre inicializar módulos individuais manualmente, mas **pygame.init()** inicializa todos os módulos pygame importados, é uma maneira conveniente de começar tudo.
- `pygame.quit()`: Desinicializa todos os módulos do pygame que foram inicializados anteriormente. Quando o interpretador Python é encerrado, este método é chamado independentemente, portanto, seu programa não deve precisar dele, exceto quando deseja encerrar seus recursos de pygame e continuar. É seguro chamar esta função mais de uma vez, pois as chamadas repetidas não surtem efeito.

Se eventualmente precisarmos obter ajuda sobre algum método do Pygame, podemos utilizar a função **help()** do Python, por exemplo:

```python
help(pygame)
help(pygame.draw)
help(pygame.event)
help(pygame.image)
```

**Bônus**: Para acessar todos os exemplos utilizados neste tutorial e outros adicionais, você pode visitar o repositório do GitHub **[PyGameDev](https://github.com/the-akira/PyGameDev/tree/master/Exemplos)**

### Displays e Superfícies

Além dos módulos, o Pygame também inclui várias classes Python, que encapsulam conceitos não dependentes de hardware. Um deles é a **Surface**, que em sua forma mais básica, define uma área retangular na qual podemos desenhar. Objetos Surface são usados em muitos contextos no pygame.

No Pygame, tudo é visualizado em uma única tela criada pelo usuário, que pode ser uma janela ou tela inteira. O **[display](https://www.pygame.org/docs/ref/display.html)** é criado usando o método **[set_mode()](https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode)**, que retorna uma Surface representando a parte visível da janela. É essa superfície que passamos para as funções de desenho, como por exemplo **[pygame.draw.rect()](https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect)**, e o conteúdo dessa superfície é colocado no display quando chamamos **[pygame.display.flip()](https://www.pygame.org/docs/ref/display.html#pygame.display.flip)**.

Esta variável será uma das variáveis mais utilizadas. Ele representa a janela que vemos:

```python
screen = pygame.display.set_mode((640, 480))
```

O argumento do tamanho é uma tupla com um par de números que representam a largura(**width**) e a altura(**height**) da tela, que nesse caso chamamos de **screen**.

### Coordenadas

O sistema de coordenadas cartesianas, é o sistema ao qual a maioria das pessoas está acostumada ao traçar gráficos. Este é o sistema normalmente ensinado nas escolas. O Pygame usa um sistema de coordenadas semelhante, mas um pouco diferente.

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Images/coordinates.png)

Pygame usa um sistema de coordenadas **x** e **y** onde a posição `(0,0)` é definida como o canto superior esquerdo da tela. Mover para baixo significa ter um valor de **y** mais alto, mover para a direita significa ter um valor de **x** mais alto.

### Imagens e Rects

Podemos desenhar formas(**shapes**) diretamente na superfície da tela, além disso também podemos trabalhar com imagens no disco. O módulo de imagem permite carregar e salvar imagens em uma variedade de formatos populares. As imagens são carregadas em objetos Surface, que podem ser manipulados e exibidos de várias maneiras.

Os Objetos Surface são representados por retângulos, assim como muitos outros objetos no pygame, como imagens e janelas. Retângulos são tão usados que existe uma classe especial **[Rect](https://www.pygame.org/docs/ref/rect.html)** apenas para manipulá-los. Usaremos objetos e imagens Rect em nossos jogos para desenhar personagens e inimigos e para gerenciar colisões entre eles.

#### Retângulo

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Images/Rect.png)

Um objeto **Rect** pode ser criado fornecendo:

- Os 4 parâmetros **left**, **top**, **width** e **height**
- A **posição** e **tamanho**
- Um **objeto** que tem um atributo rect

```
Rect(left, top, width, height)
Rect(posicao, tamanho)
Rect(objeto)
```

##### Atributos Virtuais

O Objeto **Rect** tem vários atributos virtuais que podem ser usados para mover e alinhar o Rect. A atribuição a esses atributos apenas move o retângulo sem alterar seu tamanho:

- x, y
- top, left, bottom, right
- topleft, bottomleft, topright, bottomright
- midtop, midleft, midbottom, midright
- center, centerx, centery

A atribuição desses 5 atributos a seguir altera o tamanho do retângulo, mantendo sua posição superior esquerda.

- size, width, height, w, h

Como podemos observar, a classe Rect define **4** pontos de canto, **4** pontos médios e **1** ponto central.

A tabela a seguir apresenta uma lista dos atributos mais importantes que os objetos **pygame.Rect** fornecem (neste exemplo, a variável onde o objeto Rect é armazenado é chamada de **meuRet**):

| Nome do Atributo  | Descrição |
|---|---|
| meuRet.left  | O valor int da coordenada X do lado esquerdo do retângulo. |
| meuRet.right  | O valor int da coordenada X do lado direito do retângulo. |
| meuRet.top  | O valor int da coordenada Y do lado superior do retângulo. |
| meuRet.bottom  | O valor int da coordenada Y do lado inferior. |
| meuRet.centerx  | O valor int da coordenada X do centro do retângulo. |
| meuRet.centery  | O valor int da coordenada Y do centro do retângulo.  |
| meuRet.width  | O valor int da largura do retângulo. |
| meuRet.height  | O valor int da altura do retângulo. |
| meuRet.size  | Uma tupla de dois ints: (width, height) |
| meuRet.topleft  | Uma tupla de dois ints: (left, top) |
| meuRet.topright  | Uma tupla de dois ints: (right, top) |
| meuRet.bottomleft  | Uma tupla de dois ints: (left, bottom) |
| meuRet.bottomright  | Uma tupla de dois ints: (right, bottom) |
| meuRet.midleft  | Uma tupla de dois ints: (left, centery) |
| meuRet.midright  | Uma tupla de dois ints: (right, centery) |
| meuRet.midtop  | Uma tupla de dois ints: (centerx, top) |
| meuRet.midbottom  | Uma tupla de dois ints: (centerx, bottom) |

### Cores

As cores são definidas como tuplas das cores básicas **vermelho**, **verde** e **azul**. Isso é chamado de [modelo RGB](https://en.wikipedia.org/wiki/RGB_color_model). Cada cor de base é representada como um número entre 0 (mínimo) e 255 (máximo) que ocupa 1 byte na memória. Uma cor RGB é então representada como um valor de 3 bytes. A mistura de duas ou mais cores resulta em novas cores. Um total aproximado de 16 milhões (255³) de cores diferentes podem ser representadas dessa forma.

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Images/colors.png)

Definimos então as cores básicas como tuplas dos três valores base. Como as cores são constantes, vamos escrevê-las em maiúsculas. A ausência de todas as cores resulta em preto. O valor máximo para todos os três componentes resulta em branco. Três valores intermediários idênticos resultam em cinza:

```python
PRETO = (0, 0, 0)
CINZA = (128, 128, 128)
BRANCO = (255, 255, 255)
```

As três cores base são definidas como:

```python
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
```

Ao misturar duas cores de base, podemos obter mais cores:

```python
AMARELO = (255, 255, 0)
CIANO = (0, 255, 255)
MAGENTA = (255, 0, 255)
```

O método `screen.fill(COR)` preenche toda a tela com a cor especificada. Para mostrar qualquer coisa na tela, devemos sempre lembrar de chamar a função `pygame.display.update()`.

É importante lembrarmos que Pygame também conta com cores já definidas, para vermos todas elas podemos usar o seguinte script:

```python
from pprint import pprint
import pygame

pprint(pygame.color.THECOLORS)
```

Neste caso, podemos por exemplo definir a cor preta da seguinte forma:

```python
BLACK = pygame.Color("black")
```

### Game Loop

Todo Game, de Pong à Diablo, usa um [Game Loop](https://gamedevelopment.tutsplus.com/articles/gamedev-glossary-what-is-the-game-loop--gamedev-2469) para controlar a jogabilidade. O Game Loop possui quatro elementos muito importantes:

1. Processar o *Input* do Usuário
2. Atualizar o estado de todos os objetos do Game
3. Atualizar o display e o *output* de áudio
4. Manter a velocidade do Game

Cada ciclo do Game Loop é chamado de *frame* e quanto mais rápido fizermos as ações em cada ciclo, mais rápido o jogo será executado. Os frames continuam a ocorrer até que alguma condição para sair do jogo seja satisfeita. Em seu projeto, existem duas condições que podem encerrar o Game Loop:

1. O jogador colide com um obstáculo.
2. O jogador fecha a janela do Game.

A primeira coisa que o Game Loop faz é processar o *Input* do Usuário para permitir que o jogador se mova pela tela. Portanto, precisamos de alguma forma para capturar e processar uma variedade de *inputs*. Fazemos isso usando o [sistema de eventos](https://www.pygame.org/docs/ref/event.html) do Pygame.

O fluxograma a seguir nos apresenta uma ideia geral de como um Game é estruturado e funciona no PyGame

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Images/pgflowchart.png)

#### Processando Eventos

A parte mais essencial de qualquer aplicação interativa é o **loop de eventos**. Reagir a eventos permite que o usuário interaja com a aplicação. Eventos são ações que podem acontecer em um programa, como:

- Clique do mouse
- Movimento do mouse
- Teclado pressionado
- Ação do joystick

A seguir temos um exemplo de um loop infinito que imprime todos os eventos no console:

```python
import pygame 
pygame.init()

# Variável que inicializa a tela
screen = pygame.display.set_mode((500,500))
# Variável para manter o loop principal funcionando
running = True 

while running: 
	# Observa cada evento na fila de eventos
	for event in pygame.event.get():
		# Imprime no console todos os eventos que vierem a ocorrer
		print(event)
		# O usuário clicou no botão fechar da janela? Se sim, pára o Loop
		if event.type == pygame.QUIT:
			running = False

pygame.quit()
```

Ao executarmos o script acima veremos uma janela com uma tela preta, ela não irá desaparecer até que cliquemos no botão fechar, todas as ações executadas por nós serão impressas em nosso console.

### Template Básico

Uma vez que adquirimos o conhecimento dos conceitos fundamentais do Pygame, vamos definir um template que servirá como um esqueleto para nossos projetos.

```python
from pygame.locals import *
import pygame

# Valores constantes
WIDTH = 500
HEIGHT = 400
FPS = 60

# Cores
BLACK = (13, 13, 13)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicializa pygame e cria a janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Título do Game")
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
	# Manter o loop rodando na velocidade correta
	clock.tick(FPS)
	# Processar Inputs (Eventos)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	# Atualizar
	# Desenhar / Renderizar
	screen.fill(BLACK)
	# Depois de desenhar tudo: flipar o display
	pygame.display.flip()

pygame.quit()
```

O módulo **[pygame.locals](https://www.pygame.org/docs/ref/locals.html)** contém cerca de 280 constantes usadas e definidas por Pygame. Colocar esta declaração no início de seu programa importa todos eles.

Encontramos nele, por exemplo, os modificadores de tecla (alt, ctrl, cmd, etc.):

```
KMOD_ALT, KMOD_CAPS, KMOD_CTRL, KMOD_LALT,
KMOD_LCTRL, KMOD_LMETA, KMOD_LSHIFT, KMOD_META,
KMOD_MODE, KMOD_NONE, KMOD_NUM, KMOD_RALT, KMOD_RCTRL,
KMOD_RMETA, KMOD_RSHIFT, KMOD_SHIFT,
```

As teclas numéricas:

```
K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9,
```

As teclas de caracteres especiais:

```
K_AMPERSAND, K_ASTERISK, K_AT, K_BACKQUOTE,
K_BACKSLASH, K_BACKSPACE, K_BREAK,
```

As teclas das letras do alfabeto:

```
K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z,
```

O comando `pygame.mixer.init()` inicialize o [módulo do mixer](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.init) para carregamento e reprodução de som. Os argumentos padrão podem ser substituídos para fornecer mixagem de áudio específica. 

O método **set_caption()** mudará o nome na janela, se o monitor possuir um título de janela.

O comando `pygame.time.Clock()` cria um [objeto relógio](https://www.pygame.org/docs/ref/time.html#pygame.time.Clock) que nos ajuda a rastrear o tempo. O relógio também fornece várias funções para ajudar a controlar a taxa de frames de um jogo, neste caso específico estamos setando nosso template para rodar em 60 frames por segundo.

### Desenhando

O módulo [pygame.draw](https://www.pygame.org/docs/ref/draw.html) permite desenharmos formas simples em uma superfície. Pode ser a superfície da tela ou qualquer objeto Surface, como uma imagem ou desenho. 

Podemos desenhar formas como:

- Retângulo
- Polígono
- Círculo 
- Elipse

As funções têm em comum que:

- Recebem um objeto Surface como primeiro argumento
- Recebem uma cor como segundo argumento 
- Recebem um parâmetro de largura como último argumento
- Retornam um objeto Rect que delimita a área alterada

Seguimos então o seguinte formato:

```
rect(Surface, color, Rect, width) -> Rect
polygon(Surface, color, pointlist, width) -> Rect
circle(Surface, color, center, radius, width) -> Rect
```

A maioria das funções tem um argumento de largura. Se a largura for 0, a forma será preenchida com a devida cor.

O seguinte código desenha primeiro a cor de fundo e, em seguida, adiciona três retângulos sólidos sobrepostos e, ao lado, três retângulos sobrepostos contornados com largura de linha crescente:

```python
screen.fill(COR)
pygame.draw.rect(screen, RED, (50, 20, 120, 100))
pygame.draw.rect(screen, GREEN, (100, 60, 120, 100))
pygame.draw.rect(screen, BLUE, (150, 100, 120, 100))

pygame.draw.rect(screen, RED, (350, 20, 120, 100), 1)
pygame.draw.rect(screen, GREEN, (400, 60, 120, 100), 4)
pygame.draw.rect(screen, BLUE, (450, 100, 120, 100), 8)
```

O código a seguir desenha primeiro a cor de fundo e, em seguida, adiciona três elipses sólidas sobrepostas e, ao lado, três elipses sobrepostas contornadas com largura de linha crescente:

```python
screen.fill(COR)
pygame.draw.ellipse(screen, RED, (50, 20, 160, 100))
pygame.draw.ellipse(screen, GREEN, (100, 60, 160, 100))
pygame.draw.ellipse(screen, BLUE, (150, 100, 160, 100))

pygame.draw.ellipse(screen, RED, (350, 20, 160, 100), 1)
pygame.draw.ellipse(screen, GREEN, (400, 60, 160, 100), 4)
pygame.draw.ellipse(screen, BLUE, (450, 100, 160, 100), 8)

pygame.display.update()
```

**Importante**: `display.update()` nos permite atualizar uma parte da tela, em vez de toda a área da tela. Sem passar argumentos, atualizará toda a tela.

Para compreender a diferença entre **update()** e **flip()** você pode visitar este [Link](https://stackoverflow.com/questions/29314987/difference-between-pygame-display-update-and-pygame-display-flip)

O script a seguir nos apresenta um exemplo de todas as formas possíveis que podemos desenhar:

```python
from math import pi
import pygame as pg
pg.init()

# Cores
BLACK = (27, 27, 27)
WHITE = (255, 255, 255)
GREEN = (42, 130, 72)
BLUE = (92, 127, 184)
YELLOW = (199, 177, 36)
RED = (179, 41, 7)

# Define dimensões do display
width = 600
height = 450
screen = pg.display.set_mode([width, height])

# Define três retângulos
retangulos = [
	pg.Rect(20, 20, 100, 50), 
	pg.Rect(20, 90, 50, 50),
	pg.Rect(500, 30, 80, 60)
]

done = True

while done:
    screen.fill(BLACK)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = False
    
    # Desenha três retângulos azuis
    for retangulo in retangulos:
    	pg.draw.rect(screen, BLUE, retangulo)

    # Desenha um retângulo verde
    pg.draw.rect(screen, GREEN, [115, 280, 70, 40])
    # Desenha um retângulo vermelho (borda)
    pg.draw.rect(screen, RED, [115, 280, 71, 41], 2)
    # Desenha um círculo amarelo
    pg.draw.circle(screen, YELLOW, (325,70), 30)
    # Desenha um círculo azul
    pg.draw.circle(screen, BLUE, [250, 250], 25, True)
    # Desenha uma elipse branca
    pg.draw.ellipse(screen, WHITE, (250, 300, 100, 100))
    # Desenha um arco vermelho
    pg.draw.arc(screen, RED, [430, 150, 150, 125], pi/100, 1.13*pi, 2)
    # Desenha uma linha azul
    pg.draw.line(screen, BLUE, (0, height-100), (width, height-100), 5)
    # Desenha uma linha verde
    pg.draw.aaline(screen, GREEN, (0, height-200), (width, height-200))
    # Desenha linhas brancas
    pg.draw.lines(screen, WHITE, False, [[400, 400], [400, 20], [200, 20]], 2)
    # Desenha um polígono amarelo
    pg.draw.polygon(screen, YELLOW, [[140, 120], [100, 200], [300, 200]])
    # Desenha um polígono verde (borda)
    pg.draw.polygon(screen, GREEN, [[140, 120], [100, 200], [300, 200]], 3)

    pg.display.update()
    
pg.quit()
```

Observe que neste exemplo específico estamos importando **pygame** como **pg**, uma forma conveniente que Python nos fornece de abreviarmos a escrita dos módulos.

### Trabalhando com Imagens

O [módulo de imagem](https://www.pygame.org/docs/ref/image.html) contém funções para carregar e salvar imagens, bem como transferir Superfícies para formatos utilizáveis por outros pacotes.

Observe que não há classe Image; uma imagem é carregada como um objeto Surface. A classe Surface permite a manipulação (desenhar linhas, definir pixels, capturar regiões, etc).

Quando construída com suporte total de imagem, a função `pygame.image.load()` pode suportar os formatos a seguir.

- JPG
- PNG
- GIF (não-animado)
- BMP
- TGA (não-comprimido)
- TIF
- LBM (e PBM)
- PBM (e PGM, PPM)
- XPM

Salvar imagens suporta apenas um conjunto limitado de formatos. Podemos salvar nos seguintes formatos.

- BMP
- TGA
- PNG
- JPEG

O método **load()** carrega uma imagem do sistema de arquivos e retorna um objeto Surface. O método **convert()** otimiza o formato da imagem e torna o desenho mais rápido. Por exemplo:

```python
imagem = pygame.image.load('personagem.png')
imagem.convert()
```

O método **get_rect()** retorna um objeto Rect de uma imagem, nos permitindo assim trabalhar com colisões.

O módulo [pygame.transform](https://www.pygame.org/docs/ref/transform.html) fornece métodos para **dimensionar**, **girar** e **inverter** imagens.

No exemplo a seguir iremos carregar a imagem [player.png](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Sprite/player.png), redimensioná-la e desenhá-la na tela.

```python
from sys import exit
from pygame.locals import * 
import pygame

# Define o relógio
clock = pygame.time.Clock()

# Inicializa pygame
pygame.init()

# Define o nome da janela
pygame.display.set_caption('PyGame')

# Define o tamanho da tela
WIDTH, HEIGHT = 450, 200
WINDOW_SIZE = (WIDTH, HEIGHT)

# Inicia a tela
screen = pygame.display.set_mode(WINDOW_SIZE, True, 32)

# Carrega a imagem do personagem
player_image = pygame.image.load('player.png').convert_alpha()
player_transformed = pygame.transform.scale(player_image, (50,75))

moving_right = False 
moving_left = False

player_location = [155, 310]
velocity = 3.5

# Game Loop
while True:					
	screen.fill((70,86,94)) # Preenche a tela com cinza
	screen.blit(player_transformed, player_location)

	if moving_right == True:
		player_location[0] += velocity
	if moving_left == True: 
		player_location[0] -= velocity

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True 
			if event.key == K_LEFT:
				moving_left = True 
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False 
			if event.key == K_LEFT:
				moving_left = False
	
	if player_location[0] < 0:
		player_location[0] = 0
	elif player_location[0] + player_transformed.get_width() > WIDTH:
		player_location[0] = WIDTH - player_transformed.get_width()
	elif player_location[1] + player_transformed.get_height() > HEIGHT:
		player_location[1] = HEIGHT - player_transformed.get_height()

	pygame.display.update() # atualiza a tela
	clock.tick(60) # mantém 60 FPS
```

A função **blit()** é muito importante, o termo **blit** significa *Block Transfer* e é como copiamos o conteúdo de um Surface para outra. O desenho ou imagem pode ser posicionado com o argumento **dest**. Dest pode ser um par de coordenadas que representam o canto superior esquerdo da superfície de origem. Um Rect também pode ser passado como o destino e o canto superior esquerdo do retângulo será usado como a posição para o blit. O tamanho do retângulo de destino não afeta o blit.

Sendo assim, **blit()** recebe dois importantes argumentos:

1. A superfície para desenhar (neste caso estamos usando uma imagem)
2. O local onde desenhá-lo na superfície de origem

Perceba também que definimos uma variável chamada de **player_location** que representa as coordenadas da posição do player na tela. A variável **velocity** representa a velocidade de deslocamento do player. Para movermos o player usamos as setas do teclado (<- & ->), ao pressionarmos elas, iremos acionar as respectivas variáveis **moving_right** e **moving_left** como **True** fazendo assim o player se movimentar. Por fim definimos os limites da tela, para que o player não desapareça de nossa visão e atualizamos a tela com o comando `pygame.display.update()`.

Para transparência alfa, como em imagens **.png**, usamos o método **convert_alpha()** após o carregamento para que a imagem tenha transparência por pixel.

### Detectando Colisões

Verificar colisões é uma técnica fundamental de programação de Games e geralmente requer um pouco de matemática para determinar se dois sprites estão se sobrepondo.

É neste momento que uma biblioteca como o Pygame se torna muito útil! Escrever código de detecção de colisão é tedioso, por isso Pygame possui [diversos métodos](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_rect) de detecção de colisão disponíveis para usarmos, sem precisarmos "reinventar a roda".

No exemplo a seguir usaremos o método [colliderect](https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect), que retornará **True** se qualquer parte do retângulo se sobrepor (exceto as bordas top + bottom ou left + right).

```python
from pygame.locals import * 
from random import randint
from sys import exit
import pygame
pygame.init()

# Define cores
BLACK = (12, 12, 12)
WHITE = (255, 255, 255)
BLUE = (96, 110, 150)
RED = (255, 0, 0)
 
# Define o width e height da screen [width, height]
width = 500
height = 400
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
 
# Game Loop fica ativo até que jogando seja False
playing = True
clock = pygame.time.Clock()

player_image = pygame.image.load('sprites/player.png').convert_alpha()
player_transformed = pygame.transform.scale(player_image, (70,70))
player_rect = player_transformed.get_rect()

portal_image = pygame.image.load('sprites/portal.png')
portal_transformed = pygame.transform.scale(portal_image, (70,70))
portal_rect = portal_transformed.get_rect()

trunk_image = pygame.image.load('sprites/trunk.png')
trunk_image.set_colorkey(WHITE)
trunk_transformed = pygame.transform.scale(trunk_image, (80,80))
trunk_rect = portal_transformed.get_rect()

# Posição Inicial do player
player_x = 20
player_y = 20

# Velocidade e Direção do player
player_change = 3.5

moving_right = False 
moving_left = False
moving_top = False 
moving_down = False
 
while playing:
    screen.fill(BLUE)

    if moving_right == True:
        player_x += player_change
    if moving_left == True: 
        player_x -= player_change
    if moving_top == True:
        player_y -= player_change
    if moving_down == True: 
        player_y += player_change  

    player_rect.x = player_x
    player_rect.y = player_y
    portal_rect.x = 140
    portal_rect.y = 170
    trunk_rect.x = 300
    trunk_rect.y = 250

    if player_rect.colliderect(portal_rect):
        print('ocorreu uma colisão entre os objetos')
        player_x = randint(35,450)
        player_y = randint(35,350)

    if player_rect.colliderect(trunk_rect):
        print('ocorreu uma colisão entre os objetos')
        exit()

    if player_x < 0:
        player_x = 0
    elif player_x + player_transformed.get_width() > width:
        player_x = width - player_transformed.get_width()
    if player_y < 0:
        player_y = 0
    elif player_y + player_transformed.get_height() > height:
        player_y = height - player_transformed.get_height()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True 
            if event.key == K_LEFT:
                moving_left = True 
            if event.key == K_UP:
                moving_top = True
            if event.key == K_DOWN:
                moving_down = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False 
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_top = False
            if event.key == K_DOWN:
                moving_down = False

    screen.blit(player_transformed, [player_rect.x, player_rect.y])
    screen.blit(portal_transformed, [portal_rect.x, portal_rect.y])
    screen.blit(trunk_transformed, [trunk_rect.x, trunk_rect.y])

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
```

Observe que estamos carregando três imagens, redimensionando-as e usando o método **get_rect()** para obter um retângulo delas (necessário para testarmos as colisões).

As imagens, representam, respectivamente:

- Um [jogador](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/player.png)
- Um [portal](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/portal.png)
- Um [tronco](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/trunk.png)

Um detalhe que devemos citar é que o fundo do tronco é branco, então estamos usando uma técnica chamada *colorkey* que torna uma cor totalmente transparente. A função é bastante simples, é chamada `set_colorkey(COR)`.

**Atenção**: Se uma imagem tiver um valor alfa definido, o colorkey não funcionará! Um truque simples para fazer o colorkey funcionar é: `image.set_alpha(None)` para desabilitá-lo e então você poderá usar `set_colorkey(COR)`.

O jogador poderá se mover livremente para as quatro direções (norte, sul, leste e oeste) e testaremos se ele irá colidir com o portal ou o tronco. Se houver uma colisão com o portal, iremos mover o jogador para uma posição aleatória da tela, caso haja uma colisão com o tronco, encerraremos o Game com a função **exit()** da biblioteca [sys](https://docs.python.org/3/library/sys.html).