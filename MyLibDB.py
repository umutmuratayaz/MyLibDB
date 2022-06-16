import os
import tkinter as tk
import tkinter.filedialog
from tkPDFViewer import tkPDFViewer as pdfView
import os
import getpass
import sqlite3
from shutil import move
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


def inputFiles():
    global inpFiles
    user = getpass.getuser()
    inpFiles = tk.filedialog.askopenfilenames(parent=master, title='Choose a file',filetypes=[("PDF Dosyası","*.pdf")],initialdir='C:/Users/%s' % user)    
    input_entry.delete(1, tk.END)
    input_view_text=str(len(inpFiles))+" Files Selected..."
    input_entry.insert(0,input_view_text)
    return inpFiles

def OutputPath():
    global outPath
    outPath=tk.filedialog.askdirectory()
    output_entry.delete(1, tk.END)
    output_entry.insert(0, outPath)
    return outPath

def DB_Path():
    global db_path
    db_path=tk.filedialog.askopenfilename(parent=master, title='Choose The Database')
    db_entry.delete(1,tk.END)
    db_entry.insert(0,db_path)
    Keyw_button.config(text='Add Keywords \n (File to File)')
    Db_button.config(text='Commit Files to DB')
    return db_path


def Add_DB():
    
    """Assigne Variables"""
    file_name=os.path.split(inpFiles[order])[1]
    current_dest=os.path.split(inpFiles[order])[0]
    source_dest=current_dest+'/'+file_name
    aim_dest=outPath+'/'+file_name
    print(order,file_name,current_dest,source_dest,aim_dest,db_path,sep="\n")

    
    """Read,Write Pdf Metadata"""
    file_in = open(source_dest, 'rb')
    try:
        pdf_reader = PdfFileReader(file_in)
        metadata = pdf_reader.getDocumentInfo()
    except:
        print("PdfFileReader couldn't read")
    
    try:
        title=metadata['/Title']

    except:
        title=''

    try:
        keywords_read=metadata['/Keywords']
    except:
        keywords_read=''

    keywords_merged=keywords_read+keywords
    file_in.close()

    pdf_info=(file_name,title,keywords_merged,"Not Read",aim_dest)


    """Write to Database"""
    with sqlite3.connect(db_path) as vt:
        im=vt.cursor()
        tableAdd="""CREATE TABLE IF NOT EXISTS Common ('File Name', 'Title', 'Keywords', 'Status', 'Destinion')"""
        im.execute(tableAdd)
        im.execute("""INSERT INTO Common VALUES (?,?,?,?,?)""",pdf_info)
        vt.commit()

    move(source_dest,aim_dest)
    
    return order


def Add_Keys(args):
    global keywords
    
    keywords+=", "+args
        
    return keywords
    

def All_Files_DB():
    global order
    order=-1
    for num in range(len(inpFiles)):
        orderNum()
        Add_DB()
    tk.messagebox.showinfo("Successful","Moved and Commit to DB the Selected PDFs")
    master.destroy()
    return order


def orderNum():
    global order, keywords
    keywords=''
    order+=1
    return keywords,order

def Go_Keys():
    global keywords, order
    Keyw_button.config(font="Minion 11 overstrike")
    order=0
    keywords=''
    Add_Keys('')
    label_file=os.path.split(inpFiles[order])[1]
    label_Fname.config(text=label_file[:60]+'\n'+label_file[60:120]+'\n'+label_file[120:])
    return keywords, order

def cycle():
    Add_DB()
    if order==(len(inpFiles)-1):
        tk.messagebox.showinfo("Successful","Moved and Commit to DB the Selected PDFs")
        master.destroy()
        quit()
    orderNum()
    label_file=os.path.split(inpFiles[order])[1]
    label_Fname.config(text=str(order+1)+"/"+str(len(inpFiles))+" : "+label_file[:60]+'\n'+label_file[60:120]+'\n'+label_file[120:])

def view():
    os.startfile(os.path.split(inpFiles[order])[0]+'/'+os.path.split(inpFiles[order])[1])
    
def Other_keys():
    oth_key=text6.get()
    Add_Keys(oth_key)
    
    
master=tk.Tk()
master.title("MyLibDatabases - PDF Library Tag Insert")
master.geometry('{}x{}'.format(1000, 850))

"""Create The Containers"""
top_frame = tk.Frame(master,width=800,height=200)
bottom_frame=tk.Frame(master)
lineH = tk.Frame(master, height=4, width=800, bg="grey80", relief='groove')


"""Master Grids"""
master.grid_rowconfigure(1, weight=1)
master.grid_columnconfigure(2, weight=1)

top_frame.grid(row=0, column=0, padx=15, pady=20,sticky=tk.NS)
bottom_frame.grid(row=2, column=0, padx=15, pady=10,sticky=tk.NS)
lineH.grid(row=1,column=0)

bottom_frame.grid_rowconfigure(20, weight=1)
bottom_frame.grid_columnconfigure(6, weight=1)




"""Top Frame"""
input_path = tk.Label(top_frame, text="Select PDF Files:")
input_entry = tk.Entry(top_frame, text="", width=30)
browse1 = tk.Button(top_frame, text="Browse", command=inputFiles,width=20)

output_path = tk.Label(top_frame, text="Output File Path:")
output_entry = tk.Entry(top_frame, text="", width=30)
browse2 = tk.Button(top_frame, text="Browse", command=OutputPath,width=20)

db_path = tk.Label(top_frame, text="Select Database File:")
db_entry = tk.Entry(top_frame, text="", width=30)
browse3 = tk.Button(top_frame, text="Browse", command=DB_Path,width=20)


Db_button = tk.Button(top_frame, text='',command=All_Files_DB,width=20,font="Minion 11")
Keyw_button = tk.Button(top_frame, text='',font="Minion 11",command=Go_Keys,width=20)


input_path.grid(row=0, column=0, padx=20, pady=10)
input_entry.grid(row=1, column=0, padx=20, pady=10)
browse1.grid(row=2, column=0, padx=20, pady=10)

output_path.grid(row=0, column=1, padx=20, pady=10)
output_entry.grid(row=1, column=1,padx=20, pady=10)
browse2.grid(row=2, column=1, padx=20, pady=10)

db_path.grid(row=0, column=2, padx=20, pady=10)
db_entry.grid(row=1, column=2,padx=20, pady=10)
browse3.grid(row=2, column=2, padx=20, pady=10)

Db_button.grid(row=0, column=3, padx=20, pady=10,sticky=tk.NS)
Keyw_button.grid(row=1, column=3, padx=20, pady=10,sticky=tk.NS,rowspan=2)



"""Bottom Frame"""
label_keyw = tk.Label(bottom_frame,text="ADD KEYWORD"+"_"*85,font="Calibri 12 underline")
label_Fname = tk.Label(bottom_frame,text="",font="Minion 11")
button_next = tk.Button(bottom_frame, text='Next PDF >',command=cycle,width=10,font="Minion 11")
view = tk.Button(bottom_frame, text='View This PDF',command=view,width=13,font="Minion 11")


label_keyw.grid(row=0, column=0, padx=10, pady=10,columnspan=4)
label_Fname.grid(row=1, column=0, padx=10, pady=10,rowspan=2,columnspan=2,sticky=tk.NW)
button_next.grid(row=1, column=2, padx=0, pady=5,sticky=tk.E)
view.grid(row=1, column=3, padx=1, pady=5,sticky=tk.E)

lineH2 = tk.Frame(bottom_frame, height=0, width=0)
lineH3 = tk.Frame(bottom_frame, height=0, width=0)
lineH4 = tk.Frame(bottom_frame, height=0, width=0)
lineH5 = tk.Frame(bottom_frame, height=0, width=0)
lineH6 = tk.Frame(bottom_frame, height=0, width=0)



label0 = tk.Label(bottom_frame,text="INDIVISUAL",font="Calibri 10 underline")
button1 = tk.Button(bottom_frame, text='Thesis',command=lambda: Add_Keys('Thesis'),width=15,font="Minion 11")
button2 = tk.Button(bottom_frame, text='Lecture',command=lambda: Add_Keys('Lecture'),width=15,font="Minion 11")
button3 = tk.Button(bottom_frame, text='Interesting',command=lambda: Add_Keys('Interesting'),width=15,font="Minion 11")
button4 = tk.Button(bottom_frame, text='Earth Sciences',command=lambda: Add_Keys('Earth Sciences'),width=15,font="Minion 11")
button5 = tk.Button(bottom_frame, text='Computer Sciences',command=lambda: Add_Keys('Computer Sciences'),width=15,font="Minion 11")
text6 = tk.Entry(bottom_frame, text="Type your the keyword",width=17,font="Calibri 12")
button6 = tk.Button(bottom_frame, text='^ Add Manuel ^',command=Other_keys ,width=15,font="Minion 11")

label2 = tk.Label(bottom_frame,text="NATURAL SCIENCES",font="Calibri 10 underline")
button21 = tk.Button(bottom_frame, text='Astronomy',command=lambda: Add_Keys('Astronomy'),width=15,font="Minion 11")
button22 = tk.Button(bottom_frame, text='Chemistry',command=lambda: Add_Keys('Chemistry'),width=15,font="Minion 11")
button23 = tk.Button(bottom_frame, text='Physics',command=lambda: Add_Keys('Physics'),width=15,font="Minion 11")
button24 = tk.Button(bottom_frame, text='Biology',command=lambda: Add_Keys('Biology'),width=15,font="Minion 11")
button25 = tk.Button(bottom_frame, text='Medicine',command=lambda: Add_Keys('Medicine'),width=15,font="Minion 11")
button26 = tk.Button(bottom_frame, text='Geography',command=lambda: Add_Keys('Geography'),width=15,font="Minion 11")
button27 = tk.Button(bottom_frame, text='Earth Sciences',command=lambda: Add_Keys('Earth Sciences'),width=15,font="Minion 11")

label3 = tk.Label(bottom_frame,text="SOCIAL SCIENCES",font="Calibri 10 underline")
button31 = tk.Button(bottom_frame, text='Economics',command=lambda: Add_Keys('Economics'),width=15,font="Minion 11")
button32 = tk.Button(bottom_frame, text='Anthropology',command=lambda: Add_Keys('Anthropology'),width=15,font="Minion 11")
button33 = tk.Button(bottom_frame, text='Archeology',command=lambda: Add_Keys('Archeology'),width=15,font="Minion 11")
button34 = tk.Button(bottom_frame, text='History',command=lambda: Add_Keys('History'),width=15,font="Minion 11")
button35 = tk.Button(bottom_frame, text='Law',command=lambda: Add_Keys('Law'),width=15,font="Minion 11")
button36 = tk.Button(bottom_frame, text='Political Sciences',command=lambda: Add_Keys('Political Sciences'),width=15,font="Minion 11")
button37 = tk.Button(bottom_frame, text='Psychology',command=lambda: Add_Keys('Psychology'),width=15,font="Minion 11")
button38 = tk.Button(bottom_frame, text='Sociology',command=lambda: Add_Keys('Sociology'),width=15,font="Minion 11")

label4 = tk.Label(bottom_frame,text="FORMAL and APPLIED SCIENCES",font="Calibri 10 underline")
button41 = tk.Button(bottom_frame, text='Engineering',command=lambda: Add_Keys('Engineering'),width=15,font="Minion 11")
button42 = tk.Button(bottom_frame, text='Mathematics',command=lambda: Add_Keys('Mathematics'),width=15,font="Minion 11")
button43 = tk.Button(bottom_frame, text='Statistic',command=lambda: Add_Keys('Statistic'),width=15,font="Minion 11")
button44 = tk.Button(bottom_frame, text='Computer Sciences',command=lambda: Add_Keys('Computer Sciences'),width=15,font="Minion 11")


lineH2.grid(row=5, column=4, padx=10, pady=20,columnspan=4)
lineH3.grid(row=9, column=4, padx=10, pady=5,columnspan=4)
lineH4.grid(row=13, column=4, padx=10, pady=5,columnspan=4)
lineH5.grid(row=17, column=4, padx=10, pady=5,columnspan=4)
lineH6.grid(row=20, column=4, padx=10, pady=15,columnspan=4)


label0.grid(row=6, column=0, padx=5, pady=10,columnspan=4)
button1.grid(row=7, column=0, padx=5, pady=5)
button2.grid(row=7, column=1, padx=5, pady=5)
button3.grid(row=7, column=2, padx=5, pady=5)
button4.grid(row=8, column=1, padx=5, pady=5)
button5.grid(row=8, column=0, padx=5, pady=5)
button6.grid(row=7, column=3, padx=5, pady=12,sticky=tk.S,rowspan=2)
text6.grid(row=7, column=3, padx=5, pady=12,sticky=tk.N,rowspan=2)


label2.grid(row=10, column=0, padx=5, pady=20,columnspan=4)
button21.grid(row=11, column=0, padx=5, pady=5)
button22.grid(row=11, column=1, padx=5, pady=5)
button23.grid(row=11, column=2, padx=5, pady=5)
button24.grid(row=11, column=3, padx=5, pady=5)
button25.grid(row=12, column=0, padx=5, pady=5)
button26.grid(row=12, column=1, padx=5, pady=5)
button27.grid(row=12, column=2, padx=5, pady=5)

label3.grid(row=14, column=0, padx=5, pady=10,columnspan=4)
button31.grid(row=15, column=0, padx=5, pady=5)
button32.grid(row=15, column=1, padx=5, pady=5)
button33.grid(row=15, column=2, padx=5, pady=5)
button34.grid(row=15, column=3, padx=5, pady=5)
button35.grid(row=16, column=0, padx=5, pady=5)
button36.grid(row=16, column=1, padx=5, pady=5)
button37.grid(row=16, column=2, padx=5, pady=5)
button38.grid(row=16, column=3, padx=5, pady=5)

label4.grid(row=18, column=0, padx=5, pady=10,columnspan=4)
button41.grid(row=19, column=0, padx=5, pady=5)
button42.grid(row=19, column=1, padx=5, pady=5)
button43.grid(row=19, column=2, padx=5, pady=5)
button44.grid(row=19, column=3, padx=5, pady=5)



master.mainloop()
