# Introdução ao Desenvolvimento de Games 2D com PyGame

![img](/Images/pygame.png)

<figure>
    <blockquote>
        <p>"Game creation keeps on expanding, just like the Universe. That is why I keep making games."</p>
        <footer>
            <cite>— Hideo Kojima</cite>
        </footer>
    </blockquote>
</figure>

## Conteúdo

- [Introdução](#introdução)
- [Instalação](#instalação)
- [Conceitos Fundamentais](#conceitos-fundamentais)
	- [Inicialização e Módulos](#inicialização-e-módulos)
	- [Displays e Superfícies](#displays-e-superfícies)
	- [Coordenadas](#coordenadas)
	- [Imagens e Rects](#imagens-e-rects)
	- [Cores](#cores)
	- [Game Loop](#game-loop)
	- [Template Básico](#template-básico)
	- [Desenhando](#desenhando)
	- [Trabalhando com Imagens](#trabalhando-com-imagens)
	- [Trabalhando com Textos](#trabalhando-com-textos)
	- [Detectando Colisões](#detectando-colisões)
	- [Sprites](#sprites)
	- [Efeitos Sonoros](#efeitos-sonoros)
    - [Debugging](#debugging)
- [Construindo um Platform Game](#construindo-um-platform-game)
- [Conclusão](#conclusão)

## Introdução

**[Pygame](https://www.pygame.org/)** é um conjunto de módulos Python projetados para criar vídeo-games. O Pygame adiciona funcionalidades à excelente [biblioteca SDL](https://www.libsdl.org/), que significa **Simple DirectMedia Layer**. SDL fornece acesso *cross-platform* aos componentes de hardware de multimídia de nosso sistema, como **som**, **vídeo**, **mouse**, **teclado** e **joystick**. Nos permitindo construir jogos completos e também programas multimídia na linguagem Python.

Pygame é altamente portátil e roda em quase todas as plataformas e sistemas operacionais.

## Instalação

Para instalarmos Pygame em nossa máquina, utilizaremos [pip](https://pypi.org/project/pip/), o instalador de pacotes tradicional do Python. Sendo assim, executaremos o seguinte comando em nosso terminal:

```
pip install pygame
```

Podemos verificar se a instalação ocorreu corretamente carregando um dos exemplos embutidos com a biblioteca:

```
python3 -m pygame.examples.aliens
python3 -m pygame.examples.stars
python3 -m pygame.examples.chimp
python3 -m pygame.examples.fonty
python3 -m pygame.examples.eventlist
python3 -m pygame.examples.liquid
```

Se uma janela de Game for exibida, isso indica que Pygame está instalado corretamente! Se você tiver problemas, o [guia de primeiros passos](https://www.pygame.org/wiki/GettingStarted) descreve alguns problemas conhecidos e advertências para todas as plataformas.

Observe que cada exemplo apresenta uma funcionalidade que o Pygame nos proporciona. Para conhecer todos os exemplos disponíveis você pode visitar: [pygame.examples](https://www.pygame.org/docs/ref/examples.html).

## Conceitos Fundamentais

A biblioteca Pygame é composta de vários constructos Python, que incluem vários módulos diferentes. Esses módulos fornecem acesso abstrato ao hardware específico de nosso sistema, bem como métodos uniformes para trabalhar com esse hardware. Por exemplo, o **display** permite acesso uniforme à tela de vídeo, enquanto o **joystick** permite o controle abstrato do joystick.

### Inicialização e Módulos

Para usar os métodos da biblioteca Pygame, o módulo deve primeiro ser importado da seguinte forma:

```python
import pygame
```

A instrução **import** grava a versão do pygame e um link para o site do Pygame no console:

```
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
```

A instrução de importação do Pygame é sempre colocada no início do programa. Ela importa as classes, métodos e atributos do Pygame para o espaço de nomes atual. Agora, esses novos métodos podem ser chamados via `pygame.metodo()`.

Por exemplo, agora podemos **inicializar** ou **sair** do pygame com os seguintes comandos:

```python
pygame.init()
pygame.quit()
```

- `pygame.init()`: Inicialize todos os módulos de Pygame importados. Podemos sempre inicializar módulos individuais manualmente, mas **pygame.init()** inicializa todos os módulos Pygame importados, é uma maneira conveniente de começar tudo.
- `pygame.quit()`: Desinicializa todos os módulos do Pygame que foram inicializados anteriormente. Quando o interpretador Python é encerrado, este método é chamado independentemente, portanto, seu programa não deve precisar dele, exceto quando desejar encerrar seus recursos de Pygame.

Se eventualmente precisarmos obter ajuda sobre algum método ou classe do Pygame, podemos utilizar a função **help()** do Python, por exemplo:

```python
help(pygame)
help(pygame.draw)
help(pygame.event)
help(pygame.image)
```

**Bônus**: Para acessar todos os exemplos utilizados neste tutorial e outros adicionais, você pode visitar o repositório do GitHub: **[PyGameDev](https://github.com/the-akira/PyGameDev/tree/master/Exemplos)**.

### Displays e Superfícies

Além dos módulos, o Pygame também inclui várias classes Python que encapsulam conceitos não dependentes de hardware. Uma delas é a **Surface**, que em sua forma mais básica, define uma área retangular na qual podemos desenhar. Objetos Surface são usados em muitos contextos no Pygame.

No Pygame, tudo é visualizado em uma única tela criada pelo usuário, que pode ser uma janela ou tela inteira. O **[display](https://www.pygame.org/docs/ref/display.html)** é criado usando o método **[set_mode()](https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode)**, que retorna uma Surface representando a parte visível da janela. É essa superfície que passamos para as funções de desenho, como por exemplo **[pygame.draw.rect()](https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect)**, e o conteúdo dessa superfície é colocado no display quando chamamos **[pygame.display.flip()](https://www.pygame.org/docs/ref/display.html#pygame.display.flip)**.

Esta variável será uma das variáveis mais utilizadas. Ele representa a janela que vemos:

```python
screen = pygame.display.set_mode((640, 480))
```

O argumento do tamanho é uma tupla com um par de números que representam a largura(**width**) e a altura(**height**) da tela, que nesse caso chamamos de **screen**.

### Coordenadas

O sistema de coordenadas cartesianas é o sistema ao qual a maioria das pessoas está acostumada ao traçar gráficos. Este é o sistema normalmente ensinado nas escolas. O Pygame usa um sistema de coordenadas semelhante, mas um pouco diferente.

![img](/Images/coordinates.png)

Pygame usa um sistema de coordenadas **x** e **y** onde a posição `(0,0)` é definida como o canto superior esquerdo da tela. Mover para baixo significa ter um valor de **y** mais alto, mover para a direita significa ter um valor de **x** mais alto.

### Imagens e Rects

Podemos desenhar formas(**shapes**) diretamente na superfície da tela, além disso também podemos trabalhar com imagens no disco. O módulo de imagem permite carregar e salvar imagens em uma variedade de formatos populares. As imagens são carregadas em objetos Surface, que podem ser manipulados e exibidos de várias maneiras.

Os objetos Surface são representados por retângulos, assim como muitos outros objetos no Pygame, como imagens e janelas. Retângulos são tão usados que existe uma classe especial **[Rect](https://www.pygame.org/docs/ref/rect.html)** apenas para manipulá-los. Usaremos objetos e imagens Rect em nossos jogos para desenhar personagens e obstáculos e para gerenciar colisões entre eles.

#### Retângulo

![img](/Images/Rect.png)

Um objeto **Rect** pode ser criado fornecendo:

- Os 4 parâmetros **left**, **top**, **width** e **height**
- A **posição** e **tamanho**
- Um **objeto** que tem um atributo rect

```
Rect(left, top, width, height)
Rect(posicao, tamanho)
Rect(objeto)
```

A figura a seguir nos ajuda a compreender a criação do retângulo e seu posicionamento:

![img](/Images/retangulo.png)

##### Atributos Virtuais

O objeto **Rect** tem vários atributos virtuais que podem ser usados para mover e alinhar o Rect. A atribuição a esses atributos apenas move o retângulo sem alterar seu tamanho:

- x, y
- top, left, bottom, right
- topleft, bottomleft, topright, bottomright
- midtop, midleft, midbottom, midright
- center, centerx, centery

A atribuição desses 5 atributos a seguir altera o tamanho do retângulo, mantendo sua posição superior esquerda:

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

![img](/Images/colors.png)

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

O fluxograma a seguir nos apresenta uma ideia geral de como um Game é estruturado e funciona no PyGame:

![img](/Images/pgflowchart.png)

#### Processando Eventos

A parte essencial de qualquer aplicação interativa é o **loop de eventos**. Reagir a eventos permite que o usuário interaja com a aplicação. Eventos são ações que podem acontecer em um programa, como:

- Clique do mouse
- Movimento do mouse
- Teclado pressionado
- Ação do joystick

A seguir temos um exemplo de um loop infinito que imprime todos os eventos no console:

```python
import pygame 
pygame.init()

# Inicializa a tela
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Eventos")

# Game Loop ficará ativo até que running seja False
running = True 
while running: 
    # Observa cada evento na fila de eventos
    for event in pygame.event.get():
        # Imprime no console todos os eventos que vierem a ocorrer
        print(event)
        # Fecha o jogo
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

# Inicializa PyGame, cria a janela e define o relógio
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

Ao executarmos este **template**, vamos obter o seguinte resultado:

![img](/Screenshots/screenshot1.png)

Como podemos observar, é apenas uma tela preenchida com a cor preta, mas que servirá como estrutura básica para nossos projetos futuros.

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

O seguinte código preenche a cor de fundo com branco e, em seguida, adiciona três retângulos sólidos sobrepostos e, ao lado, três retângulos sobrepostos contornados com largura de linha crescente.

Vamos executá-lo em nosso console:

```python
>>> import pygame
>>> screen = pygame.display.set_mode((625, 220))
>>> screen.fill(BRANCO)

>>> pygame.draw.rect(screen, VERMELHO, (50, 20, 120, 100))
>>> pygame.draw.rect(screen, VERDE, (100, 60, 120, 100))
>>> pygame.draw.rect(screen, AZUL, (150, 100, 120, 100))

>>> pygame.draw.rect(screen, VERMELHO, (350, 20, 120, 100), 1)
>>> pygame.draw.rect(screen, VERDE, (400, 60, 120, 100), 4)
>>> pygame.draw.rect(screen, AZUL, (450, 100, 120, 100), 8)
```

Perceba que o segundo comando que executamos irá abrir a tela e os comandos seguintes não apresentam nenhum resultado na tela, isso porque devemos atualizá-la:

```python
pygame.display.flip()
```

O resultado será este:

![img](/Screenshots/screenshot10.png)

Para fechar a janela podemos utilizar o método `quit()`:

```python
pygame.quit()
```

O código a seguir preenche a cor de fundo com branco e, em seguida, adiciona três elipses sólidas sobrepostas e, ao lado, três elipses sobrepostas contornadas com largura de linha crescente.

Novamente, vamos executá-lo em nosso console:

```python
>>> import pygame
>>> screen = pygame.display.set_mode((660, 220))
>>> screen.fill(BRANCO)

>>> pygame.draw.ellipse(screen, VERMELHO, (50, 20, 160, 100))
>>> pygame.draw.ellipse(screen, VERDE, (100, 60, 160, 100))
>>> pygame.draw.ellipse(screen, AZUL, (150, 100, 160, 100))

>>> pygame.draw.ellipse(screen, VERMELHO, (350, 20, 160, 100), 1)
>>> pygame.draw.ellipse(screen, VERDE, (400, 60, 160, 100), 4)
>>> pygame.draw.ellipse(screen, AZUL, (450, 100, 160, 100), 8)

>>> pygame.display.update()
```

Que nos trará o seguinte *output*:

![img](/Screenshots/screenshot11.png)

**Importante**: `display.update()` nos permite atualizar uma parte da tela, em vez de toda a área da tela. Sem passar argumentos, atualizará toda a tela.

Para compreender a diferença entre **update()** e **flip()** você pode visitar este [Link](https://stackoverflow.com/questions/29314987/difference-between-pygame-display-update-and-pygame-display-flip).

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
    # Atualiza a tela
    pg.display.update()
    
pg.quit()
```

Observe que neste exemplo específico estamos importando **pygame** como **pg**, uma forma conveniente que Python nos fornece de abreviarmos a escrita dos módulos.

Ao executarmos este script, obteremos como resultado diversos desenhos em nossa tela:

![img](/Screenshots/screenshot2.png)

### Trabalhando com Imagens

O [módulo de imagem](https://www.pygame.org/docs/ref/image.html) contém funções para carregar e salvar imagens, bem como transferir Superfícies para formatos utilizáveis por outros pacotes.

Observe que não há classe Image; uma imagem é carregada como um objeto Surface. A classe Surface permite a manipulação (desenhar linhas, definir pixels, capturar regiões, etc).

Quando construída com suporte total de imagem, a função `pygame.image.load()` pode suportar os formatos a seguir:

- JPG
- PNG
- GIF (não-animado)
- BMP
- TGA (não-comprimido)
- TIF
- LBM (e PBM)
- PBM (e PGM, PPM)
- XPM

Salvar imagens suporta apenas um conjunto limitado de formatos. Podemos salvar nos seguintes formatos:

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

No exemplo a seguir iremos carregar a imagem [player.png](/Exemplos/Sprite/player.png), redimensioná-la e desenhá-la na tela.

```python
from dataclasses import dataclass
import pygame

# Define o relógio
clock = pygame.time.Clock()

# Inicializa pygame
pygame.init()

# Define a cor de fundo
BACKGROUND_COLOR = (70,86,94)

# Define o nome da janela
pygame.display.set_caption('PyGame')

# Define o número de quadros por segundo
FPS = 60

# Define o tamanho da tela
WIDTH, HEIGHT = 450, 200
WINDOW_SIZE = (WIDTH, HEIGHT)

# Inicia a tela
screen = pygame.display.set_mode(WINDOW_SIZE, True, 32)

# Carrega e altera a imagem do personagem
player_image = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale(player_image, (50,75))

moving_right = False 
moving_left = False

@dataclass
class PlayerLocation:
    x: int 
    y: int

player_location = PlayerLocation(x=155, y=125)
velocity = 3.5

# Game Loop
running = True
while running:   
    # Preenche a tela com cinza              
    screen.fill(BACKGROUND_COLOR) 
    # Desenha o player
    screen.blit(player, (player_location.x, player_location.y))

    if moving_right:
        player_location.x += velocity
    if moving_left: 
        player_location.x -= velocity
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True 
            if event.key == pygame.K_LEFT:
                moving_left = True 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False 
            if event.key == pygame.K_LEFT:
                moving_left = False
    
    if player_location.x < 0:
        player_location.x = 0
    if player_location.x + player.get_width() > WIDTH:
        player_location.x = WIDTH - player.get_width()

    pygame.display.update() 
    clock.tick(FPS) 

pygame.quit()
```

A função **blit()** é muito importante, o termo **blit** significa *Block Transfer* e é como copiamos o conteúdo de um Surface para outra. O desenho ou imagem pode ser posicionado com o argumento **dest**. Dest pode ser um par de coordenadas que representam o canto superior esquerdo da superfície de origem. Um Rect também pode ser passado como o destino e o canto superior esquerdo do retângulo será usado como a posição para o blit. O tamanho do retângulo de destino não afeta o blit.

Sendo assim, **blit()** recebe dois importantes argumentos:

1. A superfície para desenhar (neste caso estamos usando uma imagem)
2. O local onde desenhá-lo na superfície de origem

Perceba também que definimos um objeto chamada de **player_location** que representa as coordenadas da posição do player na tela. A variável **velocity** representa a velocidade de deslocamento do player. Para mover o player usamos as Arrow Keys do teclado (<- & ->), ao pressionarmos elas, iremos acionar as respectivas variáveis **moving_right** e **moving_left** como **True** fazendo assim o player se movimentar. Por fim definimos os limites da tela, para que o player não desapareça de nossa visão e atualizamos a tela com o comando `pygame.display.update()`.

Para transparência alfa, como em imagens **.png**, usamos o método **convert_alpha()** após o carregamento para que a imagem tenha transparência por pixel.

Este exemplo nos trará o seguinte resultado:

![img](/Screenshots/screenshot3.png)

### Trabalhando com Textos

No Pygame, o texto não pode ser escrito diretamente na tela, o módulo [pygame.font](https://www.pygame.org/docs/ref/font.html) nos permite "desenhar" textos em nossa tela. Para isso precisamos seguir alguns passos. 

1. A primeira etapa é criar um [objeto Font](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) com um determinado tamanho de fonte. 
2. A segunda etapa é transformar o texto em uma imagem com uma determinada cor. 
3. A terceira etapa é enviar a imagem para a tela. 

Por exemplo:

```python
font = pygame.font.SysFont(None, 24)
imagem = font.render('Texto', True, VERDE)
screen.blit(imagem, (20, 20))
``` 

Pygame vem com uma fonte padrão embutida. Isso sempre pode ser acessado passando **None** como o nome da fonte como argumento para o método **SysFont()**, o segundo argumento representa o tamanho da Font.

Uma vez que a fonte é criada, seu tamanho não pode ser alterado. Um objeto **Font** é usado para criar um objeto **Surface** a partir de uma string. O Pygame não fornece uma maneira direta de escrever texto em um objeto **Surface**. O método **render()** deve ser usado para criar um objeto **Surface** a partir do texto, que então pode ser enviado para a tela. O método **render()** só pode renderizar linhas simples. Um caractere de nova linha não é renderizado.

A função **get_fonts()** retorna uma lista de todas as fontes instaladas e disponíveis. O código a seguir verifica quais fontes estão em seu sistema e quantas existem, e as imprime no console:

```python
from pprint import pprint 
import pygame

fonts = pygame.font.get_fonts()

print(f'Existem {len(fonts)} fonts disponíveis')
pprint(fonts)
```

No exemplo a seguir vamos exibir o texto "Hello PyGame" no centro de nossa tela:

```python
import pygame
pygame.init()

def main():
    # Inicializa a Tela
    screen = pygame.display.set_mode((250, 100))
    pygame.display.set_caption('PyGame Text')

    # Define e Preenche o Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((15, 15, 15))

    # Define, Posiciona e Apresenta o Texto no Background
    font = pygame.font.SysFont('dyuthi', 36)
    text = font.render("Hello PyGame", 1, (195, 195, 195))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)

    # Loop de Eventos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Desenha o Background
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': 
    main()
```

Observe que escolhemos a fonta *dyuthi*. Também utilizamos os atributos **centerx** e **centery** para nos auxiliar a centralizar o texto. O resultado será este:

![img](/Screenshots/screenshot4.png)

### Detectando Colisões

Verificar colisões é uma técnica fundamental de programação de Games e geralmente requer um pouco de matemática para determinar se dois sprites estão se sobrepondo.

É neste momento que uma biblioteca como o Pygame se torna muito útil! Escrever código de detecção de colisão é tedioso, por isso Pygame possui [diversos métodos](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_rect) de detecção de colisão disponíveis para usarmos, sem precisarmos "reinventar a roda".

No exemplo a seguir usaremos o método [colliderect](https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect), que retornará **True** se qualquer parte do retângulo se sobrepor (exceto as bordas top + bottom ou left + right).

```python
from dataclasses import dataclass
import pygame
pygame.init()

# Define cores
WHITE = (255, 255, 255)
BLACK = (17, 17, 17)
 
# Define o comprimento e altura (WIDTH e HEIGHT) da tela (screen)
WIDTH = 500
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collisions")
 
# Game Loop ficará ativo até que playing seja False
playing = True
# Define relógio e quadros por segundo
clock = pygame.time.Clock()
FPS = 60

# Carrega o fundo
background = pygame.image.load('sprites/background.png').convert_alpha()

# Carrega o sprite, transforma sua dimensão, obtém retângulo e define posição x e y
player_image = pygame.image.load('sprites/player.png').convert_alpha()
player_transformed = pygame.transform.scale(player_image, (50,75))
player_rect = player_transformed.get_rect()
player_rect.x = 10
player_rect.y = 10
# Velocidade x e y do player
dx = 3.5
dy = 3.5

portal_image = pygame.image.load('sprites/portal.png').convert_alpha()
portal_transformed = pygame.transform.scale(portal_image, (65,65))
portal_rect = portal_transformed.get_rect()
portal_rect.x = 195
portal_rect.y = 95

trunk_image = pygame.image.load('sprites/trunk.png')
trunk_image.set_colorkey(WHITE)
trunk_transformed = pygame.transform.scale(trunk_image, (65,65))
trunk_rect = trunk_transformed.get_rect()
trunk_rect.x = 355
trunk_rect.y = 205

box_image = pygame.image.load('sprites/box.png').convert_alpha()
box_transformed = pygame.transform.scale(box_image, (65,65))
box_rect = box_transformed.get_rect()
box_rect.x = 100
box_rect.y = 255

skull_image = pygame.image.load('sprites/skull.png').convert_alpha()
skull_transformed = pygame.transform.scale(skull_image, (60,70))
skull_rect = skull_transformed.get_rect()
skull_rect.x = 430
skull_rect.y = 10

# Direção do personagem
moving_right = False 
moving_left = False
moving_top = False 
moving_down = False

# Movimento e colisões
@dataclass
class Movement:
    x: int 
    y: int

def collision_test(player, obstacles):
    collisions = []
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            collisions.append(obstacle)
    return collisions

def move_and_collide(player, movement, obstacles):
    player.x += movement.x
    collisions_x = collision_test(player, obstacles)
    for obstacle in collisions_x:
        if movement.x > 0:
            player.right = obstacle.left
        if movement.x < 0:
            player.left = obstacle.right
        if obstacle.x == skull_rect.x:
            screen.fill(BLACK)
    player.y += movement.y
    collisions_y = collision_test(player, obstacles)
    for obstacle in collisions_y:
        if movement.y > 0:
            player.bottom = obstacle.top
        if movement.y < 0:
            player.top = obstacle.bottom
        if obstacle.y == skull_rect.y:
            screen.fill(BLACK)

# Início do Game Loop
while playing:
    screen.blit(background, (0,0))

    movement = Movement(x=0, y=0)
    if moving_right:
        movement.x += dx
    if moving_left: 
        movement.x -= dx
    if moving_top:
        movement.y -= dy
    if moving_down: 
        movement.y += dy  

    if player_rect.x < 0:
        player_rect.x = 0
    elif player_rect.x + player_transformed.get_width() > WIDTH:
        player_rect.x = WIDTH - player_transformed.get_width()
    if player_rect.y < 0:
        player_rect.y = 0
    elif player_rect.y + player_transformed.get_height() > HEIGHT:
        player_rect.y = HEIGHT - player_transformed.get_height()

    if player_rect.colliderect(portal_rect):
        player_rect.x = 430
        player_rect.y = 310

    obstacles = [trunk_rect, box_rect, skull_rect]
    move_and_collide(player_rect, movement, obstacles)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True 
            if event.key == pygame.K_LEFT:
                moving_left = True 
            if event.key == pygame.K_UP:
                moving_top = True
            if event.key == pygame.K_DOWN:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False 
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_UP:
                moving_top = False
            if event.key == pygame.K_DOWN:
                moving_down = False

    screen.blit(player_transformed, [player_rect.x, player_rect.y])
    screen.blit(portal_transformed, [portal_rect.x, portal_rect.y])
    screen.blit(trunk_transformed, [trunk_rect.x, trunk_rect.y])
    screen.blit(box_transformed, [box_rect.x, box_rect.y])
    screen.blit(skull_transformed, [skull_rect.x, skull_rect.y])

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
```

Observe que estamos carregando cinco imagens, redimensionando-as e usando o método **get_rect()** para obter um retângulo delas (necessário para testarmos as colisões).

As imagens, representam, respectivamente:

- Um [jogador](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/player.png)
- Um [portal](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/portal.png)
- Um [tronco](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/trunk.png)
- Um [baú](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/box.png)
- Um [crânio](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Collision/sprites/skull.png)

Um detalhe que devemos citar é que o fundo do tronco é branco, então estamos usando uma técnica chamada *colorkey* que torna uma cor totalmente transparente. A função é bastante simples, é chamada `set_colorkey(COR)`.

**Atenção**: Se uma imagem tiver um valor alfa definido, o colorkey não funcionará! Um truque simples para fazer o colorkey funcionar é: `image.set_alpha(None)` para desabilitá-lo e então você poderá usar `set_colorkey(COR)`.

O jogador poderá se mover livremente para as quatro direções (norte, sul, leste e oeste) usando as Arrow Keys: 

![img](/Images/arrowkeys.png)

E testaremos se ele irá colidir com o **portal**, o **tronco**, o **baú** ou o **crânio**, este último que apagará a luz. Se houver uma colisão com o portal, iremos mover o jogador para uma posição específica da tela, caso haja uma colisão com o tronco ou o baú, não permitiremos que ocorra sobreposição entre os retângulos.

Executando este script, teremos a seguinte tela como *output*:

![img](/Screenshots/screenshot5.png)

### Sprites

Em computação gráfica, um sprite é um bitmap bidimensional integrado em uma cena maior, na maioria das vezes usado no contexto de um videogame 2D. O termo foi usado pela primeira vez por [Danny Hillis](https://en.wikipedia.org/wiki/Danny_Hillis) na Texas Instruments no final dos anos 1970.

Pygame fornece uma [classe Sprite](https://www.pygame.org/docs/ref/sprite.html) que é projetada para conter uma ou várias representações gráficas de qualquer objeto do Game que você deseja exibir na tela. Para usá-la, criamos uma nova classe que estende **Sprite**. Isso permite usarmos todos os seus métodos embutidos.

Existe a classe Sprite principal e várias classes de Grupo que contêm Sprites. O uso dessas classes é totalmente opcional ao usar Pygame. As classes são bastante leves e fornecem apenas um ponto de partida para o código comum à maioria dos Games.

A classe Sprite tem como intenção ser usada como uma classe base para os diferentes tipos de objetos do Game. Existe também uma classe base [Group](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group) que simplesmente armazena sprites. Um Game pode criar novos tipos de classes de Grupo que operam em instâncias de Sprite especialmente personalizadas.

A classe Sprite básica pode desenhar os Sprites que ela contém em uma **Surface**. O método `Group.draw()` requer que cada Sprite tenha um atributo **Surface.image** e um **Surface.rect**. O método `Group.clear()` requer esses mesmos atributos e pode ser usado para apagar todos os Sprites com background. Existem também grupos mais avançados: `pygame.sprite.RenderUpdates()` e `pygame.sprite.OrderedUpdates()`.

Finalmente, este módulo **Sprite** contém várias funções de colisão. Isso ajuda a encontrar sprites dentro de vários grupos que possuem retângulos delimitadores que se cruzam. Para encontrar as colisões, os Sprites precisam ter um atributo **Surface.rect** atribuído.

Os grupos são projetados para alta eficiência na remoção e adição de Sprites a eles. Eles também permitem testes de baixo custo computacional para ver se um Sprite já existe em um Grupo. Um determinado Sprite pode existir em qualquer número de grupos. Um Game pode usar alguns grupos para controlar a renderização de objetos e um conjunto completamente separado de grupos para controlar a interação ou o movimento do jogador. Em vez de adicionar atributos de tipo ou bools a uma classe Sprite derivada, considere manter os Sprites dentro de Grupos organizados. Isso permitirá uma pesquisa mais fácil posteriormente no Game.

Sprites e grupos gerenciam seus relacionamentos com os métodos **add()** e **remove()**. Esses métodos podem aceitar um único ou vários destinos para associação. Os inicializadores padrão para essas classes também usam um único ou uma lista de destinos para a associação inicial. É seguro adicionar e remover repetidamente o mesmo Sprite de um Grupo.

A classe base para objetos visíveis do Game é [pygame.sprite.Sprite](http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite). As classes derivadas necessitarão substituir `Sprite.update()` e atribuir atributos **Sprite.image** e **Sprite.rect**. O inicializador pode aceitar qualquer número de instâncias de Grupo a serem adicionadas.

Ao criar uma subclasse do Sprite, certifique-se de chamar o inicializador base antes de adicionar o Sprite aos grupos. Por exemplo:

```python
class Block(pygame.sprite.Sprite):
    # Construtor. Recebe a cor do bloco e sua posição x e y como argumento
    def __init__(self, color, width, height):
       # Chama o construtor da classe pai (Sprite)
       pygame.sprite.Sprite.__init__(self)
       # Cria uma imagem do bloco e preenche com uma cor respectiva
       # Também pode ser uma imagem carregada do disco
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       # Busca o objeto retângulo que possui as dimensões da imagem
       # Atualiza a posição deste objeto setando os valores de rect.x e rect.y
       self.rect = self.image.get_rect()
```

Observe que neste exemplo estamos apenas definindo um simples Bloco.

O método **update()** é utilizado para controlar o comportamento de um Sprite. A implementação padrão deste método não faz nada, é apenas um "gancho" conveniente que você pode sobrescrever. Este método é chamado por `Group.update()` com quaisquer argumentos que você fornecer a ele.

Vejamos agora um exemplo com mais detalhes:

```python
import pygame 
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'guy.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 10

    def update(self):
        self.rect.x += 4
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 100:
            self.y_speed = -5
        if self.rect.top < 100:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sprite OOP')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True 
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
```

Neste exemplo definimos um Sprite chamado de **Player**, que é uma imagem do personagem [Guy Fawkes](/Exemplos/SpriteOOP/img/guy.png) que carregamos de nosso disco, localizada em um diretório que denominei **img**, também estamos definindo algumas propriedades básicas para este Sprite, como o retângulo e sua velocidade no eixo **y**. Também estamos sobrescrevendo o método **update()**, fazendo o Sprite se deslocar para a direita e alternando os valores do eixo **y** quando o Sprite atinge uma determinada posição na tela, nos dando assim a impressão de um movimento diagonal.

Instanciamos o objeto **Group** em uma variável chamada de **all_sprites**, lembre que Group é uma classe de contêiner para armazenar e gerenciar vários objetos Sprite.

Em seguida instanciamos o sprite **Player** e guardamos ele na variável **player**, que por sua vez é adicionada ao grupo **all_sprites**.

Em nosso Game Loop estamos atualizando todos os Sprites do grupo **all_sprites** e também desenhando eles (neste exemplo é apenas um Sprite). Preenchemos o fundo com a cor preta, que eventualmente nos fornece o seguinte resultado:

![img](/Screenshots/screenshot6.png)

### Efeitos Sonoros

O módulo [pygame.mixer](https://www.pygame.org/docs/ref/mixer.html) permite reproduzir arquivos [OGG](https://en.wikipedia.org/wiki/Ogg) compactados ou [WAV](https://en.wikipedia.org/wiki/WAV) descompactados.

O exemplo a seguir verifica os parâmetros de inicialização e imprime o número de canais disponíveis. Ele inicializa um objeto som e imprime o tempo do arquivo em segundos, ao pressionarmos a tecla `[Enter]` o som de um [Corvo Americano](/Exemplos/Sound/american_crow_spring.ogg) será tocado.

```python
import pygame
pygame.mixer.init()

print(f'init = {pygame.mixer.get_init()}')
print(f'channels = {pygame.mixer.get_num_channels()}')
som = pygame.mixer.Sound('american_crow_spring.ogg')
print(f'length = {som.get_length()}')

while True:
    input('Aperte Enter para tocar o Som')
    som.play()
    print('Tocando o som... CTRL+Z para cancelar')
```

Para cancelarmos a execução do script podemos usar os comandos `CTRL + Z` ou `CTRL + D`.

No exemplo a seguir vamos tocar a [Piano Sonata No. 14](https://en.wikipedia.org/wiki/Piano_Sonata_No._14_(Beethoven)) de [Ludwig van Beethoven](https://en.wikipedia.org/wiki/Ludwig_van_Beethoven), popularmente conhecida como [Moonlight Sonata](https://github.com/the-akira/PyGameDev/blob/master/Exemplos/Sound/beethoven.ogg).

```python
from pygame.locals import *
import pygame

WIDTH = 500
HEIGHT = 150
FPS = 60

BLACK = (13, 13, 13)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
logo = pygame.image.load("icon.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Moonlight Sonata - Beethoven")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
sound = pygame.mixer.Sound('beethoven.ogg') 
sound.set_volume(0.7)
myriad_pro_font = pygame.font.SysFont("Myriad Pro", 48)
text = myriad_pro_font.render("p = play | s = stop", 1, WHITE)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                sound.stop()

    screen.fill(BLACK)
    screen.blit(text, (100, 50))
    pygame.display.flip()

pygame.quit()
```

Este exemplo irá nos apresentar a seguinte tela:

![img](/Screenshots/screenshot7.png)

Usamos a tecla **p** para dar Play na música e a tecla **s** para dar Stop.

Perceba também que estamos carregando um [ícone de música](/Exemplos/Sound/icon.png) para customizar nossa janela.

### Debugging

[Debugging](https://en.wikipedia.org/wiki/Debugging) é o processo de detecção e remoção de erros existentes e potenciais (também chamados de 'bugs') em um código de software, que podem fazer com que ele se comporte inesperadamente ou falhe. Para evitar a operação incorreta de um software ou sistema, debugging é usada para localizar e resolver bugs ou defeitos.

Sabemos que no Pygame temos um Game Loop e que quando ele está executando é interessante que possamos inspecionar o valor de certas variáveis que estão sofrendo alterações, para isso, poderíamos utilizar o comando **print()**, porém seria inconveniente devido ao fato de que o valor será impresso muitas vezes na tela e será difícil de rastreá-lo.

Para solucionar este problema com o comando **print()**, podemos utilizar as próprias funcionalidades da biblioteca Pygame, utilizando o módulo [pygame.font](https://www.pygame.org/docs/ref/font.html) para carregar e renderizar fontes.

No [exemplo a seguir](https://github.com/the-akira/PyGameDev/tree/master/Exemplos/Debugging) vamos definir uma função chamada **debug** que receberá como argumento um valor a ser inspecionado e também as coordenadas em que ele será apresentado na tela:

```python
import pygame 
pygame.init()

WIDTH = 835
HEIGHT = 450
FPS = 30
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 33)

def debug(info, x=10, y=10):
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, WHITE)
    debug_rect = debug_surface.get_rect(topleft=(x,y))
    display_surface.blit(debug_surface, debug_rect)

class Bug(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_left = pygame.image.load(f'images/{num}.png').convert_alpha()
            new_dimension = (int(img_left.get_width() * scale), int(img_left.get_height() * scale))
            img_left = pygame.transform.scale(img_left, new_dimension)
            img_right = pygame.transform.flip(img_left, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)   
        self.image = self.images_right[self.index]    
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y
        self.direction = 0

    def update(self):
        dx = 0 
        dy = 0
        walk_cooldown = 4
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            dx -= 6
            self.counter += 1
            self.direction = -1
            if self.rect.left <= 0:
                self.rect.left = 0
        if key[pygame.K_RIGHT]:
            dx += 6
            self.counter += 1
            self.direction = 1
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1 
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        self.rect.x += dx 
        self.rect.y += dy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Debugging')
clock = pygame.time.Clock()

background = pygame.image.load('images/bg.png').convert_alpha()
all_sprites = pygame.sprite.Group()
player = Bug(50, 165, 0.3)
all_sprites.add(player)

running = True 
while running:
    screen.blit(background,(0,0))
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    all_sprites.update()
    all_sprites.draw(screen)
    debug((player.rect.x, player.rect.y))
    debug(pygame.mouse.get_pressed(), 380)
    debug(pygame.mouse.get_pos(), 725)
    pygame.display.flip()

pygame.quit()
```

Este exemplo nos trará o seguinte resultado:

![img](/Screenshots/screenshot12.png)

Observe que na primeira tupla estamos apresentando os valores **x** e **y** que representam a posição do jogador, na tupla do meio estamos mostrando o estado de cada botão do mouse (esquerda, centro e direita), sendo 0 indicando que ele não está pressionado e 1 indicando que está, e por fim, na última tupla temos os valores **x** e **y** da posição do cursor.

Perceba também que é possível mover o personagem para a esquerda e direita (utilizando as setas do teclado), além disso, estamos animando o personagem ao carregar diversas imagens e realizar um loop circular por elas ao sempre resetar o seu índice.

Com essa técnica de debugging, podemos agora inspecionar as variáveis internas de nossos Games com mais facilidade, fazendo que consigamos solucionar os problemas com mais agilidade e eficiência.

## Construindo um Platform Game

Uma vez que adquirimos o conhecimento dos fundamentos essenciais da biblioteca Pygame, vamos agora construir um [Platform Game](https://en.wikipedia.org/wiki/Platform_game) básico que servirá como estrutura para criarmos nossos Games, nos permitindo adicionar mais features a ele quando desejarmos.

Os jogos de plataforma (muitas vezes simplificados como *platformers* ou *jump 'n' run*) são um gênero de vídeo-game e um subgênero de jogos de ação. Esses Games são caracterizados pelo uso intenso de saltos e escaladas para navegar pelo ambiente do jogador e alcançar seu objetivo. Os níveis e ambientes tendem a apresentar terrenos irregulares e plataformas suspensas de alturas variáveis que exigem o uso das habilidades do personagem do jogador para atravessar.

Games como [Super Mario World](https://en.wikipedia.org/wiki/Super_Mario_World), [Super Castlevania IV](https://en.wikipedia.org/wiki/Super_Castlevania_IV) e [Sonic the Hedgehog](https://en.wikipedia.org/wiki/Sonic_the_Hedgehog_(1991_video_game)) são exemplos de platform games.

Neste exemplo, vamos emular um simples Mario [8-bit](https://en.wikipedia.org/wiki/8-bit).

Vamos usar apenas duas imagens:

- O personagem [Mario](/Exemplos/Mario%202.0/mario.png)
- O [tijolo](/Exemplos/Mario%202.0/brick.png) tradicional do Game Mario

### Estrutura do Jogo

Nosso jogo é composto por três classes principais e uma função **main()**, responsáveis por organizar toda a lógica de funcionamento, movimentação, câmera e renderização do cenário. Também temos a função auxiliar **create_level()**, que constrói o nosso mapa a partir de uma matriz de strings.

As classes utilizadas são:

- **Camera:** Responsável por controlar a câmera do jogo, fazendo com que ela siga o personagem e respeite os limites do mapa.
- **Player:** Representa o personagem controlado pelo jogador, incluindo movimento, física, pulo e colisões.
- **Platform:** Representa os blocos sólidos do cenário, sobre os quais o personagem pode caminhar e colidir.

Na função **main()** inicializamos o mapa, carregamos os sprites, configuramos a câmera e executamos o Game Loop, que é responsável por atualizar e desenhar o jogo na tela.

Vejamos então o código para compreendermos melhor:

```python
import pygame

# Configurações globais
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
SCREEN_SIZE = pygame.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
INITIAL_POS = (35, 500) # Posição inicial mais adequada
BACKGROUND_BLUE = (104, 136, 247)
GRAVITY = 0.5
JUMP_STRENGTH = -12 # Valor negativo para ir para cima
PLAYER_SPEED = 5
TILE_SIZE = 32
FPS = 60

class Camera:
    def __init__(self, target, world_width, world_height):
        self.target = target
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self):
        x = -self.target.rect.centerx + SCREEN_WIDTH // 2
        y = -self.target.rect.centery + SCREEN_HEIGHT // 2
        
        # Limitar a câmera aos limites do mundo
        x = min(0, x)  # Lado esquerdo
        x = max(-(self.world_width - SCREEN_WIDTH), x)  # Lado direito
        y = min(0, y)  # Topo
        y = max(-(self.world_height - SCREEN_HEIGHT), y)  # Base
        
        self.camera = pygame.Rect(x, y, self.world_width, self.world_height)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, platforms):
        super().__init__()
        self.original_image = pygame.image.load('mario.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (45, 55))
        self.image = self.original_image
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.image.get_rect(topleft=pos)
        
        # Física
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, GRAVITY)
        self.on_ground = False
        self.platforms = platforms
        
        # Movimento
        self.speed = PLAYER_SPEED
        self.jump_strength = JUMP_STRENGTH
        self.running_multiplier = 1.5

    def update(self):
        self.handle_input()
        self.apply_physics()
        self.handle_collisions()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.image = self.flipped_image
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.image = self.original_image
            
        # Aceleração (corrida)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.x *= self.running_multiplier
            
        # Pulo
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

    def apply_physics(self):
        # Aplicar gravidade
        if not self.on_ground:
            self.velocity.y += self.acceleration.y
            # Limitar velocidade de queda
            self.velocity.y = min(self.velocity.y, 15)

    def handle_collisions(self):
        # Movimento horizontal
        self.rect.x += self.velocity.x
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:  # Movendo para a direita
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:  # Movendo para a esquerda
                    self.rect.left = platform.rect.right

        # Movimento vertical
        self.rect.y += self.velocity.y
        self.on_ground = False
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:  # Caindo
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Pulando
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_load = pygame.image.load('brick.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_load, (TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

def create_level(level_layout, platform_group, all_sprites):
    for y, row in enumerate(level_layout):
        for x, tile in enumerate(row):
            if tile == "P":
                Platform((x * TILE_SIZE, y * TILE_SIZE)).add(platform_group, all_sprites)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mario")
    clock = pygame.time.Clock()

    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                      P",
        "P                                                      P",
        "P                                                      P",
        "P                    PPPPPPPPPPP                       P",
        "P                                                      P",
        "P                                            PPPPP     P",
        "P                                   PPP                P",
        "P    PPPPPPPP                                          P",
        "P                                                    PPP",
        "P                          PPPPPPP                     P",
        "P                 PPPP                   PPPPPP        P",
        "P                                                      P",
        "P         PPPP                                         P",
        "P                                                      P",
        "P                     PPPPPP          PPPPPPPPPP       P",
        "P                                                      P",
        "P   PPPPPPPPPPP                                        P",
        "P                                                      P",
        "P                       PPPPPPPP              PPPPPPPPPP",
        "P                                                      P",
        "P             PPPPPP                                   P",
        "P                                                      P",
        "P                                                      P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    
    # Criar nível
    level_width = len(level[0]) * TILE_SIZE
    level_height = len(level) * TILE_SIZE
    create_level(level, platforms, all_sprites)
    
    # Criar jogador
    player = Player(INITIAL_POS, platforms)
    all_sprites.add(player)
    
    # Configurar câmera
    camera = Camera(player, level_width, level_height)

    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Atualizações
        all_sprites.update()
        camera.update()
        
        # Desenho
        screen.fill(BACKGROUND_BLUE)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
```

Irei salvar o código como `mario.py` e executá-lo com o comando `python mario.py`, que irá me trazer o seguint *output*:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Screenshots/screenshot8.png)

Usamos as Arrow Keys para movimentar o personagem pela tela. Para encerrar o Game podemos clicar no botão fechar ou pressionar a tecla `[ESC]`.

Devemos agora considerar alguns detalhes importantes sobre nosso código.

### Configurações Globais

Antes da definição das classes, declaramos algumas constantes globais que controlam o comportamento do jogo:

```python
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
SCREEN_SIZE = pygame.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
INITIAL_POS = (35, 500)
BACKGROUND_BLUE = (104, 136, 247)
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
TILE_SIZE = 32
FPS = 60
```

Essas constantes facilitam ajustes futuros e tornam o código mais organizado, centralizando valores importantes como:

- **SCREEN_WIDTH e SCREEN_HEIGHT:** Definem a largura e a altura da janela do jogo, em pixels. Neste projeto, a tela possui 800×640 pixels.
- **SCREEN_SIZE:** Cria um objeto `pygame.Rect` que representa a área visível da tela. Esse retângulo pode ser utilizado para cálculos de câmera, limites de tela e centralização de elementos.
- **INITIAL_POS:** Define a posição inicial do jogador no mapa, em coordenadas (x, y). Esse valor foi escolhido para posicionar o personagem em um ponto seguro do cenário ao iniciar o jogo.
- **BACKGROUND_BLUE:** Define a cor de fundo da tela no formato RGB. Neste caso, é um tom de azul usado para representar o céu.
- **GRAVITY:** Valor que representa a força da gravidade aplicada ao personagem. Esse número é somado à velocidade vertical a cada frame enquanto o personagem está no ar.
- **JUMP_STRENGTH:** Define a força do pulo do personagem. O valor é negativo porque, no sistema de coordenadas do Pygame, valores negativos no eixo Y fazem o objeto subir.
- **PLAYER_SPEED:** Controla a velocidade horizontal do personagem ao se mover para a esquerda ou direita.
- **TILE_SIZE:** Define o tamanho padrão dos blocos do cenário (plataformas), em pixels. Esse valor é usado tanto para renderização quanto para o cálculo do mapa.
- **FPS:** Define a taxa máxima de quadros por segundo do jogo. Um valor de 60 FPS garante uma movimentação suave e consistente.

### Classe Camera

A classe **Camera** é responsável por simular uma câmera que acompanha o personagem pelo mapa. Em vez de mover diretamente o jogador pela tela, o que fazemos é mover o mundo ao redor dele.

A câmera recebe como parâmetros:

- O alvo (**target**), que será o jogador
- A largura e altura do mundo

#### Atualização da Câmera

No método **update()**, calculamos a posição da câmera de modo que o jogador fique centralizado na tela:

```python
x = -self.target.rect.centerx + SCREEN_WIDTH // 2
y = -self.target.rect.centery + SCREEN_HEIGHT // 2
```

Em seguida, limitamos o deslocamento da câmera para impedir que ela mostre áreas fora do mapa:

```python
x = min(0, x)
x = max(-(self.world_width - SCREEN_WIDTH), x)
```

Isso garante que a câmera nunca ultrapasse os limites do cenário.

#### Aplicação da Câmera

O método **apply()** ajusta a posição dos sprites antes de desenhá-los na tela:

```python
def apply(self, entity):
    return entity.rect.move(self.camera.topleft)
```

Dessa forma, todos os objetos do jogo são desenhados considerando o deslocamento da câmera.

### Classe Player

A classe **Player** representa o personagem principal do jogo. Ela herda de `pygame.sprite.Sprite` e encapsula toda a lógica de movimentação, física e colisões.

O personagem possui:

- Um sprite original e um sprite invertido.
- Vetores de velocidade e aceleração.
- Controle de estado para saber se está no chão.
- Referência às plataformas do cenário.

#### Entrada do Jogador

A leitura do teclado ocorre no método **handle_input()**:

- Setas esquerda e direita movem o personagem horizontalmente.
- Seta para cima faz o personagem pular (apenas se estiver no chão).
- Barra de espaço permite correr.

A velocidade horizontal é redefinida a cada frame, garantindo um movimento preciso e previsível.

#### Física e Gravidade

No método **apply_physics()**, aplicamos a gravidade ao personagem sempre que ele estiver no ar:

```python
self.velocity.y += self.acceleration.y
```

Também limitamos a velocidade máxima de queda para manter o controle do movimento.

#### Colisões

As colisões são tratadas no método **handle_collisions()** e ocorrem separadamente em cada eixo, uma técnica amplamente utilizada em jogos 2D.

**Colisões no eixo X**

- O personagem se move horizontalmente.
- Caso haja colisão, sua posição é ajustada para evitar atravessar a plataforma.

**Colisões no eixo Y**

- O personagem se move verticalmente.
- Detectamos se ele está caindo ou pulando.
- Quando toca o chão, o estado **on_ground** é ativado.

**Esse processo garante:**

- Pulos consistentes.
- Detecção correta de chão.
- Interações físicas estáveis.

### Classe Platform

A classe **Platform** representa os blocos sólidos do cenário, neste caso, os tijolos. Cada plataforma possui um sprite e um retângulo de colisão.

Esses objetos são usados tanto para renderização quanto para detecção de colisões com o jogador.

### Construção do Mapa

O mapa do jogo é definido como uma **lista de strings**, onde cada caractere representa um elemento do cenário:

- "P" indica uma plataforma sólida
- Espaços representam áreas vazias

```python
for y, row in enumerate(level_layout):
    for x, tile in enumerate(row):
        if tile == "P":
            Platform((x * TILE_SIZE, y * TILE_SIZE))
```

A função **create_level()** percorre essa matriz e cria os blocos correspondentes no mundo do jogo.

Essa abordagem torna o mapa fácil de visualizar, editar e expandir.

### Função main() e Game Loop

Na função **main()** inicializamos o [Pygame](https://www.pygame.org/news), configuramos a janela, criamos o nível, o jogador e a câmera.

Em seguida, iniciamos o Game Loop, que executa continuamente enquanto o jogo estiver rodando e irá:

1. Processar eventos (teclado e fechamento da janela).
2. Atualizar a lógica dos objetos.
3. Atualizar a câmera.
4. Desenhar o cenário na tela.
5. Controlar a taxa de FPS.

Durante a renderização, todos os sprites são desenhados com a posição ajustada pela câmera:

```python
screen.blit(sprite.image, camera.apply(sprite))
```

Isso cria o efeito de deslocamento do mundo conforme o personagem se move.

Com essa estrutura, temos um jogo de plataforma 2D funcional, organizado e fácil de expandir. A separação clara entre câmera, personagem e cenário facilita a manutenção do código e permite a adição de novos recursos, como inimigos, animações, fases adicionais e itens coletáveis.

## Conclusão

Através deste tutorial fomos capazes de aprender diversos conceitos importantes no campo de Desenvolvimento de Games 2D, porém exploramos somente a superfície deste grandioso universo. 

Com este conhecimento obtido, podemos agora aprofundar nossa sabedoria, para isso, fiz esta [lista de materiais importantes](https://github.com/the-akira/PyGameDev/blob/master/Materiais.md) que poderá nos ajudar bastante e que também serviu como inspiração e referência quando escrevi este material.

Você também poderá explorar todos os códigos utilizados neste tutorial no repositório do GitHub: [PyGameDev](https://github.com/the-akira/PyGameDev/tree/master/Exemplos). Espero que você possa aperfeiçoá-los e criar games ultra divertidos.

Boa diversão e bons estudos.
