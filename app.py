import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader


# setting streamlit
st.set_page_config(page_title="DEmo for summarization")
st.title("Summarize it for me")

# groq API
#with st.sidebar:
   # groq_api_key = st.text_input("Groq API Key",value="",type="password")
groq_api_key = "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"
my_url = st.text_input("URL")

llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key )

prompt_template="""
summarize the following content in not more than 400 words:
Content:{text}

"""

prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the Content from YT or Website"):
    ## Validate all the inputs
    if not groq_api_key.strip() or not my_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(my_url):
        st.error("Please enter a valid Url. It can may be a YT video utl or website url")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt video data
                if "youtube.com" in my_url:
                    loader=YoutubeLoader.from_youtube_url(my_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[my_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()

                ## Chain For Summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")
                    

                   