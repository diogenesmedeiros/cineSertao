import random
from packages.database import *
from packages.smtp import *

import random

def purchaseTicket(user_data, session_data, menu_data):
    print(user_data)
    id_ingresso = random.randint(9999, 1000000)
    id_menu = random.randint(9999, 1000000)

    session_data["id"] = id_ingresso
    session_data["uid"] = user_data["session"]["uid"]
    session_data["cardapio_id"] = id_menu
    session_data["em_aberto"] = True

    menu_data["id_ingresso"] = id_ingresso

    sendEmail = False

    if AddDoc("ingressos_vendidos.txt", id_ingresso, session_data):
        if menu_data:
            if AddDoc("comida_vendidos.txt", id_menu, menu_data):
                sendEmail = True
        else:
            sendEmail = True
    else:
        sendEmail = False
    

    item_name = ""
    item_price = ""
    item_qty = ""
    menuCardapio = ""

    name_film = session_data.get("nome_filme", "N/A")
    chair_film = session_data.get("cadeiras", "N/A")
    preco_ingresso = session_data.get("preco_ingresso", "N/A")

    filmDict = f"""
    <h3>Detalhes do Filme</h3>
    <p>Nome do Filme: {name_film}</p>
    <p>Cadeiras: {chair_film}</p>
    <p>Preço Unitário do Ingresso: {preco_ingresso}</p>
    """

    for key, value in menu_data.items():
        if key.startswith("nome_"):
            item_name = value
            item_price = menu_data[f'preco_{item_name}']
            item_qty = menu_data[f'qtde_{item_name}']
            menuCardapio += f"""
            <tr>
                <td>{item_name}</td>
                <td>{item_price}</td>
                <td>{item_qty}</td>
            </tr>
            """

    comprovante = f"""
    <html>
    <body>
        <h2>NOTA FISCAL ELETRÔNICA</h2>
        <hr>
        <h3>DADOS DO COMPRADOR</h3>
        <p>Nome: {user_data["session"]['username']}</p>
        <p>Email: {user_data["session"]['email']}</p>
        <hr>
        {filmDict}
        <h3>COMIDA SELECIONADA</h3>
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>Nome</th>
                <th>Preço</th>
                <th>Quantidade</th>
            </tr>
            {menuCardapio}
        </table>
        <hr>
        <p>Data da Compra: {session_data.get("data_compra", "N/A")}</p>
        <p>Em aberto: {session_data.get("em_aberto", "N/A")}</p>
    </body>
    </html>
    """

    titulo = f"Confirmação de Entrega - Pedido #{id_ingresso}"
    
    if sendEmail:
        send_proof_tickets(comprovante, titulo, user_data["session"]["email"])
        return True
    else:
        return False

def getTicketUser(uid:str):
    usersTickets = ReadDoc("ingressos_vendidos.txt")

    user_data_tickets = {}

    for pk, columns, values in usersTickets:
        print(values)
        if str(uid) == str(values[5]):
            if pk not in user_data_tickets:
                user_data_tickets[pk] = {}

            for collumn, value in zip(columns, values):
                user_data_tickets[pk][collumn] = value

    return user_data_tickets

def allTicketsSold():
    docTickets = ReadDoc("ingressos_vendidos.txt")

    allDataTickets = {}

    for id, columns, values in docTickets:
        if id not in allDataTickets:
            allDataTickets[id] = {}

        for collumn, value in zip(columns, values):
            allDataTickets[id][collumn] = value
        
    return allDataTickets

def GeneratorTicketsSoldsTXT(tickets: dict):
    # obtendo a chave do dict
    keys_str = "-".join(tickets.keys())
    keys_str = keys_str[:50] if len(keys_str) > 50 else keys_str

    filename = f"..\\v1.0.1\\tickets\\tickets-{random.randint(1000, 9999)}#{keys_str}.txt"
    with open(filename, "w", encoding="utf-8") as db:
        for key, ticket in tickets.items():
            print(ticket)
            db.write(f"ID filme: {key}\nNome filme: {ticket['nome_filme']}\nUID do comprador: {ticket['uid']}\nCadeiras usuario: {ticket['cadeiras']}\nData da compra: {ticket['data_compra']}\nStatus: {ticket['em_aberto']} (True -> Nao pago, False -> Ja pago)\nPreco ingresso: {ticket['preco_ingresso']}")
    return True

def SearchMovieTicketsSold(query, ticketsSold):
    result = {}
    for key, ticket in ticketsSold.items():
        if query.lower() in ticket['nome_filme'].lower():
            result[key] = ticket
    return result