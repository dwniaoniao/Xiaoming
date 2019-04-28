import tkinter as tk
import tkinter.messagebox

root = tk.Tk()
menuBar = tk.Frame(root, relief='raised', bd=2)
menuBar.pack(fill='x')


def aboutButtonCommand():
    tkinter.messagebox.showinfo("About", "about\nabout")


def exitButtonCommand():
    exit()


aboutButton = tk.Button(menuBar, text='About', command=aboutButtonCommand)
exitButton = tk.Button(menuBar, text='Exit', command=exitButtonCommand)
aboutButton.pack(side='left')
exitButton.pack(side='left')

dialogueText = tk.Text(root)
dialogueText.pack(expand='yes', fill='both')
dialogueText.insert('end','text\n\n\n\n\n')
dialogueText.insert('end','fuck')
print(dialogueText.get(1.0,'end'))
dialogueText.delete('1.0','end')
scrollBar = tk.Scrollbar(dialogueText)
dialogueText.configure(yscrollcommand=scrollBar.set)
scrollBar.config(command=dialogueText.yview)
scrollBar.pack(side='right', fill='y')

def sendButtonCommand():
    speechText = inputText.get(1.0,'end')
    inputText.delete(1.0,'end')
    dialogueText.insert('end',speechText+'\n')
def f(event):
    speechText = inputText.get(1.0,'end')
    inputText.delete(1.0,'end')
    dialogueText.insert('end',speechText+'\n')
inputText = tk.Text(root, height=5)
inputText.pack(side='left', expand='yes', fill='both')
sendButton = tk.Button(root, text='Send',command=sendButtonCommand)
sendButton.pack(side='right', fill='both')
root.bind_all('<Return>',f)
root.mainloop()
