with open("ConvertMe.txt") as read_data:
    ConvertFile = read_data.readlines()

if len(ConvertFile) < 2:
    print("No Files to convert!")
    exit()
elif ConvertFile[0][-4:] == "obj\n" and ConvertFile[1][-4:] == "mtl\n":
    ObjFileAddress = "TempFiles/" + ConvertFile[0][0:-1]
    MtlFileAddress = "TempFiles/" + ConvertFile[1][0:-1]
elif ConvertFile[1][-4:] == "obj\n" and ConvertFile[0][-4:] == "mtl\n":
    ObjFileAddress = "TempFiles/" + ConvertFile[1][0:-1]
    MtlFileAddress = "TempFiles/" + ConvertFile[0][0:-1]
else:
    print("Cannot Convert Files! Wrong Files Types!")
    exit()

with open(ObjFileAddress) as read_data:
    ObjFile = read_data.readlines()


    
FrontMatter = "xof 0303txt 0032\n"
MiddleMatter = ""
TotalLoops = 0
GlobalV = 0
GlobalN = 0
GlobalT = 0
TotalMaterials = 0
FoundO = False
FinalLoop = False

#LoopStart
while True:
    for Line in range(len(ObjFile)):
        if ObjFile[Line][:2] == "o " and FoundO:
            NewObjI = Line
            NewObjFile = ObjFile[Line:]
            ObjFile = ObjFile[:Line]
            FoundO = False
            break
        elif ObjFile[Line][:2] == "o " and not FoundO:
            FoundO = True
    if FoundO:
        FinalLoop = True
    
    VCoordNum,TCoordNum,NormNum,FaceNum,MaterialNum = 0,0,0,0,0
    
    for Line in ObjFile:
        if Line.find("v ",0,2) != -1:
            VCoordNum +=1
        if Line.find("vt ",0,3) != -1:
            TCoordNum +=1
        if Line.find("vn ",0,3) != -1:
            NormNum +=1
        if Line.find("f ",0,2) != -1:
            FaceNum +=1
        if Line.find("usemtl",0,6) != -1:
            MaterialNum +=1
    
    VCoord = [[]] * (VCoordNum)
    TCoord = [[]] * (TCoordNum)
    Norm =   [[]] * (NormNum)
    
    FaceV =   [[None]*3 for _ in range(FaceNum)]
    FaceT =   [[None]*3 for _ in range(FaceNum)]
    FaceN =[[None]*3 for _ in range(FaceNum)]
    FaceMaterial = [None] * FaceNum
    Material = [None] * MaterialNum
    FaceCorner = [None] * FaceNum
    
    VCoordI = 0
    TCoordI = 0
    NormI = 0
    FaceI = 0
    FaceY = 0
    MaterialI = 0
    
    for Line in ObjFile:
        if Line.find("v ",0,2) != -1:
            VCoord[VCoordI] = Line[2:].split()
    #        ThisVertex = VCoord[VCoordI]
    #        for i in range(len(ThisVertex)):
    #            ThisVertex[i] = float(ThisVertex[i])
            VCoordI += 1        
        elif Line.find("vt ",0,3) != -1:
            TCoord[TCoordI] = Line[3:].split()
            TCoordI +=1
        elif Line.find("vn ",0,3) != -1:
            Norm[NormI] = Line[3:].split()
            NormI +=1
        elif Line.find("usemtl",0,6) != -1:
             Material[MaterialI] = str(Line[7:].split(" "))          
             MaterialI += 1
        elif Line.find("f ",0,2) != -1:
            FaceX = 0
            FaceMaterial[FaceY] = MaterialI - 1     
            VTN = Line[2:].split()
            FaceCorner[FaceY] = len(VTN) 
            for Corner in VTN:
                TempVTN = Corner.split('/')
                if FaceX>2:
                    FaceV[FaceY].append(TempVTN[0])
                    FaceT[FaceY].append(TempVTN[1])
                    FaceN[FaceY].append(TempVTN[2])
                else:
                    FaceV[FaceY][FaceX] = TempVTN[0]
                    FaceT[FaceY][FaceX] = TempVTN[1]
                    FaceN[FaceY][FaceX] = TempVTN[2]
                FaceX += 1
            FaceY += 1
    
    
    with open(MtlFileAddress) as read_data:
        MtlFile = read_data.readlines()
    
    MatObj = [[None] * 5 for _ in range(MaterialNum)]
    MatObjI = 0
    MatPropI = 0
    
    for Line in MtlFile:
        if Line.find("newmtl ",0,7) != -1:
            ThisName = str(Line[7:].split(" ",1))
            for Name in range(MaterialNum):
                if Material[Name] in ThisName:
                    MatObjI = Name
                    break
        elif Line.find("Ns ",0,3) != -1: # Specular Exponent
            TempList = Line[2:].split()
            MatObj[MatObjI][1] = TempList[0]
        elif Line.find("Ka ",0,3) != -1: # Ambient light RGB value
            MatObj[MatObjI][2] = Line[2:].split()
        elif Line.find("Kd ",0,3) != -1: # Diffuse Light RGB value
            MatObj[MatObjI][0] = Line[2:].split()
        elif Line.find("d ",0,2)  != -1:  # Opacity percent
            TempList = Line[1:].split()
            MatObj[MatObjI][0].append(TempList[0]) 
        elif Line.find("map_Kd",0,6) != -1:
            MatObj[MatObjI][4] = Line[7:]
    
    #Write all our stuff out to a new .x file
    
    
    TotalCorners = 0
    for i in FaceCorner:
        TotalCorners += int(i)

        
    VCoordString = ""
    Loops = 1
    for Face in FaceV:
        for Vert in Face:
            if Loops == TotalCorners:
                VCoordString += "; ".join(VCoord[int(Vert)-1-(GlobalV)]) + ";;"
            else:
                VCoordString += "; ".join(VCoord[int(Vert)-1-(GlobalV)]) + ";,\n"
            Loops += 1
    
    iii = 0
    Loops = 0
    FaceVString = ""
    VCornerString = ""
    for i in range(len(FaceV)):
        FaceVString += str(FaceCorner[Loops]) + ";"
        for VI in range(FaceCorner[Loops]):
            if (VI + 1) == FaceCorner[Loops]:
                if (i + 1) == len(FaceV):
                    FaceVString += str(iii) + ";;"
                else:
                    FaceVString += str(iii) + ";,\n"
            else:
                FaceVString += str(iii) + ","
            iii += 1
        Loops += 1
            
    Loops = 1
    NString = "0.000000; 0.000000;-1.000000;,\n"
    for i in Norm:
        if Loops == NormNum:
            NString += "; ".join(i) + ";;"
        else:
            NString += "; ".join(i) + ";,\n"
        Loops += 1
    
    Loops = 0
    FaceNString = ""
    NCornerString = ""
    for i in FaceN:
        if GlobalN:
            for wannabe in range(len(i)):
                i[wannabe] = int(i[wannabe]) - GlobalN
                i[wannabe] = str(i[wannabe])            
        NCornerString = str(FaceCorner[Loops]) + ";"
        if Loops == (FaceNum - 1):
            FaceNString += NCornerString + ",".join(i) + ";;"
        else:
            FaceNString += NCornerString + ",".join(i) + ";,\n"
        Loops += 1
        
    TCoords = [None] * TotalCorners
    TI = 0
    ItemI = 0
    for TList in FaceT:
        for Item in TList:
            TCoords[TI] = TCoord[int(Item) - 1 - (GlobalT)]
            TI += 1
    
    Loops = 1
    TString = ""
    for i in TCoords:
        if Loops == TotalCorners:
            TString += "; ".join(i) + ";;"
        else:
            TString += "; ".join(i) + ";,\n"
        Loops += 1

    Loops = 1
    MatIString = ""
    for i in FaceMaterial:
        if Loops == FaceNum:
            MatIString += str(i) + ";;"
        else:
            MatIString += str(i) + ",\n"
        Loops+=1
    
    ObjLoops = 0
    MatString = ""
    MatAlias = ""
    for Obj in MatObj:
        PropLoops = 0
        MatString += "Material Mat" + str(TotalMaterials) + "[\n"
        MatAlias += "[Mat" + str(TotalMaterials) + "]\n"
        TotalMaterials += 1
        for Prop in Obj:
            if PropLoops == 4:
                if Prop != None:
                    MatString += "TextureFilename [\"" + Prop[:-1] + "\";]\n"
                else:
                    MatString += "TextureFilename [\"X:\\\\3dGame\\\\data\\\\Clear.png\";]\n"
                MatString += "]\n"
            elif PropLoops == 1:
                MatString += Obj[1] + ";\n"
            elif PropLoops == 3:
                MatString += "0.000000; 0.000000; 0.000000;;\n"
            elif Prop != None:
                MatString += "; ".join(Prop) + ";;\n"
            PropLoops += 1
        ObjLoops += 1
    
    FrontMatter += MatString
    MiddleMatter += f'''
     Frame Cube [
        FrameTransformMatrix [
           1.000000, 0.000000, 0.000000, 0.000000,
           0.000000, 1.000000, 0.000000, 0.000000,
           0.000000, 0.000000, 1.000000, 0.000000,
           0.000000, 0.000000, 0.000000, 1.000000;;
        ]
    
        Mesh [ // Cube mesh
    {TotalCorners};
    {VCoordString}
    {FaceNum};
    {FaceVString}
          MeshNormals [ // Cube normals
    {NormNum + 1};
    {NString}
    {FaceNum};
    {FaceNString}
          ] // End of Cube normals
          MeshTextureCoords [ // Cube UV coordinates
    {TotalCorners};
    {TString}
          ] // End of Cube UV coordinates
          MeshMaterialList [ // Cube material list
    {MaterialNum};
    {FaceNum};
    {MatIString}
    {MatAlias}
          ] // End of Cube material list
        ] // End of Cube mesh
      ] // End of Cube'''    

    if FinalLoop:
        break
    ObjFile = NewObjFile
    GlobalV += VCoordNum
    GlobalN += NormNum
    GlobalT += TCoordNum
    #LoopEnd

FrontMatter += f'''

Frame Root [
  FrameTransformMatrix [
     1.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 1.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 1.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 1.000000;;
  ] // CUT HERE
'''

EndMatter = "\n] // End of Root\n"

XF = FrontMatter + MiddleMatter + EndMatter

XF = XF.replace("[","{")
XF = XF.replace("]","}")

XFileAddress = "ConvertedFiles/" + ConvertFile[1][:-4] + "x"

with open(XFileAddress,'w') as X_File:
    print(X_File.write(XF))
print(XF)
