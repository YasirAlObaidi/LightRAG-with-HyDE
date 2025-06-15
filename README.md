1 Introduction
Retrieval- Augmented Generation (RAG) systems are on the rise and are a way to enhance large language models (LLMs) accuracy in answering queries related to specific documents, especially those that the LLMs haven’t been trained on. Multiple methods have been used to context retrieval, but RAG reins supreme in terms of quality of final answers. Of the RAGs available now, the most promising and highest preforming is LightRAG. LightRAG uses a graph-based architecture to find contexts that are semantically similar, as well as keyword matching. This allows for an accurate and robust method of retrieving relevant contexts to the given query. 
As for other methods of retrievals (outside of rag) there is Hypothetical Document Embeddings (HyDE). Although clever in theory, when it comes to evaluation it is beaten by RAGs in every metric, especially LightRAG. HyDE works by prompting an LLM to generate a hypothetical document that answers a query. It then embeds the document as a vector, and does a semantic similarity search with its embedded set of real documents (also stored as vectors) to find which is closest to the hypothetical document. It then retrieves the most similar real document and uses it in a prompt with the original query to provide to the LLM for a final answer. This is extremely different to the approach of LightRAG, which is graph based in its architecture and only uses the query to find key words and to preform semantic similarity searches. 
However, it is possible to combine both approaches into a single architecture that could theoretically outperform LightRAG. We propose incorporating HyDE into the LightRAG architecture to improve the accuracy and semantic quality of LightRAG’s final responses. Although LightRAG is the best available RAG-based retrieval system, it is still not perfect and can be improved. Its responses aren’t always accurate, and it fails to find certain small details in user-inputted datasets. We hypothesize that the incorporation of HyDE logic into the LightRAG architecture could further improve its ability to retrieve relevant contexts from data, and increase the overall quality of final LLM responses to specific queries
The key contributions of this work are:
•	Methodology- By changing the prompts and expected outcomes in LightRAG’s keyword searching function to act in the same logic as HyDE’s, we open the door to testing many different forms of key word retrieval.
•	Results- Our results show that the use of hypothetical documents in the key word generation function of LightRAG to match the logic of HyDE gave worse results in comparison to the standard LightRAG method in nearly every scenario.




2 Methodologies
2.1 What are LightRAG and HyDE?
LightRAG context retrieval (after the creating of the graph) is as follows
1)	Provide a query
2)	Prompt an LLM (gpt-4o-mini in our case) to find the key words in the query. LightRAG asks for 2 types of key words, low-level and high-level. Low-level keywords are for specific entities, details, or concrete terms. High-Level key words are for overarching concepts or themes
3)	Embed the retrieved keywords
4)	Do a keyword search to find nodes that are labelled as the keywords within the graph and then retrieving their closest connected nodes.
5)	Do a semantic search using the earlier created embedding on a vector database using cosine similarity to find semantically similar contexts
6)	Send retrieved contexts and original query to LLM for final response

HyDE context retrieval (after creating embedding index) is as follows
1)	Provide query
2)	Prompt LLM to answer the query in a paragraph
3)	Embed the answer from the LLM
4)	Preform cosine similarity between embedded hypothetical answer and real documents in embedding index
5)	Send retrieved contexts with query to LLM for final response

What we proposed was inserting HyDE logic into the step 2 of the LightRAG process by changing the prompt to not only search for keywords, but to also answer the query and then retrieve the key words from the answer and add them to the lists of key words produced from the query. The answer to the query in this case is the “Hypothetical Document.” The Hypothetical Document was not returned as an output to the LightRAG model, only its keywords. (Returning the hypothetical document for a proper semantic search will be done on the final paper I’m (Yasir) submitting to hopefully be published. We simply didn’t have enough time to do all tests) The original and Modified prompts will be shown at the end in section 6. By doing this, the keyword search and the semantics search done with the embedded key words in steps 4 and 5 will have the keywords of the query as well as more general keywords retrieved from the hypothetical document (that being the answer to the original query given by the LLM.
2.2 Dataset preparation and tests
We used OpenAI’s GPT-4o-mini. We followed the methodology used in the LightRAG paper, and used the same data set ( available at https://huggingface.co/datasets/TommyChien/UltraDomain) for a fair series of tests between our modified models and the original LightRAG model. The dataset was composed of 4 different sections, “mix”, “agriculture”, “legal”, and “cs”. Each dataset had its own graphing done on LightRAG, and so we had 4 base models to work with.  The rest of the methodology of dataset preparation and testing is as follows:
Step0: create contexts from the raw datasets to feed into LightRAG
Step1: feed contexts into LightRAG. Note: Due to the size of the datasets, we created a program that splits each context dataset into files no longer than 30,000 words each so as to not reach the Tokens per minutes limit on the open ai API. We fed one file per minute.
Step2: Generate queries for each dataset fed into LightRAG
Step3: Generate responses to the queries. Note: We repeated this step for every Prompt, within each dataset, and for both hybrid and local mode of LightRAG (local mode only uses low-level key words while hybrid mode uses both high-level and low-level key words)
Step4: compare the results of each modified prompt to the original prompt using the comparison prompt (see 6.4. Prompt includes definitions of parameters used in the results table). This was done for each dataset, prompt, and LightRAG setting combination.
The files in the repository responsible for the main steps have the same name as their step mentioned here. Step 0 is done by file “step_0.py” in the repository. Step 4 is an exception and is called “Eval.py”. The file splitter in Step1 is called “File_Splitter.py”.

3-Results 
Our results showed that the modified prompts produced worse outcomes on nearly all metrics. The tables below compare standard LightRAG to our different models based on dataset. As you can see, the only time our model was better than the standard LightRAG was under local, mod2, legal, diversity. Here are the tables

<img width="485" alt="image" src="https://github.com/user-attachments/assets/91941bda-fe45-4ce8-a7ed-67dc5d486b5d" />


4 Conclusion
We can confidently conclude that using the keywords of a hypothetical document hinder the quality of responses generated by LightRAG. The modified version all did worse in every parameter with varying datasets. As for further research, it could be that using the hypothetical document’s embedding in the semantic similarity search could bring about better results.

5 References
Gao, L., Ma, X., Lin, J., & Callan, J. (2023). Precise Zero-Shot Dense Retrieval without Relevance Labels. Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.acl-long.9
Guo, Z., Xia, L., Yu, Y., Ao, T., & Huang, C. (2024, October 8). LightRAG: Simple and Fast Retrieval-Augmented Generation. arXiv.org. https://arxiv.org/abs/2410.05779






6 Prompts
6.1 Original LightRAG prompt
- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}}
#############################
Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}}
#############################
Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:




6.2 Mod1 Prompt
---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Answer the query yourself, even if you don't have an accurate answer
- Create the keywords from the query AND your answer
- DON'T output your answer to the query, ONLY the keywords FROM your answer
- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
Example 1:

Query: "How does international trade influence global economic stability?"

Your answer: International trade influences global economic stability by promoting economic growth, creating jobs, and enhancing the allocation of resources across countries. It also fosters interdependence among nations, which can lead to greater economic cooperation and stability. However, it can also introduce vulnerabilities, such as trade imbalances, dependency on foreign markets, and susceptibility to global economic shocks.
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact", "economic growth", "economic cooperation", "resource allocation", "interdependence", "global economic shocks"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports", "job creation", "economic vulnerabilities", "foreign markets", "trade imbalances"]
}}
#############################
Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"

Your answer: Deforestation significantly impacts biodiversity by destroying habitats, leading to species extinction and a decline in ecosystem health. It disrupts ecological balance, reduces genetic diversity, and contributes to climate change by increasing greenhouse gas emissions. Deforestation also affects water cycles and soil fertility, further threatening the survival of various plant and animal species. 
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity", "habitat destruction", "ecosystem health", "ecological balance", "climate change"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem", "plant species", "soil fertility", "genetic diversity", "greenhouse gas emissions"]
}}
#############################
Example 3:

Query: "What is the role of education in reducing poverty?"

Your answer: Education plays a crucial role in reducing poverty by providing individuals with the skills and knowledge needed to access better job opportunities, improve productivity, and increase income levels. It also promotes social mobility, enhances health outcomes, and empowers communities to break the cycle of poverty. Additionally, education fosters critical thinking, innovation, and economic development, all of which contribute to long-term poverty reduction.
################
Output:
{{
  "high_level_keywords": ["Education", "reducing poverty", "Socioeconomic development", "critical thinking", "innovation", "economic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality", "poverty cycle", "skills and knowledge", "productivity"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:





















6.3 Mod2 Prompt

---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Create a hypothetical document answering this query that is no more than 60 words
- Create the keywords from the query AND the hypothetical document
- Don't display the hypothetical document to the query, ONLY the keywords FROM the hypothetical document
- Limit the number of keywords to a maximum of 7 for low level-keywords, and a maximum 7 for high-level keywords; You may output less key words
- Output the keywords in JSON format
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
Example 1:

Query: "How does international trade influence global economic stability?"

Your answer: International trade influences global economic stability by promoting economic growth, creating jobs, and enhancing the allocation of resources across countries. It also fosters interdependence among nations, which can lead to greater economic cooperation and stability. However, it can also introduce vulnerabilities, such as trade imbalances, dependency on foreign markets, and susceptibility to global economic shocks.
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact", "interdependence", "global economic shocks"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Imports", "Exports", "job creation"]
}}
#############################
Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"

Your answer: Deforestation significantly impacts biodiversity by destroying habitats, leading to species extinction and a decline in ecosystem health. It disrupts ecological balance, reduces genetic diversity, and contributes to climate change by increasing greenhouse gas emissions. Deforestation also affects water cycles and soil fertility, further threatening the survival of various plant and animal species. 
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity", "climate change", "ecosystem health"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Ecosystem", "plant species", "genetic diversity"]
}}
#############################
Example 3:

Query: "What is the role of education in reducing poverty?"

Your answer: Education plays a crucial role in reducing poverty by providing individuals with the skills and knowledge needed to access better job opportunities, improve productivity, and increase income levels. It also promotes social mobility, enhances health outcomes, and empowers communities to break the cycle of poverty. Additionally, education fosters critical thinking, innovation, and economic development, all of which contribute to long-term poverty reduction.
################
Output:
{{
  "high_level_keywords": ["Education", "reducing poverty", "Socioeconomic development", "critical thinking", "innovation", "economic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality", "poverty cycle", "skills and knowledge", "productivity"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:





















6.4 comparison Prompt
---Role---
You are an expert tasked with evaluating two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.
---Goal---
You will evaluate two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.

- **Comprehensiveness**: How much detail does the answer provide to cover all aspects and details of the question?
- **Diversity**: How varied and rich is the answer in providing different perspectives and insights on the question?
- **Empowerment**: How well does the answer help the reader understand and make informed judgments about the topic?

For each criterion, choose the better answer (either Answer 1 or Answer 2) and explain why. Then, select an overall winner based on these three categories.

Here is the question:
{query}

Here are the two answers:

**Answer 1:**
{answer1}

**Answer 2:**
{answer2}

Evaluate both answers using the three criteria listed above and provide detailed explanations for each criterion.

Output your evaluation in the following JSON format:

{{
    "Comprehensiveness": {{
        "Winner": "[Answer 1 or Answer 2]",
        "Explanation": "[Provide explanation here]"
    }},
    "Empowerment": {{
        "Winner": "[Answer 1 or Answer 2]",
        "Explanation": "[Provide explanation here]"
    }},
    "Overall Winner": {{
        "Winner": "[Answer 1 or Answer 2]",
        "Explanation": "[Summarize why this answer is the overall winner based on the three criteria]"
    }}
}}
![image](https://github.com/user-attachments/assets/e6a5831d-2b6e-4e2c-b186-f9be1353e4f2)
