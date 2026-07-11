# 🚀 Evolv

> **Transformando dados de treino, corrida e alimentação em evolução.**

O **Evolv** é uma aplicação desenvolvida em Python para acompanhar e analisar a evolução física, reunindo em um único sistema informações de **academia 🏋️, corrida 🏃 e alimentação 🍎**.

O projeto surgiu de uma necessidade real: durante minha rotina de treinos, percebi a dificuldade de organizar e acompanhar dados importantes como cargas utilizadas, evolução da corrida, distância percorrida e consumo alimentar. A partir disso, desenvolvi uma ferramenta própria para centralizar essas informações, transformar registros em análises úteis e acompanhar minha evolução ao longo do tempo.

Além de ser uma solução para uso pessoal, o Evolv representa minha aplicação prática dos conhecimentos adquiridos no curso de **Sistemas de Informação**, explorando desenvolvimento de software, banco de dados, arquitetura em camadas e testes automatizados.

---

# 🏋️ Sobre o projeto

O Evolv tem como objetivo ser um sistema completo de acompanhamento fitness, permitindo registrar atividades físicas e informações nutricionais para gerar uma visão mais clara da evolução do usuário.

## Funcionalidades atuais

### 🏋️ Academia

* Cadastro de exercícios;
* Registro de cargas utilizadas;
* Controle de repetições;
* Histórico de treinamento;
* Organização dos dados de treino.

### 🏃 Corrida

* Registro de atividades;
* Controle de distância percorrida;
* Registro de pace;
* Histórico de corridas.

### 🍎 Alimentação

* Banco de alimentos com informações nutricionais;
* Registro de refeições;
* Controle de:

  * 🔥 calorias;
  * 🥩 proteínas;
  * 🍚 carboidratos;
  * 🥑 gorduras.

### 🥣 Medidas e porções

* Cadastro de medidas caseiras personalizadas;
* Conversão entre quantidade em gramas e porções utilizadas no dia a dia.

---

# 🛠️ Tecnologias utilizadas

🐍 **Python**

🗄️ **SQLite**

🧪 **Pytest**

📊 **Pandas**

📄 **OpenPyXL**

🖥️ **CustomTkinter** *(em desenvolvimento)*

📈 **Matplotlib** *(planejado)*

📑 **ReportLab** *(planejado)*

---

# 🏗️ Arquitetura do projeto

O Evolv está sendo desenvolvido utilizando uma arquitetura organizada em camadas:

```text
Evolv
│
├── models
│   └── Entidades e representação dos dados
│
├── dao
│   └── Comunicação com o banco de dados
│
├── services
│   └── Regras de negócio e cálculos
│
├── controllers
│   └── Controle de fluxo da aplicação
│
├── views
│   └── Interface gráfica
│
├── database
│   └── Banco SQLite e importação de dados
│
└── tests
    └── Testes automatizados
```

---

# 🥗 Base nutricional

O módulo de alimentação utiliza a:

**TACO — Tabela Brasileira de Composição de Alimentos**

Os dados nutricionais são importados para o banco local SQLite, permitindo consultas rápidas sem dependência de conexão externa.

Dados armazenados:

* 🔥 Calorias;
* 🥩 Proteínas;
* 🍚 Carboidratos;
* 🥑 Gorduras;
* 📌 Categoria dos alimentos.

---

# 📌 Próximas etapas

## 🖥️ Interface gráfica

* Dashboard principal;
* Navegação entre módulos;
* Interface moderna inspirada em aplicativos fitness.

## 📊 Regras de negócio

* Cálculo de volume de treino;
* Evolução de cargas;
* Recordes pessoais;
* Estatísticas de corrida;
* Análise de consumo alimentar.

## 📈 Dashboard

* Gráficos de evolução;
* Comparação de períodos;
* Indicadores de desempenho.

## 📄 Relatórios

* Resumos de evolução;
* Exportação de dados;
* Histórico de atividades.

---

# 🎯 Objetivos do projeto

O Evolv está sendo desenvolvido para unir aprendizado e aplicação prática:

* Aplicar conceitos de Programação Orientada a Objetos;
* Desenvolver uma aplicação estruturada em camadas;
* Trabalhar com banco de dados relacionais;
* Implementar testes automatizados;
* Criar uma solução real para acompanhamento pessoal.

---

# 👨‍💻 Autor

**Davi Ferreira**

🎓 Bacharelado em Sistemas de Informação

💻 Desenvolvido com Python, aprendizado contínuo e foco em evolução.

---

⭐ *"Pequenas melhorias registradas todos os dias constroem grandes resultados."*
