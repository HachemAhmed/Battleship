import random  # Importa funções aleatórias
import os      # Importa funções para interação com o sistema operacional (ex: limpar tela)
import time    # Importa funções para manipulação de tempo (ex: pausas)
from typing import Tuple, Optional  # Importa tipagem para melhor definição de funções e variáveis
from colorama import init, Fore, Style  # Importa o Colorama para exibir cores no terminal

# Inicializa o Colorama para resetar as cores automaticamente após cada impressão
init(autoreset=True)

# Função principal do menu do jogo
def menu():
    while True:
        # Limpa a tela conforme o sistema operacional
        os.system('cls' if os.name == 'nt' else 'clear')
        # Exibe o cabeçalho do jogo com bordas
        print(Fore.CYAN + "╔════════════════════════╗")
        print("║     BATALHA NAVAL      ║")
        print("╚════════════════════════╝" + Style.RESET_ALL)
        # Exibe as opções do menu
        print("1. Iniciar Novo Jogo")
        print("2. Instruções")
        print("3. Créditos")
        print("4. Sair")
        # Lê a escolha do usuário
        escolha = input("Escolha uma opção: ").strip()
        if escolha == '1':
            # Inicia um novo jogo
            jogo = JogoBatalhaNaval()
            jogo.jogar()
            input("\nPressione Enter para voltar ao menu...")
        elif escolha == '2':
            # Exibe as instruções do jogo
            mostrar_instrucoes()
        elif escolha == '3':
            # Exibe os créditos do jogo
            mostrar_creditos()
        elif escolha == '4':
            # Encerra o programa
            print("Saindo...")
            break
        else:
            # Se a opção for inválida, exibe mensagem de erro
            print(Fore.RED + "Opção inválida! Tente novamente." + Style.RESET_ALL)
            input("Pressione Enter para continuar...")

# Função que exibe as instruções do jogo
def mostrar_instrucoes():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + "╔════════════════════════╗")
    print("║      INSTRUÇÕES        ║")
    print("╚════════════════════════╝" + Style.RESET_ALL)
    # Instruções e regras do jogo
    print("\nRegras do jogo:")
    print(" - Cada jogador possui 5 navios para posicionar no tabuleiro 10x10")
    print(" - Os navios ocupam apenas uma posição")
    print(" - Não é permitido sobrepor navios")
    print(" - Para jogar, você e o computador alternam turnos")
    print("\nComo jogar:")
    print(" - Para posicionar navios e atirar, digite as coordenadas no formato: linha coluna")
    print(" - As coordenadas devem ser números entre 0 e 9")
    print(" - Digite 'ver' para revelar temporariamente os navios do computador")
    print(" - Digite 'sair' para encerrar o jogo")
    print("\nSímbolos no tabuleiro:")
    print(f"   {Fore.GREEN}N{Style.RESET_ALL} = Navio")
    print(f"   {Fore.RED}X{Style.RESET_ALL} = Tiro certeiro")
    print(f"   {Fore.BLUE}O{Style.RESET_ALL} = Tiro na água")
    print("   '~' = Mar")
    input("\nPressione Enter para voltar ao menu...")

# Função que exibe os créditos do jogo
def mostrar_creditos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA + "╔════════════════════════╗")
    print("║       CRÉDITOS         ║")
    print("╚════════════════════════╝" + Style.RESET_ALL)
    # Informações sobre os desenvolvedores
    print("\nDesenvolvido originalmente por Ahmed Hachem e João Pedro")
    input("\nPressione Enter para voltar ao menu...")

# Classe que representa um navio
class Navio:
    def __init__(self, posicao: Tuple[int, int]):
        # Armazena a posição do navio (linha, coluna)
        self.posicao = posicao
        # Conjunto que armazena os tiros que atingiram o navio
        self.hits = set()

    # Verifica se o navio foi afundado (ou seja, se recebeu um tiro em sua posição)
    def esta_afundado(self):
        return self.posicao in self.hits

    # Registra um tiro e verifica se acertou o navio
    def registar_hit(self, x: int, y: int) -> bool:
        if (x, y) == self.posicao:
            self.hits.add((x, y))
            return True
        return False

# Classe que representa o tabuleiro do jogo
class TabuleiroNaval:
    def __init__(self):
        # Lista de navios posicionados no tabuleiro
        self.Navios = []
        # Conjunto de posições que já receberam tiros
        self.tiros = set()
        # Define o tamanho do tabuleiro (10x10)
        self.tamanho = 10

    # Verifica se a posição (x, y) está dentro dos limites do tabuleiro
    def is_valid_posicao(self, x: int, y: int) -> bool:
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho

    # Verifica se a célula (x, y) está livre para posicionar um navio
    def is_cell_free(self, x: int, y: int) -> bool:
        return all((x, y) != Navio.posicao for Navio in self.Navios)

    # Posiciona um navio na posição (x, y) e retorna uma tupla com sucesso e mensagem
    def posicionar_navio(self, x: int, y: int) -> Tuple[bool, str]:
        if not self.is_valid_posicao(x, y):
            return False, f"Posição ({x}, {y}) está fora dos limites do tabuleiro!"
        if not self.is_cell_free(x, y):
            return False, f"Já existe um navio na posição ({x}, {y})!"
        self.Navios.append(Navio((x, y)))
        return True, "Navio posicionado com sucesso!"

    # Processa um tiro na posição (x, y) e retorna se acertou, se o jogo acabou e uma mensagem
    def receber_tiro(self, x: int, y: int) -> Tuple[Optional[bool], bool, str]:
        if not self.is_valid_posicao(x, y):
            return None, False, f"Tiro na posição ({x}, {y}) está fora dos limites!"
        if (x, y) in self.tiros:
            return None, False, f"Você já atirou na posição ({x}, {y})!"
        
        # Registra o tiro
        self.tiros.add((x, y))
        # Verifica se algum navio foi atingido
        hit = any(Navio.registar_hit(x, y) for Navio in self.Navios)
        # Verifica se todos os navios foram afundados
        game_over = all(Navio.esta_afundado() for Navio in self.Navios)
        
        mensagem = "ACERTOU um navio!" if hit else "Tiro na água!"
        return hit, game_over, mensagem

    # Retorna o conteúdo da célula (i, j) para exibição no tabuleiro
    def cell_content(self, i: int, j: int, mostrar_navios: bool) -> str:
        if (i, j) in self.tiros:
            # Se a célula recebeu um tiro, mostra 'X' se acertou ou 'O' se errou
            return (Fore.RED + 'X' + Style.RESET_ALL 
                   if any((i, j) == Navio.posicao for Navio in self.Navios) 
                   else Fore.BLUE + 'O' + Style.RESET_ALL)
        if mostrar_navios and any((i, j) == Navio.posicao for Navio in self.Navios):
            # Se estiver no modo de visualização, mostra o navio com cor verde
            return Fore.GREEN + 'N' + Style.RESET_ALL
        # Caso contrário, exibe a célula como mar (~)
        return Fore.BLUE + '~' + Style.RESET_ALL

    # Gera uma lista de strings representando o tabuleiro para exibição
    def mostrar(self, mostrar_navios: bool = False) -> list:
        linhas = []
        # Cabeçalho com os índices das colunas
        header = "    " + "   ".join(str(j) for j in range(self.tamanho))
        linhas.append(header)
        # Borda superior do tabuleiro
        top_border = "  ╔" + "═══╦" * (self.tamanho - 1) + "═══╗"
        linhas.append(top_border)
        # Cria cada linha do tabuleiro
        for i in range(self.tamanho):
            # Conteúdo de cada célula da linha
            row_content = " ║ ".join(self.cell_content(i, j, mostrar_navios) for j in range(self.tamanho))
            linha = f'{i} ║ ' + row_content + ' ║'
            linhas.append(linha)
            # Adiciona uma linha divisória, exceto após a última linha
            if i < self.tamanho - 1:
                middle_border = "  ╠" + "═══╬" * (self.tamanho - 1) + "═══╣"
                linhas.append(middle_border)
        # Borda inferior do tabuleiro
        bottom_border = "  ╚" + "═══╩" * (self.tamanho - 1) + "═══╝"
        linhas.append(bottom_border)
        return linhas

    # Retorna a quantidade de navios que ainda não foram afundados
    def navios_restantes(self) -> int:
        return sum(1 for Navio in self.Navios if not Navio.esta_afundado())

# Classe que gerencia a lógica do jogo Batalha Naval
class JogoBatalhaNaval:
    def __init__(self):
        # Cria os tabuleiros para o jogador e para o computador
        self.tabuleiro_jogador = TabuleiroNaval()
        self.tabuleiro_computador = TabuleiroNaval()
        # Configura o jogo posicionando os navios
        self.configurar_jogo()

    # Função para limpar a tela
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Função para ler as coordenadas fornecidas pelo usuário
    def ler_coordenadas(self, mensagem: str) -> Tuple[Optional[int], Optional[int], Optional[str]]:
        try:
            entrada = input(mensagem).strip().lower()
            if entrada == 'sair':
                return None, None, 'sair'
            if entrada == 'ver':
                return None, None, 'ver'
            # Separa a entrada em dois números (linha e coluna)
            x, y = map(int, entrada.split())
            return x, y, None
        except ValueError:
            # Se ocorrer erro na conversão, exibe mensagem de erro e aguarda o usuário
            print(Fore.RED + "Entrada inválida! Digite dois números separados por espaço (ex: 3 4)" + Style.RESET_ALL)
            input("Pressione Enter para tentar novamente...")
            return None, None, None

    # Função para configurar o jogo: posiciona os navios do computador e do jogador
    def configurar_jogo(self):
        # Posiciona aleatoriamente os navios do computador
        navios_computador = 0
        while navios_computador < 5:
            sucesso, _ = self.tabuleiro_computador.posicionar_navio(
                random.randint(0, 9), random.randint(0, 9)
            )
            if sucesso:
                navios_computador += 1

        # Permite que o jogador posicione seus navios
        print(Fore.CYAN + "\nPosicione seus navios!" + Style.RESET_ALL)
        navios_jogador = 0
        while navios_jogador < 5:
            self.mostrar_tabuleiros()
            print(f"\nNavios restantes para posicionar: {5 - navios_jogador}")
            x, y, comando = self.ler_coordenadas("Digite a posição do navio (linha coluna) ou 'sair': ")
            
            if comando == 'sair':
                # Se o usuário confirmar a saída, encerra o jogo
                if input("Deseja realmente sair? (s/n): ").lower() == 's':
                    exit()
                continue

            if comando == 'ver':
                continue

            if x is None:
                continue

            sucesso, mensagem = self.tabuleiro_jogador.posicionar_navio(x, y)
            if sucesso:
                navios_jogador += 1
            else:
                print(Fore.RED + mensagem + Style.RESET_ALL)
                input("Pressione Enter para continuar...")

    # Função que processa a jogada do computador
    def jogada_computador(self) -> bool:
        while True:
            # Gera coordenadas aleatórias para o tiro do computador
            x, y = random.randint(0, 9), random.randint(0, 9)
            hit, game_over, mensagem = self.tabuleiro_jogador.receber_tiro(x, y)
            
            if hit is not None:
                # Exibe o resultado da jogada do computador
                print(f"\nComputador atirou em ({x}, {y}): {mensagem}")
                time.sleep(1)  # Pausa para visualização
                return game_over
            
    # Função que exibe o status do jogo (quantidade de navios restantes)
    def mostrar_status_jogo(self):
        navios_jogador = self.tabuleiro_jogador.navios_restantes()
        navios_computador = self.tabuleiro_computador.navios_restantes()
        print(f"\nNavios restantes - Você: {navios_jogador} | Computador: {navios_computador}")

    # Função que exibe os tabuleiros do jogador e do computador lado a lado
    def mostrar_tabuleiros(self, mostrar_navios_computador: bool = False):
        self.limpar_tela()
        tab_jogador = self.tabuleiro_jogador.mostrar(True)
        tab_computador = self.tabuleiro_computador.mostrar(mostrar_navios_computador)

        # Adiciona um espaço extra na primeira linha (cabeçalho) do tabuleiro do computador
        tab_computador[0] = "  " + tab_computador[0]

        # Exibe um cabeçalho para os tabuleiros
        print(Fore.CYAN + "  ╔══════════════════════════════════════════════════════════════════════════════════════╗" + Style.RESET_ALL)
        print("                SEU TABULEIRO                                  COMPUTADOR")
        print(Fore.CYAN + "  ╚══════════════════════════════════════════════════════════════════════════════════════╝" + Style.RESET_ALL)
        # Exibe cada linha dos tabuleiros lado a lado
        for linha_jogador, linha_computador in zip(tab_jogador, tab_computador):
            print(linha_jogador + "    " + linha_computador)

    # Função principal que controla o fluxo do jogo
    def jogar(self):
        while True:
            # Turno do jogador: exibe tabuleiros e status
            self.mostrar_tabuleiros()
            self.mostrar_status_jogo()
            
            x, y, comando = self.ler_coordenadas("\nSua vez! Digite a posição do tiro (linha coluna) ou 'sair': ")
            
            if comando == 'sair':
                # Confirma se o jogador deseja sair
                if input("Deseja realmente sair? (s/n): ").lower() == 's':
                    break
                continue

            if comando == 'ver':
                # Modo de visualização dos navios do computador
                self.mostrar_tabuleiros(True)
                print(Fore.YELLOW + "\nModo VER ativado! Mostrando navios do computador..." + Style.RESET_ALL)
                input("Pressione Enter para continuar...")
                continue

            if x is None:
                continue

            # Processa o tiro do jogador no tabuleiro do computador
            hit, game_over, mensagem = self.tabuleiro_computador.receber_tiro(x, y)
            if hit is None:
                print(Fore.RED + mensagem + Style.RESET_ALL)
                input("Pressione Enter para continuar...")
                continue

            # Exibe o resultado do tiro do jogador
            if hit:
                print(Fore.GREEN + f"\nTiro em ({x}, {y}): {mensagem}" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"\nTiro em ({x}, {y}): {mensagem}" + Style.RESET_ALL)

            if game_over:
                # Se todos os navios do computador foram afundados, o jogador vence
                self.mostrar_tabuleiros(True)
                print(Fore.GREEN + "\nParabéns! Você venceu!" + Style.RESET_ALL)
                break

            # Turno do computador: processa sua jogada
            if self.jogada_computador():
                self.mostrar_tabuleiros(True)
                print(Fore.RED + "\nGame Over! O computador venceu!" + Style.RESET_ALL)
                break

            input("\nPressione Enter para continuar...")

# Ponto de entrada do programa
if __name__ == "__main__":
    menu()