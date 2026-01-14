from search import search_prompt

def main():    
    # chain = search_prompt()

    # if not chain:
    #     print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
    #     return
    
    print("="*50)
    print("Chat iniciado. Digite 'sair' para encerrar.")
    
    while True:
        print("="*50)
        print(" ")
        pergunta = input("Digite sua pergunta: ")
     
        if pergunta.lower() == "sair":
            print(" ")
            print("Chata encerrado.")
            break
     
        resposta = search_prompt(pergunta)
        
        print(f"Resposta: {resposta}")

if __name__ == "__main__":
    main()