# Criando um Mapa com Tiled e PyGame

Neste tutorial vamos aprender como podemos utilizar a ferramenta [Tiled](https://www.mapeditor.org/) para construir mapas para os nossos Games e depois importá-los com a biblioteca [PyGame](https://www.pygame.org).

**Tiled** é um editor de mapas gratuito e de código aberto, fácil de usar e flexível.

Você pode obter o **Tiled** através do seguinte link: [Download](https://thorbjorn.itch.io/tiled)

Uma vez que você fez o download e instalou **Tiled**, vamos para o primeiro passo:

**1**: Devemos selecionar a opção `Ficheiro → Novo Mapa...` ou `CTRL + N`:

![img](/Exemplos/Mario%203.0/tutorial/imagens/1.png)

**2**: Aparecerá uma janela com algumas opções para selecionarmos, por hora, vamos escolher as seguintes configurações e então confirmar com a opção `OK`:

![img](/Exemplos/Mario%203.0/tutorial/imagens/2.png)

**3**: Surgirá uma grade de dimensão `150 × 20` no qual iremos desenhar o nosso mapa, vamos agora carregar o nosso [tileset](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/imagens/tileset.png) através da opção `Novo Tileset...`:

![img](/Exemplos/Mario%203.0/tutorial/imagens/3.png)

**4**: Devemos então clicar no botão `Explorar...`, buscar o caminho do nosso [tileset](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/imagens/tileset.png) em nossa máquina e então confirmar com a opção `OK`, de acordo com a ilustração a seguir:

![img](/Exemplos/Mario%203.0/tutorial/imagens/4.png)

**5**: Uma vez que temos o nosso **tileset** carregado, podemos então desenhar o nosso mapa conforme o nosso desejo:

![img](/Exemplos/Mario%203.0/tutorial/imagens/5.png)

**Observação**: O bloco vermelho tem como intuito marcar a posição inicial do nosso jogador.

**6**: Com o nosso mapa pronto, podemos então exportá-lo para o formato `csv` através da opção `Ficheiro → Exportar Como...`:

![img](/Exemplos/Mario%203.0/tutorial/imagens/6.png)

**7**: Finalmente, podemos escolher o caminho no qual o arquivo `csv` será salvo e também o seu nome:

![img](/Exemplos/Mario%203.0/tutorial/imagens/7.png)

Agora temos o nosso mapa em um formato que podemos facilmente carregar em nosso Game!

Neste **[exemplo](https://github.com/the-akira/PyGameDev/tree/master/Exemplos/Mario%203.0)** mostramos como carregar um mapa e desenhá-lo na tela. Também temos um personagem que pode caminhar pelo mapa com as devidas colisões e *scrolling* da tela: 

![img](/Exemplos/Mario%203.0/tutorial/imagens/screenshot.png)

Bons estudos!