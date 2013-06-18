import praw, subprocess, time, tkMessageBox
from Tkinter import *

r = praw.Reddit(user_agent='commenter')

def login(username, password):
            r.login(username, password)

class subreddit(object):
    def __init__(self, name):
        """a subreddit with given name

        __init__ (string) 
        """
        self.sub = r.get_subreddit(name)
        self.posts = None

    def get_top(self):
        """get top submissions of subreddit

        """
        self.posts = list(self.sub.get_top())

    def get_new(self):
        """get new submissions of subreddit

        """
        self.posts = list(self.sub.get_new())

    def find_post(self, title):
        """find the index of a submission with given title in
        the subreddit

        find_submission(str) -> int
        """
        for post in self.posts:
            if title in post.title:
                index = self.posts.index(post)
                return self.posts[index]

    def comment(self, post, text):
        """comment text into submission

        comment(str,str)
        """
        self.find_post(post).add_comment(text)

class Controller(Frame):
    
    def __init__(self, master):
        """Create app elements: Main frame, login options and 

        Constructor:Controller(Tk)

        """
        self.master= master

        """login"""        
        loginframe = Frame(self.master)
        Button(loginframe, text='Login',
               command=self.login).pack(padx=10)
        self.username = Entry(loginframe)
        self.username.pack()
        self.password = Entry(loginframe)
        self.password.pack()
        self.v = StringVar()
        Label(loginframe, textvariable=self.v).pack()
        self.x = IntVar()
        chk = Checkbutton(loginframe, text='Shutdown after commented', variable=self.x)
        chk.pack(side=LEFT)
        loginframe.pack(side=LEFT)
        """entry field"""
        entryframe = Frame(self.master)
        Label(entryframe, text='Subreddit').pack()
        self.sub = Entry(entryframe)
        self.sub.pack()
        Label(entryframe, text='Post Title').pack()
        self.post = Entry(entryframe)
        self.post.pack()
        entryframe.pack()
        """text field"""
        textframe = Frame(self.master)
        Label(textframe, text='Comment').pack()
        self.text = Text(textframe, width=30, height=20)
        self.text.pack()
        Button(textframe, text='Submit',
               command=self.submit).pack()
        textframe.pack()
        Label(self.master, text='Created by Danejazone').pack(side=BOTTOM)


    def login(self):
        """login to reddit using username and password

        """
        if len(self.username.get()) > 0:
            try:
                r.login(self.username.get(),self.password.get())
                self.v.set('Logged in')
            except Exception:
                self.v.set('Invalid username or password')
            
    def submit(self):
            sub = subreddit(self.sub.get())
            title = self.post.get()
            text = self.text.get('1.0','end')
            if r.is_logged_in() == False:
                tkMessageBox.showinfo('Error','Not Logged in')
                return
            while True:
                sub.get_new()
                try:
                    sub.comment(title,text)
                    if self.x.get() == 1:
                        subprocess.call(["shutdown.exe", "-f", "-s", "-t", "30"])
                    return
                except Exception:
                    pass
            
class CommentApp():
    def __init__(self, master=None):
        master.title("Reddit AutoComment")
        self.controller = Controller(master)

def main():
    root = Tk()
    root.geometry("500x500")
    root.resizable(width=FALSE, height=FALSE)
    app = CommentApp(root)
    root.mainloop()
    
if  __name__ == '__main__':
    main()
