# Relatório teórico — TechFlow Solutions

## 1. Descrição do projeto e escopo inicial
O TechFlow Solutions é um sistema web de gerenciamento de tarefas para uma startup de logística. Seu propósito é acompanhar o fluxo de trabalho, organizar atividades e dar visibilidade às entregas. O escopo inicial contempla operações de cadastro, consulta, edição e exclusão de tarefas, com título, descrição, responsável e status em um quadro Kanban.

## 2. Metodologia ágil utilizada
Foi escolhido o Kanban por sua gestão visual e fluxo contínuo. As tarefas são distribuídas em A Fazer, Em Progresso e Concluído. O quadro permite identificar acúmulo de trabalho e facilita a priorização. No GitHub Projects, as colunas correspondentes são To Do, In Progress e Done.

## 3. Importância da modelagem na Engenharia de Software
A modelagem permite compreender o problema antes da implementação, identificar atores, responsabilidades, dados e relacionamentos. Ela reduz ambiguidades, apoia a comunicação entre equipe e cliente e serve como referência para desenvolvimento, testes e manutenção. Os diagramas UML representam as funcionalidades esperadas e a estrutura conceitual do sistema.

## 4. Diagrama de Casos de Uso
O diagrama identifica Operador e Gestor como atores. O operador cadastra, consulta, edita e movimenta tarefas. O gestor acompanha o quadro, define prioridades, pesquisa, filtra e pode editar ou excluir tarefas. O arquivo-fonte Mermaid está em `uml/casos-de-uso.mmd`.

## 5. Diagrama de Classes
O modelo apresenta Tarefa como entidade principal, QuadroKanban como responsável pela organização e filtragem, e BancoDados como componente de persistência. O quadro organiza várias tarefas e o banco persiste os registros. O arquivo-fonte Mermaid está em `uml/diagrama-de-classes.mmd`.

## 6. Mudança de escopo
Após a definição do CRUD, foi simulada uma necessidade adicional: destacar tarefas urgentes e localizar atividades com rapidez. O escopo foi ampliado com níveis de prioridade, busca, filtro e indicador de tarefas críticas. A mudança foi justificada pelo impacto de atrasos nas operações logísticas e deve ser registrada como cards no GitHub Projects.

## 7. Testes automatizados
Foi utilizado Pytest. Os testes verificam carregamento da página inicial, cadastro de tarefa, obrigatoriedade do título, atualização, movimentação entre etapas, exclusão e rejeição de prioridade inválida. O workflow do GitHub Actions instala as dependências e executa `pytest -v` em push e pull request. Assim, erros são detectados de forma repetível durante a integração.

## 8. Evidências do GitHub
Inserir nesta seção capturas reais, acompanhadas de legenda:
- **Figura 1 — GitHub Projects:** quadro com os cards distribuídos em To Do, In Progress e Done.
- **Figura 2 — Commits:** histórico mostrando pelo menos dez commits descritivos.
- **Figura 3 — GitHub Actions:** execução do workflow com os testes aprovados.

As capturas devem ser adicionadas pelo estudante após publicar e executar o projeto no próprio GitHub.

## 9. Considerações finais
O projeto demonstra como práticas ágeis, modelagem, versionamento e testes automatizados podem trabalhar em conjunto. O Kanban melhora a transparência do fluxo, enquanto o pipeline de integração contínua oferece feedback rápido sobre a qualidade. O registro da mudança de escopo demonstra a importância de adaptar o produto sem perder o controle do planejamento.
