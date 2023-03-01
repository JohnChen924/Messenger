import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, simpledialog
from ds_messenger import DirectMessenger
import time, os

class Body(tk.Frame):
    
    def __init__(self, root, select_callback=None):
        """
        declare variables
        """
        global sendto
        sendto = [] #to use when selecting who to send in the widget
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._posts = None
        self._draw()
    
    def node_select(self, event):
        """
        works when an item in the treeview is selected
        """
        self.entry_editor.delete(0, tk.END)
        index = int(self.posts_tree.selection()[0])-1
        entry = self._posts
        curItem = self.posts_tree.focus()
        sendto.append(self.posts_tree.item(curItem)['text'])
        for i in range(len(self._posts)): #loops around and unwraps the first layer of the list to be inserted in the box with the given name
            if self._posts[i]['from'] == sendto[len(sendto)-1]:
                    self._set_text(self._posts[i]['message'], self._posts[i]['timestamp'])
        del sendto[0]
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    def _set_text(self,_list:list, _time:list):
        """
        loops and unwraps the text and time to and insert it into the listbox. Used only with node_select function
        """
        self.entry_editor.delete(0, tk.END)
        _list.reverse()
        _time.reverse()
        for i in range(len(_list)):
            self.entry_editor.insert(tk.END,_time[i] +' - ' +  _list[i], '\n')
        
    def set_text_entry(self, text:str):
        """
        puts text in the listbox. Works with send function
        """
        self.entry_editor.insert(0,text,'\n')

    def set_posts(self, posts:list):
        """
        prep to place text in the treeview widget
        """
        self._posts = posts
        for i in range(len(self._posts)):
            self._insert_post_tree(i, self._posts[i])


    def insert_post(self, post):
        """
        prep to insert a text into the treeview. Works with add user only
        """
        self._posts.append(post)
        self._insert_post_tree(len(self._posts), post)

    def reset_ui(self):
        """
        clear the entire window
        """
        self.entry_editor.delete(0)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def _insert_post_tree(self, id, post = None):
        """
        puts the name of the sender to the treeview
        """
        entry = post
        self.posts_tree.insert('', id, id, text = post['from'])
        
    def insert_add(self,id, user):
        """
        Insert added username to treeview.
        """
        if user != None:
            self.posts_tree.insert('', id, id, text = user)
        
    def _draw(self):
        """
        draws the widgets, backgrounds of the file
        """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=10, pady=10)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame)
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Listbox(editor_frame, width=0,justify = tk.CENTER)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    
    def __init__(self, root, save_callback=None, online = None, add_user = None):
        """
        declare variables
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self.msg = tk.StringVar()
        self.msg.set("Type messages here")
        self._save_callback = save_callback
        self.add_user = add_user
        self._online_callback = online
        self.is_online = tk.IntVar()
        self._draw()

    def new(self):
        """
        works with check button to see whether it was checked.
        """
        chk_value = self.is_online.get()
        self._online_callback(chk_value)
    
    def save_click(self):
        """
        works when save button is clicked
        """
        if self._save_callback is not None:
            self._save_callback()
            
    def word(self):
        """
        recieve the input message by the user
        """
        msg = self.msg.get()
        self.msg.set("")
        return msg

    def _draw(self):
        """
        puts the buttons on the canvas
        """
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        add_user = tk.Button(master=self, text = 'Add User', width = 20)
        add_user.configure(command=self.add_user)
        add_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        self.chk_button = tk.Checkbutton(master=self, variable = self.is_online)
        self.chk_button.configure(command=self.new) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)
        inbox = tk.Entry(master=self,fg='BLACK', bd= 1,width=150,textvariable=self.msg, justify= CENTER)
        inbox.pack(side= tk.RIGHT)


class MainApp(tk.Frame):
    
    def __init__(self, root):
        """
        declare variables
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._current_profile = None
        self.profile = None
        self._is_online = False
        self.dsu = None
        self.username = None
        self.password = None
        self.token = None
        self.count = 0
        self._draw()
    
    def add(self):
        """
        add user to the treeview with the information written by user in the popup window
        """
        self.count+=1
        root = tk.Tk()
        root.withdraw()
        a = simpledialog.askstring("Input", "Input User")
        self.body.insert_add(self.count, a)

    def close(self):
        """
        closes the window
        """
        self.root.destroy()

    def send(self):
        """
        sends message to the selected user when the send button is clicked
        """
        msg = self.footer.word()
        self.body.set_text_entry(msg)
        if len(sendto) != 0:
            recipient = sendto[len(sendto)-1]
            self.profile.send(msg, recipient)
            
    def online_new(self, value:bool):
        """
        retrieve new message if there are any otherwise inserts no new messages into the listbox
        """
        self._is_online = bool(value)
        if self._is_online is True and len(self.profile.retrieve_new()) == 0:
            self.body.reset_ui()
            self.body.set_text_entry("No New Messages")
        else:
            self.body.reset_ui()
            self.body.set_posts(self.profile.retrieve_all())

        
    def _draw(self):
        """
        combines the things drawn in footer and body class into one. Also makes a separate popup window to help inform the users what to do
        https://stackoverflow.com/questions/43932106/tkinter-how-to-fix-the-window-opening-position-while-letting-the-width-and-heig
        ^^^ helps place the popup in the center of the screen
        """
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.title("READ")
        root.geometry("250x225")
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        root.geometry("+{}+{}".format(positionRight, positionDown))
        txt = tk.Text(root, height = 15,width = 30)
        txt.insert(0.0,"Available for Server 168.235.86.101:\nUsername: Clowna (or) Clownb\n(or) Clownc (or) Clownd\nPassword: pwd123\n\nNotice: Only Clowna has infor-mation")
        txt.insert(10.0,"\nUser Message will be hidden when revisiting to protect privacy!\nClick Check Button to view New Message.\nMessenger will only show received messages upon loading")
        txt.configure(state='disabled')
        txt.pack()
        a = simpledialog.askstring("Input", "Input a Server")
        self.dsu = a
        if self.dsu == "" or self.dsu == None:
            raise Exception("ERROR! NO SERVER DETECTED!")
        a = simpledialog.askstring("Input", "Input a Username")
        self.username = a
        a = simpledialog.askstring("Input", "Input a Password")
        self.password = a
        self.profile = DirectMessenger(self.dsu,self.username,self.password)
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Close', command=self.close)
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.body.set_posts(self.profile.retrieve_all())
        self.count = len(self.profile.retrieve_all())
        if self.count == 0: #when no messages are received, puts text and photo on the ui
            self.body.set_text_entry("It's quiet in here... People who message you will appear here")
        self.footer = Footer(self.root, save_callback=self.send,online = self.online_new, add_user = self.add)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        

if __name__ == "__main__":
    """
    runs the program
    """
    main = tk.Tk()
    main.title("ICS 32 Messenger Demo")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()
