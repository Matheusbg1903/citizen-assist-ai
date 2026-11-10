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