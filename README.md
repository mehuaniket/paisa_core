# Paisa Core - 5Paisa API client (Python SDK)
(still under development) <br/>
Python library for 5paisa trading APIs.

## Installation

- Clone the repository. (Only supports python3)

```python
git clone https://github.com/kodani/paisa_core.git
cd paisa_core
pip setup.py install
```

## Usage

- Create new directory and copy `main.py`.
- Create env file.

```bash
mv .env.template .env
chmod +x .env 
```

- Provide all the variables from app credentials you have and user authentication detail. You can execute `.env` with 
following command.

```bash 
./.env
```

- Run main.py. 
```bash
python main.py
```