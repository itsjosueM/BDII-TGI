# Modelagem-e-Implementacao-Objeto-Relacional-de-um-Sistema-de-Imobiliaria-com-Persistencia-de-Dados

# Como funciona? 

Através do mapeamento objeto-relacional, é possível traduzir o sistema do modelo 
orientado a objetos para o modelo relacional.

Primeiramente, modelamos um diagrama de classes com 5 entidades principais
e restrições das regras de negócio. O diagrama de classes criado pensando 
numa abordagem que incluisse a normalização de de banco de dados, portanto, 
foram criadas tabelas intermediarias em relações N:M.

Após a modelagem, na etapa de construção, criamos o código em python e, logo
em seguida, utilizamos o framework orm SQLalchemy para o mapeamento objeto-relacional

# SUMÁRIO:

1 - Modelagem do sistema de uma imobiliária

2 - Desenvolvimento do código a partir da modelagem e uso do SQLalchemy

3 - Ambiente de virtualização para o sistema

# 1 - Modelagem do sistema de uma imobiliaria

Antes de pôr a mão na massa, primeiro modelamos nosso sistema usando diagrama de classes.
Modelar o sistema. A modelagem em diagrama de classes serviu para visualizar, especificar, 
construir e documentar a estrutura do sistema orientado a objetos, mostrando as classes, seus a
tributos, operações e os relacionamentos entre elas, além de servir como um "padrão" de comunicação
entre a equipe, inteligível para todos.

<img width="2859" height="1299" alt="image" src="https://github.com/user-attachments/assets/4a19320d-ed2d-48c4-b3a2-befd53d3e5f7" />

# 2 - Desenvolvimento do código a partir da modelagem

Criada a representação pictórica do sistema, é hora de construir!

<img width="908" height="684" alt="image" src="https://github.com/user-attachments/assets/c541b29f-caba-4f42-99cf-8d5f54aa0851" />


# 3 - Ambiente de virtualização para o sistena

<img width="1116" height="656" alt="image" src="https://github.com/user-attachments/assets/29445173-26e0-463f-a023-16625a2a7058" />

Um container é criado e, dentro do mesmo, surgem dois serviços: db e app.

O db trata-se do banco de dados utilizado na aplicação, no nosso caso, gerenciado pelo postgres

O serviço 'app' é a lógica de negócio, é o principal módulo do sistena. Ele lê url do banco de dados,
autenticando-se ao banco.








