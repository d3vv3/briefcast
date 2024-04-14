from fastapi import FastAPI, UploadFile
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_text_splitters import CharacterTextSplitter

app = FastAPI()
llm = OpenAI(temperature=0.3, model="gpt-3.5-turbo-instruct")

prompt = PromptTemplate.from_template(
    """**Input**: A transcript file with timestamps (format: [start_time -> end_time] text)
**Task**: Filter out lines that are not relevant to the main topic of the podcast transcription, condensing the transcript to focus on the primary discussion.
**Objective**: Reduce the overall time of the transcription by removing:
    - Off-topic conversations
    - Unrelated tangents
    - Intro/outro segments (e.g., opening credits, closing remarks)
    - Unnecessary filler words (e.g., "um," "ah")
    - Any other non-essential content
**Output**: A condensed transcript file with timestamps (format: [start_time -> end_time] text), containing only the relevant lines that align with the main topic of the podcast.
**Example Input**:
```
[1,00s -> 3,00s] Hello and welcome to our podcast!
[4,00s -> 6,00s] Today we're discussing the impact of AI on society.
[7,00s -> 10,00s] Um, can you hear me okay?
[11,00s -> 15,00s] Absolutely, let's dive into the topic.
```

**Example Output**:
```
[4,00s -> 6,00s] Today we're discussing the impact of AI on society.
[11,00s -> 15,00s] Absolutely, let's dive into the topic.
```

**Note**: The output transcript should maintain the original timestamp format and only include the relevant lines that align with the main topic.
**Important**: Only output the condensed transcript file, without any additional text or explanations. The output should consist solely of the relevant lines with timestamps, formatted as shown above.

Input transcription file:
```
{transcription}
```

Output:
"""
)

# The prompt is the same for both the map and reduce chains
map_chain = LLMChain(llm=llm, prompt=prompt)
reduce_chain = LLMChain(llm=llm, prompt=prompt)

combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="transcription"
)

# For each transcription chunk, highlight the relevant parts
# (smaller transcription)
reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
    token_max=3000,
)

# Combine the smaller transcriptions into a single document and reduce them
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="transcription",
    return_intermediate_steps=True,
)
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n", chunk_size=2000, chunk_overlap=0
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/trim")
def trim(transcription_file: UploadFile):
    transcription_text = transcription_file.file.read().decode("utf-8")
    split_transcription = text_splitter.create_documents([transcription_text])
    response = map_reduce_chain.invoke(split_transcription)
    return {"trimmed_transcription": response["output_text"].replace("```\n", "")}
