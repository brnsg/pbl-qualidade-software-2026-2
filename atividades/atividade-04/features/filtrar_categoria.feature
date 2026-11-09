# language: pt
Funcionalidade: Filtrar restaurantes por categoria
  Como usuário do LocalEats
  Quero filtrar os restaurantes por categoria
  Para encontrar rapidamente o tipo de comida que desejo

  Cenário: Filtrar restaurantes da categoria Japonesa
    Dado que estou logado na página inicial do LocalEats
    Quando eu seleciono a categoria "Japonesa"
    Então todos os restaurantes exibidos devem ser da categoria "Japonesa"
    E nenhum restaurante da categoria "Italiana" deve ser exibido
