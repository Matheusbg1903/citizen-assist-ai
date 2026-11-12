# Citizen Assist AI – Conta de Luz em Dia

Assistente de terminal, feito em Python, que orienta famílias de baixa renda sobre a **conta de luz em atraso** e a **Tarifa Social de Energia Elétrica**. As respostas vêm de uma base de conhecimento verificada, sempre com a fonte oficial e a data de verificação.

> **Aviso:** este assistente NÃO é um canal oficial. Ele não substitui a distribuidora de energia, o CRAS nem a ANEEL.

Global Solution 2026.2 · FIAP · 1º ano de Ciência da Computação · Pensamento Computacional e Automação com Python

---

## Integrantes

|          Nome            |     RM    |
|--------------------------|-----------|
| Matheus Borges Soares    | RM 574085 |
| Erick Hernandes Penhabel | RM 570237 |
| Enzo Ricardo Silva       | RM 571333 |

## Público e problema

**Público:** famílias de baixa renda, inscritas ou não no CadÚnico, que estão com a conta de luz atrasada ou com medo de ter a energia cortada.

**Problema:** muitas famílias que têm direito à Tarifa Social não recebem o desconto. Os motivos mais comuns são a conta estar no nome de outra pessoa e o CadÚnico estar desatualizado. Além disso, quem está com a conta atrasada muitas vezes não conhece os próprios direitos: o aviso de 15 dias antes do corte, os dias em que o corte é proibido, o parcelamento obrigatório para baixa renda e o prazo de religação. Essas informações existem, mas estão espalhadas em resoluções da ANEEL e em sites diferentes, numa linguagem difícil. O assistente reúne tudo isso em respostas curtas, cada uma com a fonte.

## ODS relacionados

- **ODS 1 – Erradicação da pobreza:** acesso a um benefício social que reduz o custo de um serviço essencial.
- **ODS 7 – Energia limpa e acessível:** energia a preço acessível para famílias de baixa renda.
- **ODS 10 – Redução das desigualdades:** informação clara sobre direitos para quem mais precisa deles.

## Como executar

Requisito: Python 3.10 ou mais recente. Não usa bibliotecas externas.

```bash
git clone https://github.com/Matheusbg1903/citizen-assist-ai.git
cd citizen-assist-ai
python main.py
```

Menu principal:

1. **Fazer uma pergunta:** você digita a dúvida em texto livre e o assistente busca a melhor orientação.
2. **Navegar por categorias:** lista numerada de categorias e orientações, com "0 para voltar" em todas as telas.
3. **Ver indicadores:** mostra os indicadores calculados a partir do histórico de atendimentos.
4. **Exportar atendimentos (CSV):** gera o arquivo `data/atendimentos.csv`.
0. **Sair:** pede uma nota de facilidade de 1 a 5 e exporta o CSV.

## Estrutura do projeto

```
citizen-assist-ai/
├── README.md
├── main.py                  # ponto de entrada: carrega a base e inicia o assistente
├── orientacao.py            # classe Orientacao: um registro da base e exibir()
├── base_conhecimento.py     # classe BaseConhecimento: carregar, categorias, pontuar, buscar
├── assistente.py            # classe Assistente: atendimento, histórico, indicadores, CSV
└── data/
    ├── base_conhecimento.json   # 13 orientações em 3 categorias
    ├── historico.json           # atendimentos registrados
    └── atendimentos.csv         # exportação dos atendimentos
```

As classes se ligam por composição: o `Assistente` tem uma `BaseConhecimento`, e a `BaseConhecimento` tem uma lista de objetos `Orientacao`.

## Base de conhecimento

A base tem **13 orientações em 3 categorias**:

- **Tarifa Social e descontos (6):** quem tem direito, gratuidade até 80 kWh, Desconto Social, desconto que não veio na conta, CadÚnico, família com aparelho elétrico para tratamento de saúde.
- **Conta atrasada e corte (4):** quando a luz pode ser cortada, dias e horários em que o corte é proibido, parcelamento, multa e juros.
- **Religação e direitos (3):** religação depois de pagar, corte indevido, dívida do antigo morador.

Cada orientação tem de 5 a 8 palavras-chave, fonte oficial (ANEEL, MME ou REN ANEEL 1.000/2021) e data de verificação.

**Decisão:** a base não traz valores em reais, como "R$ 810,50". Ela fala em "meio salário mínimo por pessoa", porque o salário mínimo muda todo ano e o valor em reais ficaria desatualizado. Também avisa que as faixas antigas de 65%, 40% e 10% deixaram de valer em 5/7/2025.

## Regra de pontuação

A pergunta, as palavras-chave e o título são normalizados antes da comparação: tudo em minúsculas, sem acentos e sem pontuação. Também colocamos espaços nas pontas do texto, para comparar só palavras inteiras.

|                                Regra                             | Pontos |
|------------------------------------------------------------------|--------|
| Palavra-chave da orientação que aparece na pergunta              |   +3   |
| Palavra da pergunta, com 4 letras ou mais, que aparece no título |   +1   |

| Pontuação da melhor orientação |                                Resultado                                    |
|--------------------------------|-----------------------------------------------------------------------------|
|           6 ou mais            | Confiança **ALTA**                                                          |
|            3 a 5               | Confiança **MÉDIA**                                                         |
|          Menos de 3            | "Não encontrei": o assistente sugere outras palavras e mostra as categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, da maior para a menor pontuação. O assistente mostra a melhor orientação. Se ela não resolver a dúvida, mostra até duas alternativas com 3 pontos ou mais.

**Exemplo:** "Tenho direito à tarifa social?"
- +3 por `tarifa social`
- +3 por `tenho direito`
- +1 por "tarifa", +1 por "social" e +1 por "direito", que aparecem no título "Tarifa Social de Energia: quem tem direito"
- Total: **9 pontos, confiança ALTA**

## Proteção de dados e entradas inválidas

- O assistente nunca pede nome, CPF, telefone ou e-mail.
- Pergunta com 8 ou mais dígitos, ou com `@`, é recusada e não fica registrada.
- Opção fora da faixa, letras, resposta vazia ou s/n inválido mostram uma mensagem e pedem a entrada de novo. O programa nunca é encerrado por isso.
- Se o JSON estiver ausente ou corrompido, o programa avisa e encerra sem travar.

## Integrações com outras disciplinas

_(preencher se houver)_ Exemplo: o módulo `energia.py`, de Soluções em Energias Renováveis, fica ligado ao menu pela opção "Orientações de energia" (`assistente.adicionar_opcao`).

## Fontes consultadas

Todas as fontes foram verificadas em 12/11/2026.

- ANEEL – Tarifa Social: https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social
- ANEEL – Como resolver: principais dúvidas: https://www.gov.br/aneel/pt-br/consumidores/como-resolver
- ANEEL – Resolução Normativa nº 1.000/2021 (arts. 343, 344, 346, 357, 359, 361 e 441): https://www2.aneel.gov.br/cedoc/ren20211000.html
- ANEEL – Conheça a Resolução 1.000: https://www.gov.br/aneel/pt-br/assuntos/noticias/2022/conheca-a-resolucao-1-000-que-reune-os-direitos-e-deveres-do-consumidor-de-energia-eletrica
- ANEEL – Cadastro automático na Tarifa Social: https://www.gov.br/aneel/pt-br/assuntos/noticias/2022/governo-federal-aprova-novo-modo-de-cadastro-na-tarifa-social
- MME – Programa Luz do Povo (Tarifa Social e Desconto Social): https://www.gov.br/mme/pt-br/luzdopovo
- MME – Tarifa social: saiba como funciona: https://www.gov.br/mme/pt-br/assuntos/noticias/tarifa-social-saiba-como-funciona-e-quem-pode-pedir-desconto
- Lei nº 15.235/2025 (gratuidade até 80 kWh e Desconto Social) e Lei nº 14.015/2020 (proibição de corte em sexta-feira, fim de semana e feriado)

## Resultado do teste com usuários

_(preencher depois do teste: pelo menos 3 pessoas de fora da equipe e 10 atendimentos; sem nomes nem dados dessas pessoas)_

- Pessoas testadas: __
- Atendimentos: __
- Resposta encontrada: __ %
- Taxa de acerto (ajudou): __ %
- Tempo médio para encontrar: __ s
- Tentativas por atendimento: __
- Facilidade de uso (1 a 5): __
- Dúvidas sem solução: __
- **Melhoria feita a partir do teste:** __ (exemplo: incluímos a palavra-chave "desligada" na orientação de religação, porque um usuário perguntou "minha luz foi desligada" e o assistente não encontrou)

## Limitações

- **A busca é por palavras, não por significado.** O assistente só encontra a resposta se a pergunta tiver uma palavra-chave ou uma palavra do título. Sinônimos não cadastrados, como "desligaram" em vez de "cortaram", não são reconhecidos.
- **O filtro de dado pessoal pode bloquear perguntas legítimas.** Uma pergunta como "consumo de 220 kWh em 10/2026" soma 9 dígitos e é recusada, mesmo sem ter dado pessoal.
- **As regras mudam.** A base reflete as regras vigentes em 12/11/2026. Mudanças na lei ou nas resoluções da ANEEL exigem atualizar o JSON.
- **O assistente não consulta a conta real.** Ele não calcula o valor de uma fatura nem informa se a família já recebe o desconto. Isso só a distribuidora pode fazer.
- **Não é canal oficial.** O assistente informa e encaminha, mas não resolve o problema no lugar da distribuidora ou do CRAS.

## Vídeo técnico

Link (YouTube, não listado): _(preencher)_