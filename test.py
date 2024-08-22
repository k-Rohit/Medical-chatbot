# test_import.py
import crew_ai

print("crew_ai package imported successfully!")
# PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# # Initialize the Google Generative AI model
# 

# # Create the LLMChain with the prompt
# llm_chain = LLMChain(llm=llm, prompt=PROMPT)

# # Specify the document variable name for StuffDocumentsChain
# combine_documents_chain = StuffDocumentsChain(
#     llm_chain=llm_chain,
#     document_variable_name="context"
# )

# # Now, create the RetrievalQA chain manually
# qa_chain = RetrievalQA(
#     retriever=retriever,
#     combine_documents_chain=combine_documents_chain,
#     return_source_documents=True
# )

# # Test the chain with a sample input
# user_input = input("What would like to know today?")
# result = qa_chain({"query": user_input})
# print("Response: ", result['result'])
