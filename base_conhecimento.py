import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
            "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
         texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
         texto = texto.replace(sinal, " ")
    # espaço nas pontas pra comaprar  palavra inteira
    return " " + " ".join(texto.split()) + " "
     

class BaseConhecimento: 
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                registros = json.load(arquivo)
        except FileNotFoundError:
            print("Atenção: base de conhecimento não encontrada.")
            return False
        except (json.JSONDecodeError, OSError):
                print("Atenção: base de conhecimento ilegível ou corrompida.")
                return False

        if not isinstance(registros, list):
             print("Atenção: a base deve ser uma lista de orientações.")
             return False

        for registro in registros:
             try:
                  self.orientacoes.append(Orientacao(**registro))
             except TypeError:
                  print("Atenção: um regsitro com campos inválidos foi ignorado.")
        return len(self.orientacoes) > 0

    def categorias(self):
         return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
         return [o for o in self.orientacoes if o.categoria == categoria]