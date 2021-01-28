from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("InstaScrap")
root.iconbitmap("C:/Users/tobi/Desktop/Proyectos/tkinter/imagenes/instagram1.ico")

#Tengo que ver como pasarlo a otro archivo, importarlo y que me deje usarlo
from time import sleep
from selenium import webdriver
import time

seguidores=[]
seguidos = []
#Abro chrome y voy a instagram
def analizar(Usuario,Contraseña,Cuenta):
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com/')

    #Esto es para hacer el programa que labure en segundo plano, pero tiene bugs
    '''options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_window_size(1980, 1080)
    browser.get('https://www.instagram.com/')'''
    sleep(2)
    #Me logeo a mi cuenta
    usuario_input = browser.find_element_by_css_selector("input[name='username']")
    contraseña_input = browser.find_element_by_css_selector("input[name='password']")
    usuario_input.send_keys(Usuario)
    contraseña_input.send_keys(Contraseña)
    IniciarSesion = browser.find_element_by_xpath("//button[@type='submit']")
    IniciarSesion.click()
    sleep(5)
    #voy hasta el perfil
    cuenta = Cuenta
    browser.get("https://www.instagram.com/"+ cuenta +"/?hl=es-la")
    #cantidad de seguidores y seguidos
    cantSeguidos = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text) - 1
    cantSeguidores = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text) - 1
    #busco los seguidores
    seguidores2 = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    seguidores2.click()


    #Esto puede llegar a optimizar el programa pero tiene bugs
    '''cantSeguidoresEnteros = cantSeguidores // 12
    for i in range(12,cantSeguidoresEnteros,12):
    scr1 = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[%s]' % i)
    browser.execute_script("arguments[0].scrollIntoView();", scr1)
    sleep(0.01)'''

    
    for i in range(1,cantSeguidores):
        scr1 = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[%s]' % i)
        browser.execute_script("arguments[0].scrollIntoView();", scr1)
        sleep(0.001)
        text = scr1.text
        lista = text.split()
        seguidores.append(lista[0])

    browser.refresh()

    sleep(2)
    #busco los seguidos
    seguidos2 = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
    seguidos2.click()
    
    for i in range(1,cantSeguidos):
        scr1 = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[%s]' % i)
        browser.execute_script("arguments[0].scrollIntoView();", scr1)
        sleep(0.005)
        text = scr1.text
        lista = text.split()
        seguidos.append(lista[0])

    browser.quit()

    #Esta es la parte que comparo las listas
    seguidoresMutuos = set(seguidores).intersection(seguidos)
    noSeguidores2 = (set(seguidos)-seguidoresMutuos)
    noSeguidores = list(noSeguidores2)
    print(noSeguidores)
    #abro nueva ventana con los resultados
    ventanaAnalisis = Toplevel()
    ventanaAnalisis.geometry("400x400")

    #hago display de las listas en la ventana
    i = 0
    verticalBar = Scale(ventanaAnalisis,from_=0, to=200).grid(row=0,column = 1)
    w = Listbox(ventanaAnalisis,yscrollcommand = verticalBar)
    w.grid(row = 0, column = 0)
    for i in range(len(noSeguidores)):
        print(noSeguidores[i])
        w.insert(END, noSeguidores[i])
        i = i + 1


    





#Funciones

def abrirVentanaPrincipal():
    usuario = str(usuarioInput.get())
    contraseña = str(contraseñaInput.get())
    credenciales = [usuario,contraseña]
    nuevaVentana = Toplevel()
    nuevaVentana.geometry("400x400")
    #DEF
    botonAnalizar = Button(nuevaVentana,padx = 30,pady = 15, text = "Analizar seguidores",command = lambda : analizar(usuario,contraseña,"tobi_ilicic") )
    botonBuscar = Button(nuevaVentana,padx = 30,pady = 15, text = "¿Vio mi historia?")
    #Display
    botonAnalizar.grid(row = 0, column = 0,padx = 120,pady = 100)
    botonBuscar.grid(row = 1, column = 0,padx= 120, pady = 0)




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