
from types import SimpleNamespace
from base_conhecimento import BaseConhecimento

base = BaseConhecimento("data/base_conhecimento.json")

orientacao = SimpleNamespace(
    titulo="Solicitar segunda via de documento",
    palavras_chave=["segunda via", "documento"],
    categoria="Documentação"
)

base.orientacoes = [orientacao]

# Teste de pontuação
pontos = base.pontuar(
    "Como solicitar segunda via do documento?",
    orientacao
)

print("Pontuação:", pontos)

# Teste de busca
resultados = base.buscar(
    "Como solicitar segunda via do documento?"
)

print("Resultados encontrados:", len(resultados))

for pontuacao, item in resultados:
    print(f"{item.titulo}: {pontuacao} pontos")

assert pontos > 0
assert len(resultados) == 1

print("Todos os testes passaram!")
