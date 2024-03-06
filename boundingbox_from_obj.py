# -*- coding: utf-8 -*-
import sys 
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import utm 
import numpy as np 


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.icon_generation()
        self.central_widget = QWidget()

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Find Bounding Box')
        
        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)
        
        self.groupBox = QGroupBox()
        self.groupBox.setObjectName(u"groupBox")
        # self.groupBox.setMaximumSize(QSize(781, 80))
        
        grid = QGridLayout(self.groupBox)

        lbl = QLabel(self)
        lbl.setText('File :')
        lbl.adjustSize()
        self.qle_file = QLineEdit(self)
        
        self.open_obj = QPushButton(self,text='...')
        self.open_obj.setObjectName(u"Open Obj")
        self.open_obj.setStyleSheet(u"")
        
        grid.addWidget(lbl,0,0)
        grid.addWidget(self.qle_file,1,0)
        grid.addWidget(self.open_obj,1,2)
        
        grid_2 = QGridLayout(self)
        lbl_zone = QLabel(self)
        lbl_zone.setText('Zone :')
        lbl_zone.adjustSize()
        # self.qle_zone = QLineEdit(self)
        self.zone = QSpinBox(self)
        self.zone.setMinimum(1)
        self.zone.setMaximum(60)
        grid_2.addWidget(lbl_zone,0,0)
        grid_2.addWidget(self.zone,1,0)
        lbl_hem = QLabel(self)
        lbl_hem.setText('Hemisphere :')
        lbl_hem.adjustSize()
        self.combo_Hem = QComboBox()
        self.combo_Hem.addItem('S')
        self.combo_Hem.addItem('N')
        grid_2.addWidget(lbl_hem,0,1)
        grid_2.addWidget(self.combo_Hem,1,1)
    
        self.pushButton = QPushButton(self,text='Find')
        self.pushButton.setObjectName(u"Find")
        self.pushButton.setStyleSheet(u"")
        grid_2.addWidget(self.pushButton,1,2)
        self.pushButton.setEnabled(False)

        grid.addLayout(grid_2,2,0)
        
        #---------------------------------#
        self.groupBox2 = QGroupBox()
        self.groupBox2.setObjectName(u"groupBox")
        grid_part2 = QGridLayout(self.groupBox2)
               
        lbl_lat = QLabel(self)
        lbl_lat.setText('Latitude :')
        lbl_lat.adjustSize()
        self.qle_latitude = QLineEdit(self)
        
        lbl_long = QLabel(self)
        lbl_long.setText('Longitude :')
        lbl_long.adjustSize()
        self.qle_longitude = QLineEdit(self)
        
        lbl_alt = QLabel(self)
        lbl_alt.setText('Altitude :')
        lbl_alt.adjustSize()
        self.qle_alt = QLineEdit(self)
        
        grid_part2.addWidget(lbl_lat,0,0)
        grid_part2.addWidget(self.qle_latitude,1,0)
        
        grid_part2.addWidget( lbl_long,0,1)
        grid_part2.addWidget(self.qle_longitude,1,1)
        
        grid_part2.addWidget( lbl_alt,0,2)
        grid_part2.addWidget(self.qle_alt,1,2)
        

        #---------------------------------#
        self.groupBox3 = QGroupBox('Bounding Box')
        self.groupBox3.setObjectName(u"groupBox")
        grid_part3 = QGridLayout(self.groupBox3)
        
        lbl_maxX = QLabel(self)
        lbl_maxX.setText('Max X :')
        lbl_maxX.adjustSize()
        self.qle_maxX = QLineEdit(self)
        
        lbl_minX = QLabel(self)
        lbl_minX.setText('Min X :')
        lbl_minX.adjustSize()
        self.qle_minX = QLineEdit(self)
        
        grid_part3.addWidget(lbl_minX,0,0)
        grid_part3.addWidget(self.qle_minX,1,0)
        
        grid_part3.addWidget(lbl_maxX,2,0)
        grid_part3.addWidget(self.qle_maxX,3,0)
        
        lbl_maxY = QLabel(self)
        lbl_maxY.setText('Max Y :')
        lbl_maxY.adjustSize()
        self.qle_maxY = QLineEdit(self)
        
        lbl_minY = QLabel(self)
        lbl_minY.setText('Min Y :')
        lbl_minX.adjustSize()
        self.qle_minY = QLineEdit(self)
        
        grid_part3.addWidget(lbl_minY,0,1)
        grid_part3.addWidget(self.qle_minY,1,1)
        
        grid_part3.addWidget(lbl_maxY,2,1)
        grid_part3.addWidget(self.qle_maxY,3,1)
        
        lbl_maxZ = QLabel(self)
        lbl_maxZ.setText('Max Z :')
        lbl_maxZ.adjustSize()
        self.qle_maxZ = QLineEdit(self)
        
        lbl_minZ = QLabel(self)
        lbl_minZ.setText('Min Z :')
        lbl_minZ.adjustSize()
        self.qle_minZ = QLineEdit(self)
        
        grid_part3.addWidget(lbl_minZ,0,2)
        grid_part3.addWidget(self.qle_minZ,1,2)
        
        grid_part3.addWidget(lbl_maxZ,2,2)
        grid_part3.addWidget(self.qle_maxZ,3,2)

        #---------------------------------#
        self.grid_layout.addWidget(self.groupBox, 1,0)
        self.grid_layout.addWidget(self.groupBox2, 2,0)
        self.grid_layout.addWidget(self.groupBox3, 3,0)
        
        self.open_obj.clicked.connect(self.func_open_obj)
        self.pushButton.clicked.connect(self.find_coord)
    
    def icon_generation(self):
        
        my_pixmap = QPixmap("icone_real.ico")
        my_icon = QIcon(my_pixmap)
        self.setWindowIcon(my_icon)
        
    def func_open_obj(self):
        
        self.path,_ = QFileDialog.getOpenFileName(self, 'Open Obj (*.obj)', '','Obj Files (*.obj)')
        self.qle_file.setText(self.path)
        self.pushButton.setEnabled(True)

    
    def find_coord(self):
        try:
            self.coordenations()
        except:
            self.criticalMessage()

        
    
    def get_obj_geometry(self):
        # with open(self.path,'r') as read_data:
             
        #     del read_data[0:2]
        #     name = read_data.split(' ')
        #     print(name)

        objFile = open(self.path, 'r')
    
        vertexList = []
        textureList = []
    
        finalVertexList = []
        finalTextureList = []
    
        finalVertexListIdx = []
        finalTextureListIdx = []
    
        currentMaterial = ''
        materialsList = []

        for line in objFile:
            # print(line)
            split = line.split()
            #if blank line, skip
            if not len(split):
                continue
            # print(split)
            if split[0] == "usemtl":
                currentMaterial = split[1:]
            if split[0] == "v":
                vertexList.append(np.float64(split[1:]))
            elif split[0] == "vt":
                textureList.append(split[1:])
            elif split[0] == "f":
                count=1
                firstSet=[]
                firstTextureSet=[]
                materialsList.append(currentMaterial[0])
                while count<4:
                    removeSlash = split[count].split('/')
                    if count == 1:
                        firstSet.append(vertexList[int(removeSlash[0])-1][0:3])
                        firstTextureSet.append(textureList[int(removeSlash[1])-1])
                    elif count == 2:
                        firstSet.append(vertexList[int(removeSlash[0])-1][0:3])
                        firstTextureSet.append(textureList[int(removeSlash[1])-1])
                    elif count == 3:
                        firstSet.append(vertexList[int(removeSlash[0])-1][0:3])
                        firstTextureSet.append(textureList[int(removeSlash[1])-1])
    
                    count+=1
                finalVertexList.append(firstSet)
                finalTextureList.append(firstTextureSet)

        objFile.close()
        return finalTextureList, finalVertexList, materialsList, np.asarray(vertexList)
    
        
    def coordenations(self):
        _, _, _, vertexList = self.get_obj_geometry()

        easting_min = np.min(vertexList[:,0])
        easting_max = np.max(vertexList[:,0])
        northing_min = np.min(vertexList[:,1])
        northing_max = np.min(vertexList[:,1])
        elevation_min = np.min(vertexList[:,2])
        elevation_max = np.max(vertexList[:,2])
        elevation_mean = np.mean((elevation_min,elevation_max))

        
        if self.combo_Hem.currentText() == 'S':

            lat_min,long_min = self.utm_find(easting_min,northing_min,int(self.zone.value()),False)
            lat_max,long_max = self.utm_find(easting_max,northing_max,int(self.zone.value()),False)
            lat_mean,long_mean = self.utm_find(np.mean((easting_min, easting_max)), np.mean((northing_min, northing_max)),int(self.zone.value()),False)

        else:
            
            lat_min,long_min = self.utm_find(easting_min,northing_min,int(self.zone.value()),True)
            lat_max,long_max = self.utm_find(easting_max,northing_max,int(self.zone.value()),True)
            lat_mean,long_mean = self.utm_find(np.mean((easting_min, easting_max)), np.mean((northing_min, northing_max)),int(self.zone.value()),True)
        
        self.qle_latitude.setText(str(lat_mean))
        self.qle_longitude.setText(str(long_mean))
        self.qle_alt.setText(str(elevation_mean)) 
        
        self.qle_maxX.setText(str(long_max))
        self.qle_maxY.setText(str(lat_max))
        self.qle_maxZ.setText(str(elevation_max))
        
        self.qle_minX.setText(str(long_min))
        self.qle_minY.setText(str(lat_min))
        self.qle_minZ.setText(str(elevation_min))

    
    
    def utm_find(self,easting, northing,zone,bool_hem):
        return utm.to_latlon(easting, northing, zone, northern=bool_hem)
        
        
    def criticalMessage(self):
        my_pixmap = QPixmap("icone_real.ico")
        my_icon = QIcon(my_pixmap)
        
        reply = QMessageBox()
        reply.setWindowIcon(my_icon)
        reply.setIcon(QMessageBox.Critical)
        reply.setText('ERROR')
        reply.setWindowTitle("ERROR")
        reply.exec_()


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    window = MyWindow()
    window.setMaximumSize(QSize(450, 300))
    window.setMaximumSize(QSize(450, 300))
    window.show()
    app.exec()