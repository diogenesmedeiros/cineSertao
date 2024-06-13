import random
from difflib import *
from packages.formataData import formata_data
from packages.database import *

def AddMovie(capa:str, titulo:str, descricao:str, genero:str, trailer:str, data_lancamento:str, diretor:str, elenco:str, nota_imdb:str, capacidade_sessao:int, preco_ingresso: str, data_disponivel:str, ):
    dados_filme = {
        "capa": capa,
        "titulo": titulo,
        "descricao": descricao,
        "genero": genero,
        "trailer": trailer,
        "data_lancamento": formata_data(data_lancamento),
        "diretor": diretor,
        "elenco": elenco,
        "nota_imdb": nota_imdb,
        "preco_ingresso": preco_ingresso,
        "capacidade_sessao": capacidade_sessao,
        "data_disponivel": formata_data(data_disponivel),
    }
    
    if AddDoc("filmes.txt", random.randint(9999, 1000000), dados_filme):
        return True
    
def UpdateMovie(id_filme:str, capa:str, titulo:str, descricao:str, genero:str, trailer:str, data_lancamento:str, diretor:str, elenco:str, nota_imdb:str, capacidade_sessao:int, preco_ingresso: str, data_disponivel:str):
    newDataFilm = {
        "capa": capa,
        "titulo": titulo,
        "descricao": descricao,
        "genero": genero,
        "trailer": trailer,
        "data_lancamento": data_lancamento,
        "diretor": diretor,
        "elenco": elenco,
        "nota_imdb": nota_imdb,
        "preco_ingresso": preco_ingresso,
        "capacidade_sessao": capacidade_sessao,
        "data_disponivel": data_disponivel,
    }
    
    if UpdateDoc("filmes.txt", id_filme, newDataFilm):
        return True
    else:
        return False

def GetMovies():
    filmeReadL = ReadDoc("filmes.txt")

    count_films = 0
    filme_data = {}

    for pk, columns, values in filmeReadL:
        if pk not in filme_data:
            filme_data[pk] = {}

        for collumn, value in zip(columns, values):
            filme_data[pk][collumn] = value

    return filme_data

def GetMovieById(id_filme):
    cardapioReadL = ReadDoc("cardapio.txt")
    filmeReadL = ReadDoc("filmes.txt")

    filme_data = {}
    cardapio_data = {}

    for pk, columns, values in cardapioReadL:
        if pk not in cardapio_data:
            cardapio_data[pk] = {}

        for collumn, value in zip(columns, values):
            cardapio_data[pk][collumn] = value

    for pk, columns, values in filmeReadL:
        if pk not in filme_data:
            filme_data[pk] = {}

        for collumn, value in zip(columns, values):
            filme_data[pk][collumn] = value

    return filme_data, cardapio_data

def SearchMovie(qSearch:str):
    search_movie = ReadDoc("filmes.txt")

    matches = []
    for pk, columns, value in search_movie:
        if qSearch.lower() in value[1].lower():
            value.append(pk)
            matches.append(value)
        else:
            similarity = SequenceMatcher(None, qSearch.lower(), value[1].lower()).ratio()
            if similarity > 0.6:
                value.append(pk)
                matches.append(value)
    print(matches)
    return matches

def DeleteMovies(id):
    if RemoveDoc("filmes.txt", id):
        return True
    else:
        return False