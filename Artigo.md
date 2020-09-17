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

**[Pygame](https://www.pygame.org/)** é um conjunto de módulos Python projetados para escrever vídeo-games. O Pygame adiciona funcionalidades à excelente [biblioteca SDL](https://www.libsdl.org/), que significa **Simple DirectMedia Layer**. SDL fornece acesso *cross-platform* aos componentes de hardware de multimídia do seu sistema, como **som**, **vídeo**, **mouse**, **teclado** e **joystick**. Nos permitindo criar jogos completos e também programas multimídia na linguagem Python.

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

Observe que cada exemplo apresenta uma funcionalidade que o Pygame nos proporciona.