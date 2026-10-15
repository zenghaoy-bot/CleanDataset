from system_graph import construct_graph
from my_llm import llm_langchain
from pydantic import BaseModel, Field
import pandas as pd
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from playwright.sync_api import sync_playwright


class Triple(BaseModel):
    head: str = Field(description="head entity must be organization / institution / system name")
    relation: str = Field(description="relation between entities, concise verb phrase")
    tail: str = Field(description="tail entity must be organization / institution / system name")

class TripleList(BaseModel):
    triples: List[Triple] = Field(description="all triple relationships extracted from the article")

def fetch_web_text(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
            page.goto(url, timeout=45000)
            page.wait_for_load_state("networkidle")
            content = page.locator("body").inner_text()
            browser.close()
        return content
    except Exception as e:
        print(f"Grab failed for {url}: {e}")
        return ""


prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
You are an expert in knowledge extraction.
Read the full article on cybersecurity breach incidents and extract third-party entity triple relationships in the format (head, relation, tail).

Rules:
1. Prioritize extracting organizations, companies and institutions as head and tail entities. Use the provided victim name as head for security‑incident‑related triples.
2. Extract organizational relationships, including only business cooperation, project partnership, collaboration, client‑vendor and more.
3. Use concise verb phrases for relations; avoid long sentences. Relation should reflect factual interaction described in original text.
4. Ignore advertisements, navigation elements and irrelevant web‑page noise content.
5. Do NOT fabricate non‑existent relationships; return an empty list if no relationships exist in the original text.
6. Remove triples where head and tail are identical; do not generate self‑referential triples.
7. If the article mentions third‑party companies that the victim has worked with, collaborated with, or done projects with, explicitly generate triples for those business connections.

Example:
Text snippet: "Bird Construction has worked on multiple projects with Suncor Energy."
Output triple example:
["Bird Construction", "business cooperation", "Suncor Energy"]

Output strictly follow the specified JSON list‑of‑lists structure.
"""),
    ("human", "Article content\n{content}, Victim：{victim}"),
])

structured_llm = llm_langchain.with_structured_output(TripleList)
chain = prompt | structured_llm


df = pd.read_csv("filtered_sources.csv")
subset_df = df[["victim","sources"]]
records = subset_df.to_records(index=False).tolist()
print("length of urls:", len(subset_df))
entity_relations = []


for idx, record in enumerate(records[:10]):
    print("Index:", idx, "Record:", record)
    victim, url = record
    page_text = fetch_web_text(url)
    if not page_text or len(page_text) < 100:
        print("Page content too short, skipping URL")
        continue

    doc_content = page_text[:12000]
    print("lnegth of doc_content:", len(doc_content))

    try:
        print(f"Processing record {idx + 1}/{len(records)}: Victim: {victim}")
        result: TripleList = chain.invoke({"content": doc_content,"victim":victim})
        print("done")
        for t in result.triples:
            triple_item = (t.head.strip(), t.relation.strip(), t.tail.strip())
            entity_relations.append(triple_item)
            print(f"Triple: {triple_item}")
    except Exception as err:
        print(f"LLM parsing error：{err}")
print("entity_relations:", entity_relations)

    
# get graph
construct_graph(entity_relations)
