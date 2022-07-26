from tkinter import *
import tkinter.filedialog
from PIL import Image, ImageTk
import os

from clusters import *
import xlrd as xlrd

root = Tk()
root.title("Corona Virus Analyser Tool")


# MAIN CLASS
class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.initUI()
        self.data = Data()


    # DEFINE THE GUI
    def initUI(self):
        self.labelhead = Label(self, text="Corona Virus Data Analysis Tool", bg="red", fg="white",font=("", "20", "bold"),padx=250)
        self.labelhead.pack(fill=X)

        self.frame = Frame(self, width=300, height=300)
        self.frame.pack(expand=True, fill=BOTH,padx=15,pady=13)  # .grid(row=0,column=0)
        self.canvas = Canvas(self.frame, bg='grey', width=300, height=300, scrollregion=(0, 0, 500, 500))
        self.hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = Scrollbar(self.frame, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300, height=300)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)

        self.frameButtons=Frame(self,bg='grey')
        self.frameButtons.pack(fill=X)
        self.load_country_data = Button(self.frameButtons, text="Upload Country Data",command=self.import_country_file)
        self.load_country_data.pack(side=LEFT,padx=(350,15))

        self.load_test_statistic = Button(self.frameButtons, text="Upload Test Statistics",command=self.importStatistics_file)
        self.load_test_statistic.pack(side=LEFT)
        #self.load_test_statistic.bind('<ButtonRelease-1>',self.import_files)

        self.frameSortCountries = Frame(self, borderwidth=1, bg='grey',relief=SOLID)
        self.frameSortCountries.pack(side=LEFT,padx=(15,0))
        self.labelsortCountries=Label(self.frameSortCountries,text='Sort Countries:',bg='grey')
        self.labelsortCountries.pack(pady=(7,5))
        self.sortbyName=Button(self.frameSortCountries,text='Sort by Name',command=self.sortByCountry)
        self.sortbyName.pack(pady=5)
        self.sortbyTotalCase=Button(self.frameSortCountries, text='Sort by Total Cases',command=self.sortByTotalCases)
        self.sortbyTotalCase.pack(padx=5,pady=(0,7))

        self.label2 = Label(self, text="Countries:",bg='grey')
        self.label2.pack(side=LEFT,padx=(20,0))

        self.frameCountriesListbox = Frame(self)
        self.frameCountriesListbox.pack(fill=Y, side=LEFT,pady=15)
        self.listbox2 = Listbox(self.frameCountriesListbox, width=40, height=7,selectmode=MULTIPLE)
        self.listbox2.pack(side=LEFT)
        self.scrollbar = Scrollbar(self.frameCountriesListbox)
        self.listbox2.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox2.yview)
        self.scrollbar.pack(side=LEFT, fill=Y)
        self.listbox2.bind('<ButtonRelease-1>',self.onSelectCountries)




        self.label3 = Label(self, text="Criterias:",bg='grey')
        self.label3.pack(side=LEFT,padx=(20,0))

        self.frameCriteriasListbox=Frame(self)
        self.frameCriteriasListbox.pack(fill=Y,side=LEFT,pady=15)
        self.listbox3 = Listbox(self.frameCriteriasListbox, width=40, height=7,selectmode=MULTIPLE)
        self.listbox3.pack(side=LEFT)
        self.scrollbar = Scrollbar(self.frameCriteriasListbox)
        self.listbox3.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox3.yview)
        self.scrollbar.pack(side=LEFT,fill=Y)
        self.listbox3.bind('<ButtonRelease-1>',self.onSelectCriterias)

        self.frameAnalyseData = Frame(self, borderwidth=1, bg='grey', relief=SOLID)
        self.frameAnalyseData.pack(side=LEFT, padx=(15, 15))
        self.labelAnalyseData = Label(self.frameAnalyseData, text='Analyse Data:', bg='grey')
        self.labelAnalyseData.pack(pady=(7, 5))
        self.buttonClusterCounties = Button(self.frameAnalyseData, text='Cluster Countries',command=self.onClickClusterCounteries)
        self.buttonClusterCounties.pack(pady=5,padx=5)
        self.buttonClusterCriterias = Button(self.frameAnalyseData, text='Cluster Criterias',command=self.onClickClusterCriterias)
        self.buttonClusterCriterias.pack(padx=5, pady=(0, 7))

        self.countryFiltered=0
        self.criteriasFiltered=0

    # IMPORTING COUNTRY FILE
    def import_country_file(self):
        paths = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",filetypes=(("Excel Files", "*.xlsx"), ("all files", "*.*")))
        # CREATE COUNTRY LIST
        workbook = xlrd.open_workbook(paths)
        sheet = workbook.sheet_by_index(0)
        total_row = sheet.nrows-1
        global country_names
        country_names = list()
        global data_matrix
        data_matrix = list()
        global criterias
        criterias = list()
        global countryDictionary
        countryDictionary=dict()

        for col in range(1,sheet.ncols):
            criterias.append(sheet.cell_value(0,col))
        for row in range(1, total_row):
            country_name = sheet.cell_value(row, 0)
            total_cases = sheet.cell_value(row, 1)
            total_deaths=sheet.cell_value(row,2)
            total_recovered=sheet.cell_value(row,3)
            active_cases=sheet.cell_value(row,4)
            serious_cases=sheet.cell_value(row,5)
            totalcase_1M=sheet.cell_value(row,6)
            if country_name== '': country_name=0
            if total_cases =='':total_cases=0.0
            if total_deaths=='':total_deaths=0.0
            if total_recovered=='':total_recovered=0.0
            if active_cases=='':active_cases=0.0
            if serious_cases=='':serious_cases=0.0
            if totalcase_1M=='':totalcase_1M=0.0

            countryDictionary[country_name]=total_cases
            country_names.append(country_name)

            data_matrix.append([total_cases, total_deaths,total_recovered, active_cases, serious_cases,totalcase_1M])
            self.listbox2.insert(END,country_name+'('+str(int(total_cases))+')')
        #print(criterias)
        #print(country_names)
        #print(data_matrix)
        #print()
    #THIS FUNCTION IMPORT STATISTICS FILE
    def importStatistics_file(self):
        paths = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",filetypes=(("Excel Files", "*.xlsx"), ("all files", "*.*")))
        # CREATE COUNTRY LIST
        workbook = xlrd.open_workbook(paths)
        sheet = workbook.sheet_by_index(0)
        total_row = sheet.nrows - 1
        for col in range(1,sheet.ncols):
            if col!=3:
                criterias.append(sheet.cell_value(0,col))

        for rowIndex in range(1,total_row):
            temp=str(sheet.cell_value(rowIndex,0)[1:len(sheet.cell_value(rowIndex,0))])
            if temp in country_names:
                for col in range(1, sheet.ncols):
                    if col != 3 and sheet.cell_value(rowIndex,col)!='':
                        data_matrix[country_names.index(temp)].append(sheet.cell_value(rowIndex,col))
                    elif col!=3 and sheet.cell_value(rowIndex,col)=='':
                        data_matrix[country_names.index(temp)].append(0.0)
        for rowIndexData in range(0,len(country_names)):
            if len(data_matrix[rowIndexData])!=10:
                for i in range(0,4):
                    data_matrix[rowIndexData].append(0.0)
        for index in range(len(criterias)):
            self.listbox3.insert(END,criterias[index])
        print(criterias)
        print(country_names)
        print(data_matrix)
        # for index in range(0,len(data_matrix)):
        #     print(str(data_matrix[index])+'     '+str(len(data_matrix[index])))



    def sortByCountry(self):
        orderedDict=dict(sorted((value,key) for (value,key) in countryDictionary.items()))
        keys=list(orderedDict.keys())
        self.listbox2.delete(0,END)
        for index in range(len(orderedDict)):
            self.listbox2.insert(END,keys[index]+'('+str(int(orderedDict[keys[index]]))+')')

    def sortByTotalCases(self):
        orderedDict={k: v for k, v in sorted(countryDictionary.items(), key=lambda item: item[1],reverse=True)}
        keys=list(orderedDict.keys())
        self.listbox2.delete(0,END)
        for index in range(len(orderedDict)):
            self.listbox2.insert(END,keys[index]+'('+str(int(orderedDict[keys[index]]))+')')
        # self.std_bsd_gpa()

    def onSelectCountries(self,event):
        w = event.widget
        self.countryFiltered=1
        global countriesFilter
        countriesFilter = [w.get(idx) for idx in w.curselection()]
        for countryNameIndex in range(0,len(countriesFilter)):
            countriesFilter[countryNameIndex]=countriesFilter[countryNameIndex][0:str(countriesFilter[countryNameIndex]).find('(')]
        print(countriesFilter)


    def onSelectCriterias(self,event):
        w = event.widget
        self.criteriasFiltered=1
        global criteriasFilter
        criteriasFilter = [w.get(idx) for idx in w.curselection()]
        print(criteriasFilter)

    def onClickClusterCounteries(self):
        colIndexes=list()
        rowIndexes=list()
        global newDataMatrix
        newDataMatrix=list()
        tempList=list()
        if self.countryFiltered==0 and self.criteriasFiltered== 0:
            clust=hcluster(data_matrix)
            kclust=kcluster(data_matrix,k=10)
            print(clust)
            printclust(clust,labels=None,n=0)
            printclust(clust,labels=country_names)
            drawdendrogram(clust,country_names,jpeg='deneme.jpg')
            image1 = Image.open('deneme.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.countryFiltered==1:
            for index in range(0,len(countriesFilter)):
                rowIndexes.append(country_names.index(countriesFilter[index]))
        if self.criteriasFiltered==1:
            for index in range(0,len(criteriasFilter)):
                colIndexes.append(criterias.index(criteriasFilter[index]))

        if self.countryFiltered==0 and self.criteriasFiltered==1:
            for row in range(0,len(country_names)):
                tempList = list()
                for col in colIndexes:
                    tempList.append(data_matrix[row][col])
                newDataMatrix.append(tempList)

            clust2 = hcluster(newDataMatrix)
            kclust2 = kcluster(newDataMatrix, k=10)
            print(clust2)
            printclust(clust2, labels=None, n=0)
            printclust(clust2, labels=country_names)
            drawdendrogram(clust2, country_names, jpeg='test.jpg')
            image1 = Image.open('test.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.countryFiltered==1 and self.criteriasFiltered==0:
            for row in rowIndexes:
                tempList = list()
                for col in range(0,len(criterias)):
                    tempList.append(data_matrix[row][col])
                newDataMatrix.append(tempList)

            clust3 = hcluster(newDataMatrix)
            kclust3 = kcluster(newDataMatrix, k=10)
            print(clust3)
            printclust(clust3, labels=None, n=0)
            printclust(clust3, labels=country_names)
            drawdendrogram(clust3, country_names, jpeg='test1.jpg')
            image1 = Image.open('test1.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.countryFiltered==1 and self.criteriasFiltered==1:
            for row in rowIndexes:
                tempList = list()
                for col in colIndexes:
                    tempList.append(data_matrix[row][col])
                newDataMatrix.append(tempList)

            clust4 = hcluster(newDataMatrix)
            kclust4 = kcluster(newDataMatrix, k=10)
            print(clust4)
            printclust(clust4, labels=None, n=0)
            printclust(clust4, labels=country_names)
            drawdendrogram(clust4, country_names, jpeg='test2.jpg')
            image1 = Image.open('test2.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))


    def onClickClusterCriterias(self):
        colIndexes = list()
        rowIndexes = list()
        global newDataMatrix
        newDataMatrix = list()
        tempList = list()
        if self.countryFiltered == 0 and self.criteriasFiltered == 0:
            newDataMatrix=rotatematrix(data_matrix)
            clust = hcluster(newDataMatrix)
            kclust = kcluster(newDataMatrix, k=10)
            print(clust)
            printclust(clust, labels=None, n=0)
            printclust(clust, labels=criterias)
            drawdendrogram(clust, criterias, jpeg='deneme.jpg')
            image1 = Image.open('deneme.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.countryFiltered == 1:
            for index in range(0, len(countriesFilter)):
                rowIndexes.append(country_names.index(countriesFilter[index]))
        if self.criteriasFiltered == 1:
            for index in range(0, len(criteriasFilter)):
                colIndexes.append(criterias.index(criteriasFilter[index]))

        if self.countryFiltered == 0 and self.criteriasFiltered == 1:
            for row in range(0, len(country_names)):
                tempList = list()
                for col in colIndexes:
                    tempList.append(data_matrix[row][col])
                newDataMatrix.append(tempList)
            newDataMatrix=rotatematrix(newDataMatrix)
            clust2 = hcluster(newDataMatrix)
            kclust2 = kcluster(newDataMatrix, k=10)
            print(clust2)
            printclust(clust2, labels=None, n=0)
            printclust(clust2, labels=country_names)
            drawdendrogram(clust2, criterias, jpeg='test.jpg')
            image1 = Image.open('test.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.countryFiltered == 1 and self.criteriasFiltered == 0:
            for row in rowIndexes:
                tempList = list()
                for col in range(0, len(criterias)):
                    tempList.append(data_matrix[row][col])
                newDataMatrix.append(tempList)

            newDataMatrix=rotatematrix(newDataMatrix)
            clust3 = hcluster(newDataMatrix)
            kclust3 = kcluster(newDataMatrix, k=10)
            print(clust3)
            printclust(clust3, labels=None, n=0)
            printclust(clust3, labels=country_names)
            drawdendrogram(clust3, criterias, jpeg='test1.jpg')
            image1 = Image.open('test1.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.countryFiltered == 1 and self.criteriasFiltered == 1:
            for row in rowIndexes:
                tempList = list()
                for col in colIndexes:
                    tempList.append(data_matrix[row][col])
                newDataMatrix.append(tempList)
            newDataMatrix=rotatematrix(newDataMatrix)
            clust4 = hcluster(newDataMatrix)
            kclust4 = kcluster(newDataMatrix, k=10)
            print(clust4)
            printclust(clust4, labels=None, n=0)
            printclust(clust4, labels=country_names)
            drawdendrogram(clust4, criterias, jpeg='test2.jpg')
            image1 = Image.open('test2.jpg')
            self.canvas.image = ImageTk.PhotoImage(image1)

            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox('all'))

# THIS CLASS HANDLES DATA
class Data:
    def __init__(self):
        self.countries = {}
        self.criteria_list = []
        self.counry_name = []
        self.data_matrix = []


# THIS CLASS HANDLES DATA FOR EACH COUNTRY
class Country:
    def __init__(self,country_name,total_cases, total_deaths, total_recovered, active_cases,serious_cases, total_case_rate):
        self.country_name=country_name
        self.total_cases = total_cases
        self.total_deaths = total_deaths
        self.total_recovered = total_recovered
        self.active_cases = active_cases
        self.serious_cases=serious_cases
        self.total_case_rate=total_case_rate

    def __repr__(self):
        return '[{},{},{},{},{},{}]'.format(
                            self.total_cases,
                            self.total_deaths,
                            self.total_recovered,
                            self.active_cases,
                            self.serious_cases,
                            self.total_case_rate)


myapp = GUI(root)
myapp.pack()
myapp.configure(bg='gray')
root.mainloop()

