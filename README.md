# GPTeach: Create Q&A's for any topic for studying or data generation

A project I'm working on that will aim to create Q&A's for a topic of your choice using the Wikipedia API and GPT, that can be used for study guides or for data to fine-tune an autoregressive model. Uses Wikipedia articles as a resource to prevent inaccuracies/hallucinations. Work in progress.

## Quickstart
An example implementation is below. 

You can start by loading the `ChunkGenerator` object, which gets wikipedia article text and splices it into sections.

```
from gpteach.data_preparation import ChunkGenerator
from gpteach.generation import QAGenerator
from secret import api_key # Wherever you get your API key from

chunk_generator = ChunkGenerator()
sections = chunk_generator.get_data_from_wikipedia('George Washington')
```

From there, you can generate QAs with the `QAGenerator`. 

```
QA = QAGenerator(api_key = api_key, model_id = 'gpt-3.5-turbo')
QAs = QA.qas_from_sections(sections)
```