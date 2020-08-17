# gui using Tkinter
# Allison Poh
# 2020

import tkinter as tk
from Scraper import scrape_titles

#dropdown options for option menus
seasonlist = ['01','02','03','04','05','06','07','08','09','n/a']
episodelist = [
    ['01','02','03','04','05','06','n/a'],
    ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','n/a'],
    ['01','02','03','04','05','06','07','08','09','10/11','12','13','14','15','16','17','18','19','20','21','22','23','24/25','n/a'],
    ['01/02','03/04','05/06','07/08','09','10/11','12','13','14','15','16','17','18/19','n/a'],
    ['01/02','03','04','05','06','07','08','09','10','11','12','13','14/15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','n/a'],
    ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17/18','19','20','21','22','23','24','25','26','n/a'],
    ['01','02','03','04','05','06','07','08','09','10','11/12','13','14','15','16','17/18','19','20','21','22','23','24','25/26','n/a'],
    ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','n/a'],
    ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22/23','24/25','26','n/a']
]
speakerlist = ['Michael','Dwight','Jim','Pam','Ryan','Andy','Stanley','Kevin','Meredith','Angela','Oscar','Phyllis','Toby','Kelly','Creed','Darryl','Erin','Gabe','n/a']

#change episode drowdown options based on season selected
def update_episodes(self,*args):
    try:
        arr = episodelist[int(var_season.get())-1]
    except:
        arr = episodelist[len(episodelist)-1]

    menu = menu_episode['menu']
    menu.delete(0, 'end')

    for item in arr:
        command=lambda item=item: var_episode.set(item)
        menu.add_command(label=item,command=command)

#print new output to text
def update_output(arr):
    text_box.configure(state='normal')
    text_box.delete('1.0', 'end')
    for item in arr:
        text_box.insert('end',item + '\n')
    text_box.configure(state='disabled')

#get inputs from gui elements when search clicked
def get_input():
    season = var_season.get()
    episode = var_episode.get()
    speaker = var_speaker.get()
    keyword = ent_keyword.get()
    update_output(scrape_titles(season,episode,speaker,keyword))

#pack gui together (and position elements)    
def pack_all(*arg, **karg):
    lbl_header.pack()
    menu_season.pack(padx=10,side=tk.LEFT,fill=tk.X,expand=True)
    menu_episode.pack(padx=10,side=tk.LEFT,fill=tk.X,expand=True)
    menu_speaker.pack(padx=10,side=tk.LEFT,fill=tk.X,expand=True)
    ent_keyword.pack(padx=10,side=tk.LEFT,fill=tk.BOTH,expand=True)
    btn_search.pack(padx=10,side=tk.LEFT,fill=tk.BOTH,expand=True)
    lbl_instructions.pack(padx=10,side=tk.LEFT,fill=tk.X,expand=True)
    text_box.pack(fill=tk.BOTH,expand=True)
    frm_title.pack(pady=20,fill=tk.X)
    frm_input_labels.pack(fill=tk.X)
    frm_input.pack(fill=tk.X)
    frm_output.pack(padx=10,pady=7,fill=tk.BOTH,expand=True)
    frm_all.pack(fill=tk.BOTH,expand=True)
  
window = tk.Tk()
window.geometry('1100x720')

window.winfo_toplevel().title("The Office Quote Finder")

frm_all = tk.Frame(bg='black')
frm_title = tk.Frame(master=frm_all,bg='black')
frm_input_labels = tk.Frame(master=frm_all,bg='black',borderwidth=2)
frm_input = tk.Frame(master=frm_all,bg='black',borderwidth=2)
frm_output = tk.Frame(master=frm_all,borderwidth=1,relief='flat')

#header/title label
lbl_header = tk.Label(master=frm_title,text='The Office',fg='white',bg='black',borderwidth=2,relief='ridge',padx=10,pady=5,font='Helvetica 24 bold')

lbl_instructions = tk.Label(master=frm_input_labels,text='enter season, episode, speaker, and/or keyword to search for quotes',fg='white',bg='black',font='Helvetica 10',anchor='w')

#season option menu
var_season = tk.StringVar(window)
var_season.set(seasonlist[0])
menu_season = tk.OptionMenu(frm_input,var_season,*seasonlist,command=update_episodes)
menu_season.config(fg='black',bg='white',activebackground='white',borderwidth=2,relief='flat',font='Helvetica 10')

#episode option menu
var_episode = tk.StringVar(window)
var_episode.set(episodelist[0][0])
menu_episode = tk.OptionMenu(frm_input,var_episode,*episodelist[0])
menu_episode.config(fg='black',bg='white',activebackground='white',borderwidth=2,relief='flat',font='Helvetica 10')

#speaker/character option menu
var_speaker = tk.StringVar(window)
var_speaker.set(speakerlist[0])
menu_speaker = tk.OptionMenu(frm_input,var_speaker,*speakerlist)
menu_speaker.config(fg='black',bg='white',activebackground='white',borderwidth=2,relief='flat',font='Helvetica 10')

#keyword entry box
ent_keyword = tk.Entry(master=frm_input,fg='black',bg='white',borderwidth=2,relief='flat',font='Helvetica 10')
ent_keyword.insert(0,'keyword...')

#search button
btn_search = tk.Button(master=frm_input,text='Search',command=get_input,fg='#0b5498',bg='white',activebackground='white',font='Helvetica 10 bold')

#output text box
text_box = tk.Text(master=frm_output,font='Helvetica 10')
text_box.config(state='disabled')

pack_all()
window.mainloop()