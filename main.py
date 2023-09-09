import random
import tkinter
import tkinter.messagebox
import customtkinter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use("TkAgg")
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
#customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
size=20
current = np.full(size * size, 0.0).reshape(size, size)
def start(app):
    fig=plt.figure()
    ax1=fig.add_subplot(1,2,1)
    ax2=fig.add_subplot(1,2,2)
    # plt.interactive(False)
    # ax = plt.axes(xlim=(0, 17.5), ylim=(17.5, 0))
    infectedline, = ax2.plot([], [], lw=2)
    curedline,=ax2.plot([],[],lw=2)
    healthyline,=ax2.plot([],[],lw=2)
    deadline,=ax2.plot([],[],lw=2)
    ax1.grid()
    ax2.set_ylim(-0.1, 400.1)
    ax2.set_xlim(-0.1, 100.1)

    # initialization function: plot the background of each frame
    def init():
        infectedline.set_data([], [])
        curedline.set_data([], [])
        healthyline.set_data([], [])
        deadline.set_data([], [])
        return [infectedline,curedline,healthyline,deadline]

    global current
    current=app.start_state
    radius=app.slider_1.get()
    infectious=app.slider_2.get()
    deathrate=app.slider_3.get()
    reinfectious=app.slider_4.get()
    lifetime=app.slider_5.get()

    print(current)
    print(radius)
    def gol_step(arr):
        templist = []
        for i in range(size):
            for j in range(size):
                if arr[i][j]==0:
                    infection_result=0
                    for x in range(size):
                        for y in range(size):
                            if min((x-i+size)%size,(i-x+size)%size)+min((y-j+size)%size,(j-y+size)%size)<=radius \
                                    and 1<=arr[x][y]<lifetime and (i!=x or j!=y):
                                temp=random.random()
                                if temp<=infectious:
                                    infection_result=1
                    templist.append(infection_result)
                elif 1<=arr[i][j]<lifetime:
                    if arr[i][j]==(lifetime+1)//2:
                        temp=random.random()
                        if temp<=deathrate:
                            templist.append(-lifetime)
                        else:
                            templist.append(arr[i][j] + 1)
                    else:
                        templist.append(arr[i][j]+1)
                elif arr[i][j]==lifetime:
                    infection_result = lifetime
                    for x in range(size):
                        for y in range(size):
                            if min((x - i + size) % size, (i - x + size) % size) + min((y - j + size) % size,(j - y + size) % size) <= radius \
                                    and 1 <= arr[x][y] < lifetime and (i != x or j != y):
                                temp = random.random()
                                if temp <= reinfectious:
                                    infection_result = 1
                    templist.append(infection_result)
                else:
                    templist.append(arr[i][j])
        ans = np.array(templist)
        #print(ans.reshape(size,size))
        return ans.reshape(size, size)

    def f(x, y):
        return current/lifetime

    x = np.array([i for i in range(size)])
    y = np.array([i for i in range(size)]).reshape(-1, 1)
    im = ax1.imshow(f(x,y), animated=True,vmin=-1, vmax=1)
    infected=0
    cured=0
    dead=0
    for i in range(size):
        for j in range(size):
            if 0<current[i][j]<lifetime:
                infected+=1
            elif current[i][j]>=lifetime:
                cured+=1
            elif current[i][j]<0:
                dead+=1
    graphx=[0]
    infectedy=[infected]
    curedy=[cured]
    deady=[dead]
    healthyy=[size*size-infected-cured-dead]

    def updatefig(*args):
        global current
        #print(current)
        current = gol_step(current).reshape(size, size)
        im.set_array(f(x,y))
        return im,

    def updatefig2(i):
        graphx.append(i)
        infected = 0
        cured = 0
        dead = 0
        for i in range(size):
            for j in range(size):
                if 0 < current[i][j] < lifetime:
                    infected += 1
                elif current[i][j] >= lifetime:
                    cured += 1
                elif current[i][j] <0:
                    dead += 1
        infectedy.append(infected)
        curedy.append(cured)
        healthyy.append(size*size-infected-cured-dead)
        deady.append(dead)
        infectedline.set_data(graphx, infectedy)
        curedline.set_data(graphx,curedy)
        healthyline.set_data(graphx,healthyy)
        deadline.set_data(graphx,deady)

        return [infectedline,curedline,healthyline,deadline]

    plt.plasma()
    ani1 = animation.FuncAnimation(fig, updatefig,interval=50, blit=True)
    ani2 = animation.FuncAnimation(fig, updatefig2, init_func=init, interval=50, blit=True)
    plt.show()

class App(customtkinter.CTk):

    WIDTH = 1000
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Epidemic Prediction Simulator.py")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=600,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(2, weight=0)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(12, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="감염 반경",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=100)
        self.slider_1 = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=1,
                                                to=20,
                                                number_of_steps=19)
        self.slider_1.grid(row=1, column=0, pady=10, padx=20, sticky="we")
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="감염률",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_2.grid(row=3, column=0, pady=10, padx=100)
        self.slider_2 = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=0,
                                                to=1)
        self.slider_2.grid(row=4, column=0, pady=10, padx=20, sticky="we")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="치명률",
                                              text_font=("Roboto Medium", -16))
        self.label_3.grid(row=6, column=0, pady=10, padx=100)
        self.slider_3 = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=0,
                                                to=1)
        self.slider_3.grid(row=7, column=0, pady=10, padx=20, sticky="we")
        self.label_4 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="재발병률",
                                              text_font=("Roboto Medium", -16))
        self.label_4.grid(row=8, column=0, pady=10, padx=100)
        self.slider_4 = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=0,
                                                to=1)
        self.slider_4.grid(row=9, column=0, pady=10, padx=20, sticky="we")
        self.label_5 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="전염기간",
                                             text_font=("Roboto Medium", -16))
        self.label_5.grid(row=10, column=0, pady=10, padx=100)
        self.slider_5 = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=1,
                                                to=20,
                                                number_of_steps=19)
        self.slider_5.grid(row=11, column=0, pady=10, padx=20, sticky="we")
        self.start_button=customtkinter.CTkButton(master=self.frame_left,text='START',command=lambda :start(self))
        self.start_button.grid(row=12,column=0,pady=10,padx=20,sticky="s")

        # ============ frame_right ============

        # configure grid layout (20x20)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.buttons=[[None for _ in range(20)] for _ in range(20)]
        for i in range(20):
            for j in range(20):
                self.buttons[i][j]=customtkinter.CTkButton(master=self.frame_right,width=28,height=28,text="",corner_radius=0,
                                                command= lambda x=i,y=j :self.button_event(x,y),fg_color='white',border_color='RoyalBlue1',border_width=0.5)
        for i in range(20):
            for j in range(20):
                self.buttons[i][j].grid(row=i, column=j, pady=0, padx=0)

        # ============ frame_right ============

        # set default values
        self.start_state = np.full(size * size, 0).reshape(size, size)

    def button_event(self,x,y):
        print("Button pressed",x,y)
        if self.buttons[x][y].fg_color=='black':
            self.start_state[x][y]=0
            self.buttons[x][y].fg_color='white'
        else:
            self.start_state[x][y]=1
            self.buttons[x][y].fg_color='black'


    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()