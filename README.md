### GPT-backed Sales Assistant 
 This project aims to create a GPT-backed AI assistant for answering customer sales inquiries.

### Background
The main objective of this project is to effectively distinguish between general and product-specific customer inquiries and provide tailored responses using suitable tools. We utilize a vector store to handle general questions by referencing guidelines and employ a knowledge graph to address specific product-related queries. A customized agent, developed using the LangChain framework, is responsible for selecting the appropriate tool to address each inquiry.

### Prepare a guildline for sales inquries
Prepare your guidelines for the sales process (take a look at examples/guidelines.txt), each guideline has the following format:<br>
```
[sales inquiry from a customer](double quoted)
[Customer's intention behind this inquiry]

[What strategy should be used to answer this inquiry.]

Example Response
[An example response is presented here.](double quoted)
```

### Prepare a knowledge graph by using Neo4j
Before running main.py, visit the official Neo4j website to initiate a free AuraDB instance and configure the connection in your environment.
```
export NEO4J_URL=neo4j+s://{{instance id of your auradb instance}}.databases.neo4j.io
export NEO4J_PASSWORD={the password of your auradb instance}
```

We create a Neo4j model as depicted in the image below.<p>
![Model in Neo4j](../assets/model.png?raw=true)

### Quick Start
Next, we convert the text file containing the guidelines into a JSON file. This JSON file will be loaded into a vector store once the UI is initiated
```
pip install -r requirements.txt

export OPENAI_API_KEY=your_api_key
python src/convert_guidelines.py \
   example/guidelines.txt \
   example/guidelines.json
```
Now let's initiate the chatbot by running main.py.
```
python src/main.py
```

### Example inputs for the chatbot
```
1. The cost of your product seems very high.
2. We don't have any budget left in this year.
3. What are the main features of your product?
4. How many components in your product?
5. What kind of service will be available after purchasing?
```

### Demo Results
For general questions from the customer, the chatbot searches the vector store to retrieve the answer.<p>
![general customer inquiry](../assets/general-inquiry.png?raw=true)<p>
When the customer requests specific product details, the chatbot searches the knowledge graph to provide the answer.<p>
![product-specific customer inquiry](../assets/product-inquiry.png?raw=true)
