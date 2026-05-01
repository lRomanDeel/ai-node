from kernel.pipeline import Pipeline


def main():
    print("🚀 PIPELINE TEST\n")

    pipeline = Pipeline()

    result = pipeline.run({
        "text": "   Ethereum is also growing   "
    })

    print("\n📤 FINAL POST:\n")
    print(result["post"])


if __name__ == "__main__":
    main()