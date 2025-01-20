import json
import os
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
import openai
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from enum import Enum
from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from tagging_schema_old import ArticleMetadata
from langchain_core.pydantic_v1 import validator
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import pandas as pd
import time
# Load environment variables
load_dotenv()

# Setup the API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class DocumentTagExtractor:
    def __init__(self, documents,output_file, schema=None):
        self.documents = documents
        self.output_file = output_file
        self.output_dir = "data/tagged_documents"
        self.ensure_output_directory()
        self.schema = None
        self.extraxtor = None

    def ensure_output_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def set_schema(self, schema):
        self.schema = schema

    def setup_extraction_chain(self):
        system_prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    "You are a highly detailed and context-aware extraction algorithm. "
                    "Your task is to meticulously analyze research papers on large language models (LLMs) for software engineering tasks, focusing on the titles and abstracts. "
                    "Your primary objectives are to categorize the papers based on their research focus and intended goals. "
                    
                    "For the research_focus field, provide the following structure:\n"
                    "research_focus:\n"
                    "  category: [MUST be exactly one of: 'direct_solution', 'dataset_benchmark', 'llm_property_investigation', 'existing_solution_evaluation', 'other' - all lowercase]\n"
                    "  category_reasoning: [Provide a brief explanation for the chosen category]\n"
                    
                    "The categories are defined as follows:\n"
                    "- DIRECT_SOLUTION: Papers proposing a solution Y for Problem(s) X related to SE-Task(s) X. Artifacts may include new frameworks, concepts, or modifications of existing solutions.\n"
                    "- DATASET_BENCHMARK: Papers creating new Datasets or Benchmarks Y' related to Problem(s) X of SE-Task(s) X for assessing the quality of Solutions Y.\n"
                    "- LLM_PROPERTY_INVESTIGATION: Papers investigating properties of LLMs related to Problem(s) X of SE-Task(s) X, providing new findings about specific LLM attributes.\n"
                    "- EXISTING_SOLUTION_EVALUATION: Papers investigating existing Solution Y's quality for Problem(s) X related to SE-Task(s) X, evaluating performance of existing LLM-based solutions.\n"
                    "- OTHER: Papers that do not clearly fit into the above categories.\n"
                    
                    "If you choose OTHER, provide a matching new category suggestion in the category_reasoning field.\n"
                    
                    
                    "Your analysis should help categorize each paper's research focus accurately, providing a comprehensive understanding of their contributions to the field of software engineering using LLMs."
                ),
                ("human", "{text}"),
            ])
        
        api_key = "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"
        #llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key,temperature=0)gpt-4o
        llm = ChatOpenAI(model="gpt-4o", api_key=api_key,temperature=0)

        runnable = system_prompt | llm.with_structured_output(schema=ArticleMetadata)
        self.extraxtor = runnable

    def extract_metadata(self, document):
        metadata = self.extraxtor.invoke({"text": "Title: "+document['Title']+"\nAbstract: "+document['Abstract']})
        
        #if metadata.directSolution is None and metadata.custom_category:
        #    # If no predefined category was selected, but a custom category was suggested
        #    print("OK HERE IS A CUSTOM CATEGORY!: ",metadata.custom_category)
        #    metadata.directSolution = metadata.custom_category
        
        return metadata
    
    def save_metadata(self, metadata):
        output_path = os.path.join(self.output_dir, self.output_file)

        # Custom JSON encoder to handle Enum types
        class EnumEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Enum):
                    return obj.value
                return super().default(obj)

        # Check if the output file exists
        if os.path.exists(output_path):
            try:
                # Load existing data
                with open(output_path, 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)
            except json.JSONDecodeError:
                print(f"Error reading JSON from {output_path}. Starting with empty list.")
                existing_data = []
        else:
            # If the file does not exist, initialize an empty list
            existing_data = []

        # Convert metadata to dictionary
        metadata_dict = metadata.dict()

        # Manually handle the DirectSolution serialization
        if metadata_dict['research_focus']:
            metadata_dict['research_focus'] = {
                'category': metadata_dict['research_focus']['category'][0].value,
                'category_reasoning': metadata_dict['research_focus']['category_reasoning']
            }

        # Append the new metadata to existing data
        existing_data.append(metadata_dict)

        # Write updated data back to file
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, cls=EnumEncoder, indent=2, ensure_ascii=False)

        print(f"Metadata saved to {output_path}")
    
    def process_documents(self):
        for document in self.documents:
            time.sleep(4)
            print("Document: ",document['Title'])
            metadata = self.extract_metadata(document)
            #print(metadata)
            
            content_data = metadata.dict()
            print("\nContent data: ",content_data)
            #content_data['research_focus'] = content_data['research_focus'].dict()
            #print("\nContent data danach: ",content_data)
            additional_metadata = document
            #print("\nAdditional data: ",additional_metadata)
            
            
            #if 'Title' in additional_metadata:
                # Remove the key-value pair
            #    del additional_metadata['Title']

            # Merge additional_metadata directly into content_data
            content_data.update(additional_metadata)
            #metadata.directSolution
            class DocumentMetadata(BaseModel):
                """Extended model to include additional arbitrary fields from content_guides."""
                Title: str
                Abstract: str
                evaluation: Optional[dict] = Field(default=None)
                research_focus:Optional[dict] = Field(default=None)

            # Now create the DocumentMetadata instance
            extended_document_metadata = DocumentMetadata(**content_data)

            self.save_metadata(extended_document_metadata)
        
    
# Define the file path
file_path = 'data\papers\iltered_papers.json'

# Read the JSON file
with open(file_path, 'r', encoding='utf-8') as file:
    content_guides = json.load(file)

extractor = DocumentTagExtractor(content_guides,output_file="test_4o_16.json")
extractor.set_schema(ArticleMetadata)
extractor.setup_extraction_chain()
extractor.process_documents()

