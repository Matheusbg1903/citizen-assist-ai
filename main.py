from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("dataa/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível carregar a base de conhecimento.")
        print("Verifique o arquivo data/base_conhecimento.json")
        return
    
    assistente = Assistente("Citizen Assist AI", base) 

    # módulo de energia (descomentar quando existir)
    # import energia
    # assistente.adicionar_opcao("Orientações de energia", energia.menu)
    
    try:
        assistente.executar()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
        
        
if __name__ == "__main__":
    main()