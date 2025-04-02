
# security
This repository contains the code creating a local serve, to simulate the phishing attacking and its detection.

## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Create an environment and install dependencies

```conda
  conda env create -f env/environment.yml
```

Or only install dependencies
```bash
  pip install -r env/requirements.txt
```

For creating the server:
Run "python initialDB.py" at terminal first to create a initial database bank.db.
```bash
  python initialDB.py
```

Run "python server.py" at terminal to create server, open the web url https://localhost:8080 in a browser for operations. Press CTRL+C to stop the server.

```bash
  python server.py
```

For creating phishing servers and send phishing email. Run "python phishing.py"

```bash
  python phishing.py
```


The phishing_detect file contains dataset file and NLP_phishing_detect.ipynb. The NLP_phishing_detect.ipynb shows a simple case to detect phishing content in emails using machine learning. To change and run it, make sure there are two files in the dataset: Enron.csv and phishing_email.csv from https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset.

