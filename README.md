### GPT-backed Sales Assistant 
 This project aims to create a GPT-backed AI assistant for answering customer sales inquiries.

### Background
This project draws inspiration from the [SalesCopilot](https://github.com/e-johnstonn/SalesCopilot) project. Our primary goal is to promptly identify and address potential objections and acceptances in customer inquiries, offering instant guidance for effective responses. To streamline this, we've excluded call recording and transcription components from SalesCopilot, enabling us to enhance the assistant's capabilities for objection and acceptance handling.

### Quick Start
Prepare your guidelines for the sales process (take a look at examples/guidelines.txt), each guideline has the following format:<br>
```
[sales inquiry from a customer](double quoted)
[Customer's intention behind this inquiry]

[What strategy should be used to answer this inquiry.]

Example Response
[An example response is presented here.](double quoted)
```
Next, we convert the text file containing the guidelines into a JSON file. This JSON file will be loaded into a vector store once the UI is initiated
```
pip install -r requirements.txt

export OPENAI_API_KEY=your_api_key
python src/convert_guidelines.py example/guidelines.txt example/guidelines.json
```
Now let's initiate the chatbot by running main.py.
```
python src/main.py example/guidelines.json
```