from langchain_community.embeddings import HuggingFaceEmbeddings


def main():
    embedding_model = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        cache_folder="models",
        )

    while True:
        user_input = input("Enter your question: ")
        print(embedding_model.embed_query(user_input))


if __name__ == "__main__":
    main()
