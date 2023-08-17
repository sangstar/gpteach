# GPTeach: Create Q&A's for any topic for studying or data generation

Aims to create Q&A's for a topic of your choice using the Wikipedia API and GPT, that can be used for study guides or for data to fine-tune an autoregressive model. Uses Wikipedia articles as a resource to prevent inaccuracies/hallucinations. 

## Quickstart
An example implementation is below. 

You can start by loading the `ChunkGenerator` object, which gets Wikipedia article text and splices it into sections.

```
from gpteach.data_preparation import ChunkGenerator
from gpteach.generation import QAGenerator
from secret import api_key # Wherever you get your API key from

chunk_generator = ChunkGenerator()
sections = chunk_generator.get_data_from_wikipedia('George Washington')
```
If you want larger or smaller sections from which to generate QAs, you can change the `num_chunks` in `QAGenerator`, which is the number of slices used to create prompts. By default it is 25. 

If you want to instead separate slices by a separator rather than into even chunks, you can specify that you want to use a separator and state which separator you want to use. By default, the Wikipedia separator is `'[edit]'`, but you can set it to whatever you want. 

```
chunk_generator_using_separator = ChunkGenerator(use_separator = True, separator = 'foo')
```

From there, you can generate QAs with the `QAGenerator`. 

```
QA = QAGenerator(api_key = api_key, model_id = 'gpt-3.5-turbo')
QAs = QA.qas_from_sections(sections)
```

If you want to get an idea of how much the QAs will cost you, you can get an estimation of it using a few prompts, by taking the mean and standard error of the costs of those QAs. Obviously, the more you test, the lower the uncertainty. 

```
QA.estimate_cost(sections, num_to_test = 10)
```

You can also use a custom prompt if you want using `prompt_generator` method of `QAGenerator`.

```
QA.prompt_generator = lambda x: f"""Write a QA based on the following text: {x}"""
QA.qas_from_sections(sections[:2])
```

