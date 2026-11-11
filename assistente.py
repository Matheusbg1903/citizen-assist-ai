import csv
import json
import os
import time
from datetime import datetime

LIMITE_ALTA = 6
LIMITE_MEDIA = 3

CAMPOS_CSV = ["data", "sessao", 'origem', "pergunta", "id_orientacao",
              "encontrou", "ajudou", "tentativas", "tempo_segundos",
              "facilidade"]


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.sessao = datetime.now().strftime("%Y%m%d-%H%M%S%F")
        self.opcoes_extras = []
        self.caminho_historico = self.carregar_historico()

    def _ler_numero(self, texto, minimo, maximo):
        while True:
            valor = input(texto).strip()
            try: 
                numero = int(valor)
            except ValueError:
                numero = None
            if numero is not None and minimo <= numero <= maximo:
                return numero
            print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")

    def _ler_sim_nao(self, texto):
        while True:
            valor = input(texto).strip().lower()
            if valor in ("s", "sim"):
                return True
            if valor in ("n", "nao", "não"):
                return False
            print("Resposta inválida. Digite s ou n.")

    def _tem_dado_pessoal(self, texto):
        # 8+ digitos (cpf, telefone) ou @ (email)
        digitos = sum(1 for letra in texto if letra.isdigit())
        return digitos >= 8 or "@" in texto

    def nivel_confianca(self, pontos):
        if pontos >= LIMITE_ALTA:
            return "ALTA"
        if pontos >= "MEDIA":
            return "MEDIA"
        return None
    


    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m%d %H:%M:%S"),
            "sessao": self.sessao,
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "facilidade": None,
        }
        self.historico.append(atendimento)
        self.salvar_historico()

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            return[]
        except(json.JSONDecodeError, OSError):
            print("Atenção: histórico ilegível. Um novo será iniciado.")
            return[]
        if not isinstance(dados, list):
            return[]
        return [item for item in dados if isinstance(item, dict)]

    def salvar_historico(self):
        try:
            pasta = os.path.dirname(self.caminho_historico)
            if pasta:
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho_histórico, "w", encoding="utf8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, ident=2)
        except OSError:
            print("Atenção: Não foi possível salvar o histórico.")



    def perguntar(self):
        # repete até o usuário digitar 0
        while self._atender_pergunta():
            pass

    def _atender_pergunta(self):
        inicio = time.time()
        tentativas = 0
        pergunta = ""
        encontrou = False
        ajudou = False
        id_orientacao = None
        voltar = False

        while True:
            texto = input("/nDigite sua dúvida (0 para voltar): ").strip()
            if texto == '0':
                voltar = True
                break
            if texto == '':
                print("Digite um apergunta ou 0 para voltar.")
                continue
            if self._tem_dado_pessoal(texto):
                #não conta como tentativa nem é registrada
                print("Atenção: não digite o seu CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            pergunta = texto
            resultados = self.base.buscar(texto)

            if not resultados or resultados[0][0] < LIMITE_MEDIA:
                self._mostrar_nao_encontrei()
                continue

            encontrou = True
            ajudou, id_orientacao = self._apresentar(resultados)
            if ajudou:
                break

        if tentativas > 0:
            tempo = round(time.time() - inicio, 1)
            self.registrar("perguntas", pergunta, id_orientacao, encontrou,
                           ajudou, tentativas, tempo)
            
        return not voltar
    
    def _apresentar(self, resultados):
        pontos, melhor = resultados[0]
        print(f"\nCOnfiança da resposta: {self.nivel_confianca(pontos)}"
              f"({pontos} pontos)\n")
        melhor.exibir()
        if self._ler_sim_nao("\nEssa orientação respondeu  sua dúvida? (S/N)"):
            return True, melhor.id

        # até duas alternativas, só as com 3+ pontos
        alternativas = [(p, o) for p, o in resultados[1:3] if p >= LIMITE_MEDIA]
        for pontos_alt, alternativa in alternativas:
            print(f"\nOutra possibilidade "
                  f"({self.nivel_confianca(pontos_alt)}, {pontos_alt} pontos):\n")
            alternativa.exibir()
            if self._ler_sim_nao("\nEssa orientação respondeu sua dúvida? (S/N): "):
                return True, alternativa.id

            print("\nTente reescrever a pergunta com outras palavras.")
            return False, melhor.id

    def _mostrar_nao_encontrei(self):
        print("\nNão encontrei uma orientação para essa dúvida.")
        print("Tente outras palavras ou use a navegação por categorias.")
        categorias = self.base.categorias()
        if categorias:
            print("Categorias disponíveis: " + ", ".join(categorias))



    def navegar(self):
        while True:
            categorias = self.base.categorias()
            if not categorias:
                print("Nenhuma categoria disponível.")
                return
            print("\nCategorias:")
            for numero, categoria in enumerate(categorias, start=1):
                print(f" {numero}, {categoria}")
            print(" 0. Voltar")
            escolha = self._ler_numero("Escolha uma categoria: ",
                                       0, len(categorias))
            if escolha == 0:
                return
            self._navegar_categoria(categorias[escolha - 1])

    def _navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            print(f"\n{categoria}:")
            for numero, orientacao in enumerate(orientacoes, start=1):
                print(f" {numero}. {orientacao.titulo}")
            print(" 0. Voltar")
            escolha = self._ler_numero("Escolha uma orientação: ",
                                       0, len(orientacoes))
            if escolha == 0: return
            return

        inicio = time.time()
        orientacao = orientacoes[escolha -1]
        print()
        orientacao.exibir()
        ajudou = self._ler_sim_nao(
            "\nEssa orientação respondeu dúvida? (S/N)")
        tempo = round(time.time() - inicio, 1)
        self.registrar("categoria", orientacao.titulo, orientacao.id,
                       True, ajudou, 1, tempo)

    
    
    def _media(self, valores):
        return sum(valores) / len (valores) if valores else 0

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            return None

        encontrados = [h for h in self.historico if h.get("encontrou")]
        ajudaram = [h for h in self.historico if h.get("ajudou")]

        # a nota  é por sessão, então conta cada sessão uma vez
        notas_por_sessao = {}
        for h in self.historico:
            if h.get("facilidade") is not None:
                notas_por_sessao[h.get("sessao")] = h["facilidade"]

        sem_solucao = []
        for h in self.historico:
            if h.get("origem") == "pergunta" and not h.get("ajudou"):
                pergunta = h.get("pergunta", "")
                if pergunta and pergunta not in sem_solucao:
                    sem_solucao.append(pergunta)

        return{
            "total": total,
            "resposta_encontrada": len(encontrados) / total * 100,
            "taxa_acerto": len(ajudaram) / 100,
            "tempo_medio": self._media(
                [h.get("tempo_segundos", 0) for h in encontrados]),
            "tentivas_medias": self._media(
                [h.get("tentiva", 1)for h in self.historico]),
            "facilidades": (self._media(list(notas_por_sessao.values()))
                            if notas_por_sessao else None),
                            "sem_solucao": sem_solucao,
        }

    def mostrar_indicadores(self):
        dados = self.indicadores()
        if dados is None:
            print("\nAinda não há atendimentos registrados.")
            return
        print("\n=== Indicadores ===")
        print(f"Atendimentos: {dados['total']}")
        print(f"Resposta encontrada (%): {dados['resposta_encontrada']:.1f}")
        print(f"Taxa de acerto: ajudou (%): {dados['taxa_acerto']:.1f}")
        print(f"Tempo médio para encontrar: {dados['tempo_medio']:.1f} s")
        print(f"Tentativas por atendimento: {dados['tentativas_medias']:.1f}")
        if dados["facilidade"] is None:
            print("Facilidade de uso (1 a 5): sem nota ainda")
        else: 
            print(f"Facilidade de uso (1 a 5): {dados['facilidade']:.1f}")
        print("Dúvidas sem solução: ")
        if dados["sem_solucao"]:
            for pergunta in dados["sem_solucao"]:
                print(f" -{pergunta}")
        else:
            print(" (nenhuma)")

            def exportar_csv(self):
                try:
                    pasta = os.path.dirname(self.caminho_csv)
                    if pasta:
                        os.makedirs(pasta, exist_ok=True)
                    #utf-8-sig pro excel abriuros acentos certo
                    with open(self.caminho_csv, "w", newline="",
                              encoding="utf-8-sig") as arquivo:
                        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV,
                                                  extrasaction="ignore")
                        escritor.writeheader()
                        for atendimento in self.historico:
                            escritor.writerow(atendimento)
                    print(f"Atendimentos exportados para {self.caminho_csv}.")
                except OSError:
                    print("Atenção: não foi possível exportar o CSV.") 