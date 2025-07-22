from func.lib_structure import save_html_tree


def main():
    target_packages = [
        "langchain",
        "langchain_core",
        "langchain_openai",
        "langchain_cohere",
        "langchain_experimental",
        "langgraph",
        "langsmith",
        "pydantic",
        "ragas",
    ]

    for package_name in target_packages:
        print(f"Processing: {package_name}")
        try:
            filepath = save_html_tree(package_name)
            print(f"✅ Saved: {filepath}")
        except Exception as e:
            print(f"❌ Failed: {package_name} - {e}")


if __name__ == "__main__":
    main()
