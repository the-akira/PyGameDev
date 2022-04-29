# Tiled PyGame

Neste tutorial vamos aprender como podemos utilizar a ferramenta [Tiled](https://www.mapeditor.org/) para construir níveis para os nossos Games e depois importá-los com a biblioteca [PyGame](https://www.pygame.org).

**Tiled** é um editor de níveis gratuito e de código aberto, fácil de usar e flexível.

Você pode obter o **Tiled** através do seguinte link: [Download](https://thorbjorn.itch.io/tiled)

Uma vez que você fez o download e instalou **Tiled**, vamos para o primeiro passo:

1. Devemos selecionar a opção `Ficheiro → Novo Mapa...` ou `CTRL + N`:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/1.png)

2. Aparecerá uma janela com algumas opções para selecionarmos, por hora, vamos escolher as seguintes configurações:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/2.png)

3. Surgirá uma grade de dimensão `150 × 20` no qual iremos desenhar o nosso nível, vamos agora carregar o nosso [tileset](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/imagens/tileset.png) através da opção `Novo Tileset...`:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/3.png)

4. Devemos então clicar no botão `Explorar...`, buscar o caminho do nosso [tileset](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/imagens/tileset.png) em nossa máquina e então confirmar com a opção `OK`, de acordo com a ilustração a seguir:

[img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/4.png)

5. Uma vez que temos o nosso **tileset** carregado, podemos então desenhar o nosso nível conforme o nosso desejo:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/5.png)

**Observação:** O bloco vermelho tem como intuito marcar a posição inicial do nosso jogador.

6. Com o nosso nível pronto, podemos então exportá-lo para o formato `csv` através da opção `Ficheiro → Exportar Como...`:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/6.png)

7. Finalmente, podemos escolher o caminho no qual o arquivo `csv` será salvo e também o seu nome:

![img](https://raw.githubusercontent.com/the-akira/PyGameDev/master/Exemplos/Mario%203.0/tutorial/imagens/7.png)

Agora temos o nosso nível em um formato que podemos facilmente carregar em nosso Game!

Neste **[exemplo](https://github.com/the-akira/PyGameDev/tree/master/Exemplos/Mario%203.0)** mostramos como carregar um nível e desenhá-lo na tela. Também temos um personagem que pode caminhar pelo nível com as devidas colisões e *scrolling* da tela. Bons estudos!