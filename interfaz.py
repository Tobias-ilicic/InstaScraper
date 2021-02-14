from tkinter import *
from PIL import ImageTk, Image
import instaloader
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


root = Tk()
root.title("InstaScrap")
root.iconbitmap("C:/Users/tobi/Desktop/Proyectos/tkinter/imagenes/instagram1.ico")

def analizar(Usuario,Contraseña,Cuenta):
    L = instaloader.Instaloader()
    # Logear
    L.login(Usuario, Contraseña)        # (login)
    # Obtiene la metadata del perfil
    profile = instaloader.Profile.from_username(L.context, Cuenta)

    # Scrapeo los seguidores y seguidos
    lista_Seguidores = []
    for seguidor in profile.get_followers():
        lista_Seguidores.append(seguidor.username)
    lista_Seguidos = []
    for seguido in profile.get_followees():
        lista_Seguidos.append(seguido.username)

    #Esta es la parte que comparo las listas
    seguidoresMutuos = set(lista_Seguidos).intersection(lista_Seguidores)
    noSeguidores = list(set(lista_Seguidos) - seguidoresMutuos)
    fans = list(set(lista_Seguidores) - seguidoresMutuos)
    
    #abro nueva ventana con los resultados
    ventanaAnalisis = Toplevel()

    #titulos
    frameTitulos = Frame(ventanaAnalisis)
    frameTitulos.pack(side = "top")
    fanes = Label(frameTitulos, text = "Fans")
    noFollowers = Label(frameTitulos, text = "No seguidores")
    noFollowers.pack(side = "left",padx = 50,expand = "YES", fill = "x")
    fanes.pack(side = "right",padx = 50, expand = "YES",fill = "x")
    #hago display de las listas en la ventana
    #Slider de las listas
    verticalBar = Scrollbar(ventanaAnalisis)
    verticalBar.pack(fill = BOTH, side = LEFT)
    verticalBar2 = Scrollbar(ventanaAnalisis)
    verticalBar2.pack(fill = BOTH, side = RIGHT)
    #LISTA NO SEGUIDORES
    listaNoSeguidores = Listbox(ventanaAnalisis,yscrollcommand = verticalBar.set)
    listaNoSeguidores.pack(side = LEFT)
    listaNoSeguidores.insert(END, *noSeguidores)
    #LISTA DE FANS
    listaFans = Listbox(ventanaAnalisis,yscrollcommand = verticalBar)
    listaFans.pack(side = RIGHT)
    listaFans.insert(END, *fans)
    #config sliders
    verticalBar.config(command = listaNoSeguidores.yview)
    verticalBar2.config(command = listaFans.yview)
    #Botones
    def unfollow():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(5)
        browser.get('https://www.instagram.com/')
        sleep(10)
        usuario_input = browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
        #browser.execute_script("arguments[0].scrollIntoView();", usuario_input)
        contraseña_input = browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label")
        #browser.execute_script("arguments[0].scrollIntoView();", contraseña_input)
        usuario_input.send_keys(Usuario)
        contraseña_input.send_keys(Contraseña)
        IniciarSesion = browser.find_element_by_xpath("//button[@type='submit']")
        IniciarSesion.click()
        sleep(3)
        browser.get('https://www.instagram.com/'+ listaNoSeguidores.get(listaNoSeguidores.curselection()))
        sleep(2)
        try:                                 
            noSeguir = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
        except:
            noSeguir = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button")
        noSeguir.click()
        sleep(1)
        noSeguir2 = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]')
        noSeguir2.click()
    unfollow_btn = Button(ventanaAnalisis,text = "Unfollow",command = unfollow)
    unfollow_btn.pack()


    





#Funciones

def abrirVentanaPrincipal():
    usuario = str(usuarioInput.get())
    contraseña = str(contraseñaInput.get())
    nuevaVentana = Toplevel()
    nuevaVentana.geometry("400x400")
    #DEF
    botonAnalizar = Button(nuevaVentana,padx = 30,pady = 15, text = "Analizar seguidores",command = lambda : analizar(usuario,contraseña,"tobi_ilicic") )
    botonBuscar = Button(nuevaVentana,padx = 30,pady = 15, text = "¿Vio mi historia?")
    #Display
    botonAnalizar.grid(row = 0, column = 0,padx = 120,pady = 100)
    botonBuscar.grid(row = 1, column = 0,padx= 120, pady = 0)
    #Cierro la ventana Login
    nuevaVentana.mainloop()
    root.destroy()




#DEF
usuario = Label(root,text = "Usuario:")
contraseña = Label(root,text = "Contraseña:")
usuarioInput = Entry(root,width=30)
contraseñaInput = Entry(root,show = "*",width=30)
botonIngresar = Button(root,text = "Iniciar Sesion", command = abrirVentanaPrincipal)


#Display
usuario.grid(row=0,column=0)
contraseña.grid(row = 1,column = 0)
usuarioInput.grid(row = 0, column = 1)
contraseñaInput.grid(row = 1, column = 1)
botonIngresar.grid(row = 2, column = 0,columnspan = 2)


root.mainloop()