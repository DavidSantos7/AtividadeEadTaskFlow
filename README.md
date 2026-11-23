# TechFlow Solutions — Gestão Ágil de Tarefas

Sistema web simples para uma startup de logística acompanhar tarefas, organizar o fluxo de trabalho, priorizar atividades críticas e visualizar o andamento da equipe.

## Objetivos e escopo inicial
O escopo inicial contempla um quadro Kanban com três etapas (**A Fazer**, **Em Progresso** e **Concluído**) e operações CRUD: criar, consultar, editar e excluir tarefas. Cada tarefa possui título, descrição, prioridade e responsável.

## Metodologia
Foi adotado **Kanban**, por permitir visualizar o fluxo continuamente, limitar a dispersão de trabalho e identificar gargalos. O quadro de acompanhamento no GitHub Projects deve usar as colunas `To Do`, `In Progress` e `Done`, conforme o enunciado. O quadro da aplicação apresenta os nomes em português.

## Funcionalidades
- Cadastro, listagem, edição e exclusão de tarefas.
- Mudança de etapa diretamente no quadro.
- Prioridades Baixa, Média, Alta e Crítica.
- Filtro por prioridade e busca por título, descrição ou responsável.
- Indicadores de tarefas por etapa e total de tarefas críticas.
- Persistência local em SQLite.

## Como executar
Requer Python 3.10 ou superior.

```bash
# 1. Criar e ativar um ambiente virtual (opcional, recomendado)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Iniciar a aplicação
python src/app.py
```
Acesse http://127.0.0.1:5000 no navegador. O banco `techflow.db` será criado automaticamente na primeira execução.

## Testes e qualidade
Execute `pytest -v`. O workflow em `.github/workflows/tests.yml` executa os testes automaticamente em cada push e pull request direcionado às branches `main` ou `master`.

## Estrutura
```text
techflow_solutions/
├── .github/workflows/tests.yml
├── docs/
├── src/app.py
├── tests/test_app.py
├── README.md
├── requirements.txt
└── pytest.ini
```

## Gestão de mudanças — alteração simulada de escopo
**Escopo inicial:** CRUD básico de tarefas com status e responsável.

**Mudança solicitada:** durante a simulação, a startup identificou que entregas urgentes precisavam de destaque e que a coordenação necessitava localizar rapidamente tarefas específicas. O escopo foi ampliado para incluir prioridade (Baixa, Média, Alta e Crítica), busca, filtro e indicador de tarefas críticas.

**Justificativa:** a mudança atende ao risco operacional de atrasos logísticos e melhora a tomada de decisão sem descaracterizar o objetivo principal. Para manter o fluxo controlado, a alteração foi registrada como novos cards no backlog e implementada após as operações essenciais.

## Backlog sugerido para GitHub Projects
Importe ou crie os cards descritos em [`docs/kanban-backlog.csv`](docs/kanban-backlog.csv). Configure as colunas `To Do`, `In Progress` e `Done`. O CSV é uma referência de planejamento; ele não cria automaticamente um GitHub Project.

## Questões norteadoras
1. **Causas de falhas em projetos ágeis e mitigação:** falta de priorização, comunicação deficiente, requisitos pouco claros e ausência de acompanhamento. O Kanban torna o trabalho visível; Issues, Projects, Pull Requests e Actions centralizam decisões, mudanças e validações.
2. **Beneficiados:** equipe operacional, gestores, responsáveis por entregas e clientes. A equipe atualiza tarefas; gestores identificam gargalos e prioridades; clientes se beneficiam de maior previsibilidade.
3. **Qualidade com Actions:** testes executados a cada alteração detectam regressões cedo e dão retorno repetível antes da integração.
4. **Desafios de mudanças:** avaliar impacto, repriorizar o backlog, comunicar envolvidos e testar novamente. A mudança simulada foi documentada e dividida em entregas menores.
5. **Aplicação ágil:** o Kanban organiza o fluxo; reuniões rápidas podem revisar bloqueios e prioridades; a revisão contínua permite adaptar o backlog.

## UML e relatório
Os diagramas de casos de uso e classes estão em `docs/uml/`. O relatório teórico em DOCX está em `docs/relatorio_teorico.docx`. Antes da entrega, complemente o relatório com capturas reais do seu repositório, do quadro Projects e da execução do workflow.

## GitHub: publicação e evidências
1. Crie um repositório **público** no GitHub.
2. Envie os arquivos deste projeto.
3. Crie um GitHub Project e adicione os cards do CSV, organizando-os nas três colunas solicitadas.
4. Faça pelo menos 10 commits reais, pequenos e descritivos. Sugestões de mensagens estão em `docs/commits-sugeridos.md`.
5. Confira a aba **Actions** e capture a execução bem-sucedida.
6. Grave o vídeo pitch de até 4 minutos usando o roteiro em `docs/roteiro-pitch.md`.

> **Importante:** o pacote fornece o código, testes, documentação e workflow. Ele não cria o repositório público, o GitHub Project, os commits da sua conta, as capturas de tela nem publica o vídeo. Essas etapas precisam ser realizadas na sua conta GitHub/YouTube/Drive para que as evidências sejam autênticas.
