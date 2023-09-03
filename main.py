from interprete import Commnads

if __name__ == "__main__":
    while True:
        entrada = input(
            "🧑 \033[31muser \033[0m@ \033[36mHT 2\033[0m:» ").strip()
        Commnads(entrada)
