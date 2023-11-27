# README

## Descrição do Projeto

Este projeto é um backend de um aplicativo de cardápio que permite aos usuários criar, recuperar, atualizar e excluir grupos de produtos e produtos individuais. O backend é construído usando Flask, um microframework web para Python, e SQLAlchemy, um ORM (Object Relational Mapper) para Python que permite interagir com bancos de dados SQL.

## Recursos

### POST /menu/

Cria um novo menu. Os dados do menu são enviados como dados de formulário no corpo da solicitação. O menu é criado com um grupo e uma lista de produtos, cada um com um nome e um preço. Se o grupo já existir, os novos produtos serão adicionados ao grupo existente.

### GET /menu/<id>

Recupera um menu existente pelo seu ID. Retorna um objeto JSON com o grupo e a lista de produtos do menu.

### PUT /menu/<id>

Atualiza um menu existente pelo seu ID. Os novos dados do menu são enviados como um objeto JSON no corpo da solicitação. O menu é atualizado com um novo grupo e uma nova lista de produtos. Se um produto já existir no menu, seu preço será atualizado. Se um produto não existir no menu, ele será adicionado.

### GET /grupos/

Recupera uma lista de todos os grupos existentes. Retorna uma lista de strings, onde cada string é o nome de um grupo.

### GET /produtos/<grupo>

Recupera uma lista de todos os produtos em um grupo. Retorna uma lista de objetos JSON, onde cada objeto representa um produto com um nome e um preço.

### DELETE /grupos/<nome>

Exclui um grupo existente pelo seu nome. Todos os produtos no grupo também serão excluídos.

### DELETE /produtos/<nome>

Exclui um produto existente pelo seu nome. Se o produto existir, ele será excluído e a mensagem 'Produto excluído com sucesso!' será retornada. Se o produto não existir, a mensagem 'Produto não encontrado' será retornada com um código de status 404.

### GET /grupos_produtos/

Retorna uma lista de todos os grupos existentes, juntamente com os produtos em cada grupo. Cada item na lista é um objeto JSON que contém o nome do grupo e uma lista de produtos, onde cada produto é representado por um objeto JSON com um nome e um preço.

## Como usar

Para usar este backend, você pode enviar solicitações HTTP para as rotas acima. Você pode usar qualquer cliente HTTP para fazer isso, como curl, Postman ou um navegador web. Para rotas que requerem dados de entrada, os dados devem ser enviados no corpo da solicitação no formato apropriado (por exemplo, dados de formulário para POST /menu/ e JSON para PUT /menu/<id>).
