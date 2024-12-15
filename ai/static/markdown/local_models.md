# Local models used from hugging face

The following sections provide an overview of code snippets for working with different platforms and their language models using the `transformers` library.

## Alibaba
This section demonstrates the use of the `AutoTokenizer` and `AutoModelForCausalLM` classes from the `transformers` library. It includes:
- Specifying a model name.
- Loading the tokenizer and model.

## Meta
This section also uses the `AutoTokenizer` and `AutoModelForCausalLM` classes and includes:
- Setting the number of CPU threads when running on a CPU.
- Specifying a different model name to load.

## OpenAI
This section demonstrates:
- Loading the pre-trained GPT-2 model and tokenizer.
- Adjusting the number of CPU threads when running on a CPU.

## Google
This section provides instructions for:
- Directly loading a BERT model and tokenizer.
- Moving the model to a GPU if one is available.

## Custom Models
This section explains:
- Loading a fine-tuned GPT-2 model and tokenizer.
- Configuring the use of additional CPU threads as needed.

---

Overall, the sections highlight code snippets for working with various large language models and tokenizers, primarily leveraging the `transformers` library.
