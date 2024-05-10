# chatbot/bot.py
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms.ctransformers import CTransformers
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_pinecone import Pinecone
import os
# Set up embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Connect to Pinecone
os.environ['PINECONE_API_KEY'] = "API-KEY"
index_name = "rs-chatbot"
vector_database_index = Pinecone.from_existing_index(index_name, embeddings)

def get_similiar_docs(query,k=1,score=False):
  if score:
    similar_docs = vector_database_index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = vector_database_index.similarity_search(query,k=k)
  return similar_docs

def get_bot_response(query):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    # Load and initialize model from the local path
    llm = CTransformers(model="chatbot/Model/llama-2-7B.bin",
                    model_type="llama",
                    config={'max_new_tokens':512,
                            'temperature':0.8})
    
    # Load question-answering chain
    chain = load_qa_chain(llm, chain_type="stuff")
    
    # Perform similarity search
    similar_doc = get_similiar_docs(query)

    # Get bot response
    bot_response = chain.run(input_documents=similar_doc, question=query)
    
    if "Unhelpful Answer:" in bot_response:
        bot_response = bot_response.split("Unhelpful Answer:")[0]
    if "Incorrect Answer:" in bot_response:
        bot_response = bot_response.split("Incorrect Answer:")[0]
    if "Lacking Knowledge:" in bot_response:
        bot_response = bot_response.split("Lacking Knowledge:")[0]
    if "Please answer the question below using only the context provided:" in bot_response:
        bot_response = bot_response.split("Please answer the question below using only the context provided:")[0]
    if "Helpful Hint:" in bot_response:
        bot_response = bot_response.split("Helpful Hint:")[0]
    if "Based on your search history," in bot_response:
        bot_response = bot_response.split("Based on your search history,")[0]
    if "Can you please tell me more about your preferences?" in bot_response:
        bot_response = bot_response.split("Can you please tell me more about your preferences?")[0]
    if "Are you looking for a specific brand or price range?" in bot_response:
        bot_response = bot_response.split("Are you looking for a specific brand or price range?")[0]
    if "I'm glad you're looking to find the best product! However, I cannot suggest or endorse any specific product without knowing more about your preferences and requirements. Could you please provide me with some details such as your budget, preferred brand, and what features are most important to you? That way, I can give you a personalized recommendation that meets your needs." in bot_response:
        bot_response = bot_response.split("I'm glad you're looking to find the best product! However, I cannot suggest or endorse any specific product without knowing more about your preferences and requirements. Could you please provide me with some details such as your budget, preferred brand, and what features are most important to you? That way, I can give you a personalized recommendation that meets your needs.")[0]

    return bot_response

