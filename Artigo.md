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

O comando `pygame.time.Clock()` cria um [objeto relógio](https://www.pygame.org/docs/ref/time.html#pygame.time.Clock) que nos ajuda a rastrear o tempo. O relógio também fornece várias funções para ajudar a controlar a taxa de frames de um jogo.