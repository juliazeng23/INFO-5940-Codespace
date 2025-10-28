External Sources

I came across a problem where similarity_search was returning one document multiple times and searching the web led me to the following page where I found the issue:
- https://stackoverflow.com/questions/77555312/langchain-chromadb-why-does-vectorstore-return-so-many-duplicates

I then looked at Chroma documentation to reset the database when the files are changed
- Chroma documentation: https://python.langchain.com/api_reference/community/vectorstores/langchain_community.vectorstores.chroma.Chroma.html#langchain_community.vectorstores.chroma.Chroma.__init__

I looked at Streamlit file_uploader documentation to learn how to accept multiple documents
- Streamlit file_uploader documentation: https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader

AI Usage

I asked ChatGPT to generate a short article on a topic and some questions relating to the article. I used this to test my application. I was able to adjust the article to the level of complexity that I wanted. Additionally, I was able to get questions of different types, e.g. factual, critical thinking, etc.
https://chatgpt.com/s/t_690136547fcc8191b246e313b30aa833
https://chatgpt.com/s/t_6901367a10848191982694c7104fd419

I asked ChatGPT about my similarity_search response duplicate issue, though it did not find the correct source of the problem.
