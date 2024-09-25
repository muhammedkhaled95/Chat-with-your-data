from langchain_community.llms import CTransformers
import gc

# Loading the model
# If local = True, we use locally downloaded LLM. (Free)
# If local = False, we use OpenAI's GPT models using an API call. (Paid)
def load_llm(local: bool):
    
    if local:
        # Load the locally downloaded model here
        llm = CTransformers(
            # model="TheBloke/Llama-2-7B-Chat-GGML",
            model="app/LLM/capybarahermes-2.5-mistral-7b.Q3_K_M.gguf",
            model_type="mistral",
            max_new_tokens = 1024,
            temperature = 0.5
        )
        
        return llm

    else:
        # This is using a paid LLM like GPT4o from OpenAI
        return None 
    

# Unloading the LLM
def unload_llm():
    global llm_model  # Assuming llm_model is a global variable

    if llm_model:
        print("Unloading the LLM from memory...")
        del llm_model  # Dereference the LLM object
        gc.collect()  # Force the garbage collector to free up memory
        print("LLM successfully unloaded.")