# Grupo 4 - TO-DO-LIST (Stellar Projects)

**Projeto Final da Disciplina de Programação Web I**

---

### **Grupo 4**
* Guilherme Alves
* Guilherme Monteiro
* Paulo Cosmo

### **Professor**
* Reginaldo

---

### **1. Sobre o Projeto**

O TO-DO-LIST é um sistema web completo para gestão de projetos pessoais, utilizando um quadro Kanban interativo. A aplicação foi desenvolvida para ser uma ferramenta robusta e com uma experiência de utilizador moderna, permitindo que cada pessoa se cadastre, faça login e gira os seus próprios projetos e tarefas de forma privada e organizada.

O projeto cumpre e supera os requisitos propostos, implementando não apenas o CRUD completo de duas entidades (`Projetos` e `Tarefas`), mas também funcionalidades avançadas para criar uma aplicação rica e profissional.

**Links do Projeto:**
* **Sistema Online:** [https://guilhermealves05.github.io/projeto_final_grupo4/](https://guilhermealves05.github.io/projeto_final_grupo4/)
* **API Online:** [https://api-kanban-grupo4.onrender.com/](https://api-kanban-grupo4.onrender.com/)

### **2. Funcionalidades Principais**

* **Autenticação de Utilizadores:** Sistema de login seguro para garantir a privacidade dos dados de cada utilizador.
* **Gestão de Projetos:** Criação, renomeação e exclusão de múltiplos projetos por utilizador.
* **Quadro Kanban Interativo:** Organize tarefas em colunas ("A Fazer", "Em Andamento", "Concluído") com funcionalidade de arrastar e soltar (drag-and-drop).
* **Gerenciamento de Tarefas:** Crie, edite e exclua tarefas através de um modal de detalhes.
* **Prazos (Due Dates):** Defina datas de entrega para as tarefas, com destaque visual para as que estão atrasadas.
* **Dashboard de Progresso:** Acompanhe o percentual de conclusão de cada projeto em tempo real.
* **Modo Escuro (Dark Mode):** Tema alternativo para melhor conforto visual, com a preferência salva no navegador.
* **Feedback Visual:** Notificações "toast" para ações e animação de confetes ao concluir tarefas.
* **Design Responsivo:** A interface adapta-se a diferentes tamanhos de ecrã.

### **3. Tecnologias Utilizadas**

* **Back-end:** API RESTful desenvolvida em **Python** com o micro-framework **Flask**.
* **Front-end:** Interface dinâmica construída com **HTML5**, **JavaScript** puro (ES6+) e estilizada com **Tailwind CSS**.
* **Hospedagem:**
    * O Front-end está hospedado no **GitHub Pages**.
    * A API do Back-end está hospedada como um Web Service no **Render.com**.
* **Versionamento:** O código é gerido com **Git** e hospedado no **GitHub**.

### **4. Como Executar Localmente**

**Pré-requisitos:**
* Python 3.x
* Navegador moderno

**Back-end:**
```bash
# 1. Navegue até a pasta raiz do projeto

# 2. Crie e ative um ambiente virtual
python -m venv venv
.\\venv\\Scripts\\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a API
python api.py

