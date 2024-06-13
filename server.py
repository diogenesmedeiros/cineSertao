from flask import Flask, session, render_template, request, flash, redirect, url_for
from packages.smtp import *
from packages.verify_input import *
from packages.auth import *
from packages.movie import *
from packages.user import *
from packages.tickets import *
from packages.canteen import *
from datetime import datetime
import os
import random

app = Flask(__name__)

app.secret_key = "12345"
app.config["UPLOAD_FOLDER"] = "uploads/"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.mkdir(app.config["UPLOAD_FOLDER"])
    os.mkdir(f'{app.config["UPLOAD_FOLDER"]}/movies/')
    os.mkdir(f'{app.config["UPLOAD_FOLDER"]}/users/')

logado = False

@app.route("/")
def Home():
    if VerifySession():
        logado = True
    else:
        logado = False

    filmes = GetMovies()

    return render_template("index.html", title="Inicio", logado=logado, filme=filmes)

#########################################################################
@app.route("/auth/signin", methods=["POST", "GET"])
def SignIn():
    if VerifySession():
        logado = True
    else:
        logado = False

    if logado == True:
        return redirect(url_for("Home"))
    else:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["senha"]

            if verifyInput(email) and verifyInput(password):
                if SigninUser(str(email), str(password)):
                    flash("Login feito com sucesso", "success")
                    return redirect(url_for("Home"))
                else:
                    flash("Usuario ou senha invalida", "danger")
            else:
                flash("Você precisa digitar algo", "danger")

    return render_template("signin.html", title="Login")

@app.route("/auth/signup", methods=["POST", "GET"])
def SignUp():
    if request.method == "POST":
        name = request.form["nome"]
        email = request.form["email"]
        password = request.form["senha"]
        isAdmin = request.form.get("isAdm", "off")

        print(isAdmin)

        typeUser = ""

        if isAdmin == "off":
            typeUser = "read"
        else:
            typeUser = "adm"

        if verifyInput(name) or verifyInput(email) or verifyInput(password):
            if SignupUser(email, password, name, typeUser):
                welcomeEmail(name, email)
                flash("Cadastro feito com sucesso", "success")
                return redirect(url_for("Home"))
            else:
                flash("Não foi possível realizar o cadastro", "danger")
        else:
            flash("Você precisar digitar algo", "danger")

    return render_template("signup.html", title="Cadastro")

@app.route("/auth/logout", methods=["GET"])
def Logout():
    if(LogoutUser()):
        flash("Você será redirecionado.")
        return redirect(url_for("Home"))
    else:
        flash("Aconteceu um erro inesperado")
    
    return render_template("logout.html", title="Sair da conta")

#########################################################################
@app.route("/management/addMovies", methods=["POST", "GET"])
def AddMovies():
    if VerifySession():
        logado = True
        
        if session["session"]["typeUser"] == "adm":
            if request.method == "POST":
                capa = request.files["thumbnail_filme"]
                titulo = request.form["titulo"]
                trailer = request.form["link_trailer"]
                descricao = request.form["descricao"]
                genero = request.form["genero"]
                data_lancamento = request.form["data_lancamento"]
                diretor = request.form["diretor"]
                elenco = request.form["elenco"]
                nota_imdb = request.form["nota_imdb"]
                capacidade_sessao = request.form["capacidade_sessao"]
                preco_ingresso = request.form["preco_ingresso"]
                data_disponivel = request.form["data_disponivel"]

                if verifyInput(capa.filename) or verifyInput(titulo) or verifyInput(trailer) or verifyInput(descricao) or verifyInput(genero) or verifyInput(data_lancamento) or verifyInput(diretor) or verifyInput(elenco) or verifyInput(nota_imdb) or verifyInput(capacidade_sessao) or verifyInput(preco_ingresso) or verifyInput(data_disponivel):
                    if capa:
                        filepath = os.path.join(f'{app.config["UPLOAD_FOLDER"]}movies/', f"{random.randint(9999, 1000000)}_{capa.filename}")
                        capa.save(f"static/{filepath}")

                        capa = filepath

                    if AddMovie(capa, titulo, descricao, genero, trailer, data_lancamento, diretor, elenco, nota_imdb, capacidade_sessao, preco_ingresso, data_disponivel):
                        flash("Filme adicionado com sucesso", "success")
                        return redirect(url_for("Home"))
                    else:
                        flash("Não foi possivel adicionar o filme, tente novamente", "danger")

            return render_template("addMovies.html", logado=logado)
        else:
            return render_template("notAdm.html")
    else:
        logado = False
        return redirect(url_for("SignIn"))
    
@app.route("/movies/<id>", methods=["GET"])
def GetFilme(id):
    if VerifySession():
        logado = True
    else:
        logado = False

    movie, cardapio = GetMovieById(id)

    movie[str(id)]["nota_imdb"] = float(movie[str(id)]["nota_imdb"])
    movie[str(id)]["filme_id"] = str(id)
    print(movie[str(id)])

    return render_template("viewMovies.html", title=movie[str(id)]["titulo"], filme=movie[str(id)], logado=logado)

@app.route("/movies/update/<id_filme>", methods=["GET", "POST"])
def UpdateFilme(id_filme):
    if id == "":
        return redirect(url_for("Home"))
    
    if VerifySession():
        logado = True

        if session["session"]["typeUser"] == "adm":
            movie, cardapio = GetMovieById(id)

            if request.method == "POST":
                capa = request.files["thumbnail_filme"] if verifyInput(request.files["thumbnail_filme"].filename) else movie[str(id_filme)]["capa"]
                titulo = request.form["titulo"] if verifyInput(request.form["titulo"]) else movie[str(id_filme)]["titulo"]
                trailer = request.form["link_trailer"] if verifyInput(request.form["link_trailer"]) else movie[str(id_filme)]["trailer"]
                descricao = request.form["descricao"] if verifyInput(request.form["descricao"]) else movie[str(id_filme)]["descricao"]
                genero = request.form["genero"] if verifyInput(request.form["genero"]) else movie[str(id_filme)]["genero"]
                data_lancamento = request.form["data_lancamento"] if verifyInput(request.form["data_lancamento"]) else movie[str(id_filme)]["data_lancamento"]
                diretor = request.form["diretor"] if verifyInput(request.form["diretor"]) else movie[str(id_filme)]["diretor"]
                elenco = request.form["elenco"] if verifyInput(request.form["elenco"]) else movie[str(id_filme)]["elenco"]
                nota_imdb = request.form["nota_imdb"] if verifyInput(request.form["nota_imdb"]) else movie[str(id_filme)]["nota_imdb"]
                capacidade_sessao = request.form["capacidade_sessao"] if verifyInput(request.form["capacidade_sessao"]) else movie[str(id_filme)]["capacidade_sessao"]
                preco_ingresso = request.form["preco_ingresso"] if verifyInput(request.form["preco_ingresso"]) else movie[str(id_filme)]["preco_ingresso"]
                data_disponivel = request.form["data_disponivel"] if verifyInput(request.form["data_disponivel"]) else movie[str(id_filme)]["data_disponivel"]

                if UpdateMovie(id_filme, capa, titulo, descricao, genero, trailer, data_lancamento, diretor, elenco, nota_imdb, capacidade_sessao, preco_ingresso, data_disponivel):
                    return redirect(url_for("Home"))

            return render_template("updateMovies.html", filme=movie[str(id_filme)], logado=logado)
        else:
            return render_template("notAdm.html", logado=logado)
    else:
        return redirect(url_for("Home"))
    
@app.route("/movies/remove/<id_filme>", methods=["GET"])
def DeleteFilme(id_filme):
    if(VerifySession()):
        if session["session"]["typeUser"] == "adm":
            if DeleteMovies(id_filme):
                return redirect(url_for("Home"))
            else:
                return redirect(url_for("Home"))
        else:
            return render_template("notAdm.html")

#########################################################################
@app.route("/reserve/<id_filme>", methods=["GET"])
def reserveSession(id_filme):
    if VerifySession():
        logado = True

        if session["session"]["typeUser"] == "read":
            movie, cardapio = GetMovieById(id_filme)

            movie[str(id_filme)]["nota_imdb"] = float(movie[str(id_filme)]["nota_imdb"])
            movie[str(id_filme)]["filme_id"] = str(id_filme)
            movie[str(id_filme)]["capacidade_sessao"] = int(movie[str(id_filme)]["capacidade_sessao"])

            return render_template("comprarIngressos.html", logado=logado, filme=movie[str(id_filme)], cardapio=cardapio)
        else:
            return redirect(url_for("Home"))

@app.route("/checkout", methods=["POST", "GET"])
def checkoutSession():
    if VerifySession():
        logado = True

        if session["session"]["typeUser"] == "read":
            if request.method == "POST":
                menu = request.form["menu"]
                chair = request.form["chair"]
                name_film = request.form["name_film"]
                preco_ingresso = request.form["preco_ingresso"]

                chair = chair.split(",")
                chair_formatado = ""

                for chair_f in range(len(chair)):
                    n = ""

                    if chair_f < len(chair) - 1:
                        n = " - "
                    else:
                        n = ""

                    chair_formatado += chair[chair_f] + n

                session_data = {
                    "nome_filme": name_film,
                    "cadeiras": chair_formatado,
                    "preco_ingresso": preco_ingresso,
                    "data_compra": datetime.now().strftime("%d/%m/%Y")
                }

                def process_menu(menu_str):
                    items_menu = menu_str.split(",")
                    menu_dict = {}

                    for item in items_menu:
                        if item:
                            nome, preco, qtde = item.split(":")
                            menu_dict[f'nome_{nome}'] = nome
                            menu_dict[f'preco_{nome}'] = float(preco)
                            menu_dict[f'qtde_{nome}'] = int(qtde)

                    return menu_dict
                
                menu_dict = process_menu(menu)
                
                if purchaseTicket(session, session_data, menu_dict):
                    print(session)

                    return render_template("sendTicketEmail.html", title="Ingresso enviado pelo email", logado=logado)
                else:
                    print("Erro ao realizar a compra.")
        else:
            return redirect(url_for("Home"))

@app.route("/management/listTicketsSold", methods=["POST", "GET"])
def ListTicketsSold():
    if VerifySession():
        logado = True
        ticketsSold = allTicketsSold()
        resultSearch = {}

        if request.method == "POST":
            qSearch = request.form.get("q", "")
            if qSearch:
                resultSearch = SearchMovieTicketsSold(qSearch, ticketsSold)
                GeneratorTicketsSoldsTXT(resultSearch)

        if session["session"]["typeUser"] != "adm":
            return render_template("notAdm.html")

        return render_template("listTicketsSold.html", title="Lista ingressos vendidos", ticketsSold=ticketsSold, resultSearch=resultSearch, logado=logado)
    else:
        flash("Você precisa estar logado para acessar esta página.", "danger")
        return redirect(url_for("Home"))
    
@app.route("/management/canteen", methods=["GET"])
def AllCanteen():
    if(VerifySession()):
        logado = True

        if session["session"]["typeUser"] == "adm":
            allFoods = AllFoods()

            return render_template("canteen.html", title="Cantina", foods=allFoods, logado=logado)
        else:
            return render_template("notAdm.html")
    else:
        return redirect(url_for("Home"))
    
@app.route("/management/canteen/<id_food>", methods=["GET", "POST"])
def updateFood(id_food):
    if(VerifySession()):
        logado = True

        if session["session"]["typeUser"] == "adm":
            allFoods = AllFoods()
            food = {}
            
            for index in allFoods:
                if str(id_food) == str(index):
                    food = allFoods[index]

            print(food)
            
            if request.method == "POST":
                capa = food["capa"]
                nome = request.form["nome"]
                preco = request.form["preco"]
                disponivel = request.form.get("disponivel")
                print(disponivel)

                if verifyInput(nome) and verifyInput(preco) and verifyInput(disponivel):
                    newData = {
                        "capa": capa,
                        "nome": nome,
                        "preco": preco,
                        "disponivel": disponivel
                    }

                    if UpdateFood(str(id_food), newData):
                        return redirect(url_for("AllCanteen"))
            
            return render_template("updateFood.html", title="Atualizar comida", logado=logado, food=food)
        else:
            return render_template("notAdm.html")
    else:
        return redirect(url_for("Home"))

#########################################################################
@app.route("/user/<uid>", methods=["GET"])
def GetUser(uid):
    if(VerifySession()):
        logado = True

        user = GetUserData(uid)

        if user:
            meus_ingressos = getTicketUser(uid)
            print(meus_ingressos)

            return render_template("viewUser.html", title=user["username"], user=user, myTickets=meus_ingressos, logado=logado)
        else:
            return redirect(url_for("Home"))
    else:
        return redirect(url_for("SignIn"))
    
@app.route("/users/fogotpassword", methods=["GET", "POST"])
def fogotPassword():
    if request.method == "POST":
        email = request.form["email"]
        forgot_password(email)

    return render_template("forgotPassword.html")

def forgot_password(email):
    found_user = None

    users = ReadDoc("users.txt")

    for pk, columns, values in users:
        if email == values[1]:
            found_user = values
            break

    if found_user:
        send_password_email(found_user)

#########################################################################
@app.route("/search", methods=["GET"])
def SearchFilme():
    qSearch = request.args.get("q")

    if qSearch == "" or not qSearch:
        return redirect(url_for("Home"))
    else:
        resultSearch = SearchMovie(qSearch)

        return render_template("searchMovie.html", title=qSearch, search=resultSearch)
    
#########################################################################
@app.route("/newsletter", methods=["GET", "POST"])
def Newsletter():
    if VerifySession():
        logado = True
        if session["session"]["typeUser"] == "adm":
            if request.method == "POST":
                titulo = request.form["titulo"]
                message = request.form["message"]

                newsLetter(message, titulo)
            return render_template('newsletter.html', title="Enviar emails", logado=logado)
    else:
        return render_template("notAdm.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)