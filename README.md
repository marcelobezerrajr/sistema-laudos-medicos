<div align="center">
    <img src="./assets/logo_marcelo_developer.png" height="70" style="margin-bottom: 20px; margin-top: 20px;">
    <h1 align="center">Sistema de Laudos Médicos - Backend 🩺🏥</h1>
</div>

### Sobre o Projeto

Este é um sistema backend projetado para gerenciar laudos médicos, permitindo o controle eficiente de Exames eLlaudos, entre seus Médicos e Pacientes por meio de funcionalidades de CRUD (Create, Read, Update, Delete). Inclui o cadastro e a gestão de Usuários, Médicos, Pacientes, Exames, Laudos, Imagens dos Exames e Imagens dos Laudos. Ideal para clínicas que buscam uma solução integrada para otimizar processos e acompanhar os Exames e Laudos de seus pacientes.


## Funcionalidades Principais

- **Gerenciamento de Usuários:** Registre, atualize, liste e exclua usuários com tipos definidos como médico ou paciente.
- **Gestão de Pacientes e Médicos:** Cada tipo de usuário é registrado e tratado adequadamente no sistema, seja ele médico ou paciente.
- **Envio e Consulta de Exames:** Pacientes podem enviar exames, que ficam disponíveis para médicos visualizarem.
- **Criação de Laudos:** Médicos podem criar laudos baseados nos exames enviados e encaminhá-los para os pacientes.

### 1. Gerenciamento

### Usuários

- **Criar Usuário:** Cadastro de novos usuários com tipo definido como "médico" ou "paciente".

- **Atualizar Usuário:** Editar dados de usuários existentes.

- **Listar Usuários:** Exibir a lista de todos os usuários.

- **Visualizar Usuário:** Consultar detalhes de um usuário específico.

- **Deletar Usuário:** Remover um usuário do sistema.

### Pacientes

- **Envio de Exames:** Pacientes podem enviar exames para que médicos visualizem.

- **Consulta de Laudos:** Pacientes podem acessar laudos criados por médicos baseados nos exames enviados.

### Médicos

- **Consulta de Exames:** Médicos podem visualizar exames enviados pelos pacientes.

- **Criação de Laudos:** Médicos podem criar laudos baseados nos exames recebidos.

- **Envio de Laudos:** Laudos são encaminhados para os pacientes.

### 2. Permissões de Usuário

- **get_medico:** 
  - Acesso permitido apenas para médicos.
- **get_paciente:**
  - Acesso permitido apenas para pacientes.
- **get_medico_paciente:** 
  - Acesso permitido apenas para médicos e pacientes.

## Stacks utilizadas

**Back-end:** FastApi

**SQL:** Sqlite

## Documentação da API - CRUD

As chamadas para a API seguem um padrão para as entidades **Usuário, Médicos, Pacientes, Exames e Laudos** no sistema. Para utilizar os recursos, substitua o caminho e o identificador da entidade conforme necessário. Abaixo estão exemplos utilizando a entidade **Médico**.

### Listar todos os Médicos

Retorna uma lista de todos os Médicos cadastrados.

```http
  GET /medico/list
```

| Parâmetro   | Tipo       | Descrição                           | 
| :---------- | :--------- | :---------------------------------- |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/medico/list?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "especialidade": "Dermatologista",
  "crm": "395459",
  "id_medico": 1,
  "usuario": {
    "nome": "Marcelo",
    "email": "marcelo@gmail.com",
    "tipo": "medico",
    "data_criacao": "2025-01-21T20:05:14.815000",
    "id_usuario": 1
  }
}
```

### Obter Médico por ID

Retorna os detalhes de um Médico específico.

```http
  GET /medico/view/{id_medico}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_medico` | `int` | **Obrigatório**. ID do Médico que deseja consultar. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que vai consultar. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/medico/view/1?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "especialidade": "Dermatologista",
  "crm": "395459",
  "id_medico": 1,
  "usuario": {
    "nome": "Marcelo",
    "email": "marcelo@gmail.com",
    "tipo": "medico",
    "data_criacao": "2025-01-21T20:05:14.815000",
    "id_usuario": 1
  }
}
```

### Criar um Novo Médico

Adiciona um novo Médico ao sistema.

```http
  POST /medico/create
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `especialidade` | `string` | **Obrigatório**. Especialidade do Médico. |
| `crm` | `string` | **Obrigatório**. CRM do Médico. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que vai ser adicionado como médico. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que fazer a requisição para criar um novo médico. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/medico/create?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "especialidade": "Dermatologista",
  "crm": "395459",
  "id_medico": 1,
  "usuario": {
    "nome": "Marcelo",
    "email": "marcelo@gmail.com",
    "tipo": "medico",
    "data_criacao": "2025-01-21T20:05:14.815000",
    "id_usuario": 1
  }
}
```

### Atualiza um Médico
Atualiza as informações de um Médico existente.

```http
  PUT /medico/update/{id_medico}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `especialidade` | `string` | **Opcional**. Especialidade do Médico. |
| `id_medico` | `int` | **Obrigatório**. ID do Médico que deseja atualizar. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que fazer a requisição para atualizar o médico. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/medico/update/1?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "especialidade": "Pediatra",
  "crm": "395459",
  "id_medico": 1,
  "usuario": {
    "nome": "Marcelo",
    "email": "marcelo@gmail.com",
    "tipo": "medico",
    "data_criacao": "2025-01-21T20:05:14.815000",
    "id_usuario": 1
  }
}
```

### Deletar um Médico

Remover um Médico do sistema.

```http
  DELETE /medico/delete/{id_medico}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_medico` | `int` | **Obrigatório**. ID do Médico que deseja deletar. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que fazer a requisição para deletar o médico. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/medico/delete/3?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "message": "Médico com ID 3 deletado com sucesso."
}
```

### Padrão API para envio das imagens

As chamadas da API para envio de imagens seguem um padrão para as entidades **Imagem Exame e Imagem Laudo** no sistema. Para utilizar os recursos, substitua o caminho e o identificador da entidade conforme necessário. Abaixo estão exemplos utilizando a entidade **Exame Laudo**.

### Listar as imagens de um Laudo

Retorna uma lista com todas as imagens de um Laudo.

```http
  GET /images-laudo/list/{id_laudo}
```

| Parâmetro   | Tipo       | Descrição                           | 
| :---------- | :--------- | :---------------------------------- |
| `id_laudo` | `int` | **Obrigatório**. ID do Laudo que vai ser consultado. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que vai fazer a requisição. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/imagens-laudo/list/1?id_usuario=1
```

#### Exemplo de Resposta

```json
[
  {
    "id_laudo": 1,
    "descricao": "Laudo Medico",
    "id_imagem": 1,
    "caminho_arquivo": "Laudos-Medicos/uploads/laudos/laudo_1_images (1).jpeg"
  }
]
```

### Obter Imagem de Laudo por ID

Retorna a imagem de um Laudo específico.

```http
  GET /imagens-laudo/{id_imagem}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_imagem` | `int` | **Obrigatório**. ID da Imagem que deseja consultar. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que vai fazer a consulta. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/imagens-laudo/1?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "id_laudo": 1,
  "descricao": "Laudo Medico",
  "id_imagem": 1,
  "caminho_arquivo": "Laudos-Medicos/uploads/laudos/laudo_1_images (1).jpeg"
}
```

### Adicionar uma nova imagem de um Laudo

Adiciona uma imagem nova a um Laudo.

```http
  POST /imagens-laudo/upload
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_laudo` | `string` | **Obrigatório**. ID do Laudo que vai ser adicionado a imagem. |
| `descricao` | `string` | **Obrigatório**. Descrição do Laudo que está sendo enviado. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que fazer a requisição para adicionar uma nova imagem ao Laudo. |
| `file` | `string` | **Obrigatório**. Arquivo de imagem que vai ser adicionado. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/imagens-laudo/upload?id_laudo=1&descricao=imagemlaudo&id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "id_laudo": 1,
  "descricao": "imagemlaudo",
  "id_imagem": 2,
  "caminho_arquivo": "Laudos-Medicos/uploads/laudos/laudo_1_logo_marcelo_developer.png"
}
```

### Deletar uma imagem de algum Laudo

Deleta a imagem de um Laudo.

```http
  DELETE /imagens-laudo/delete/{id_imagem}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id_imagem` | `int` | **Obrigatório**. ID da Imagem que deseja deletar. |
| `id_usuario` | `int` | **Obrigatório**. ID do Usuário que fazer a requisição para deletar a imagem do Laudo. |

#### Exemplo de Requisição

```http
  http://127.0.0.1:8000/imagens-laudo/delete/2?id_usuario=1
```

#### Exemplo de Resposta

```json
{
  "detail": "Imagem de laudo deletada com sucesso."
}
```
## Guia de Instalação do Projeto (Backend: FastAPI)

### Pré-requisitos

- Python 3.8+
- Gerenciador de Pacotes:
    - Pip para Python

### 1. Configuração do Backend (FastAPI)

#### Passo 1: Acesse o diretório do backend

```bash
  cd backend
```

#### Passo 2: Crie um ambiente virtual (opcional, mas recomendado)

```bash
  python -m venv venv
  source venv/bin/activate     # Linux/MacOS
  # ou
  venv\Scripts\activate        # Windows

```

#### Passo 3: Instale as dependências

Certifique-se de que o arquivo `requirements.txt` está na pasta `backend`.

```bash
  pip install -r requirements.txt
```

#### Passo 4: Inicie o servidor FastAPI

Inicie com o código bash abaixou ou iniciando o arquivo `run.py`, que está no `backend`.

```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
O backend estará disponível em: http://localhost:8000.

## Licença

[MIT](https://github.com/marcelobezerrajr/sistema-laudos-medicos/blob/main/LICENSE)