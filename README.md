# Jupyter Book


## Initial setup for Windows 11
```bash
cd c:/workspace
git clone https://github.com/eat-sleep-code-repeat-it/jupyter-book.git
cd jupyter-book
uv venv
.venv\Scripts\activate

# Install dependencies 
uv sync
# or
uv pip install -r requirements.txt

# install jupyter in the active environment to register the kernel properly.
uv pip install jupyter ipykernel

# Register the Kernel with Jupyter
python -m ipykernel install --user --name=JupyterBook --display-name="Python (JupyterBook)"

uv pip install langchain
```

## How to use


```bash
cd c:/workspace/jupyter-book
.venv\Scripts\activate

# make sure you populated .env file with your API KEYS in the root folder
# CTRL+SHIFT+P to sellect Python Interpreter: jupyter-book
# open book_001.ipynb
# select jupyter kernel: Python (JupyterBook)
```
