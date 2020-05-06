# read in <2.8 blender export file type>


# open(filename,mode) (optional second parameter, defaults to 'r'
# <mode> can be 'r' (read-only), 'w' (write-only), 'a' (append), 'r+' (read and write)
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

VCoordString = "0.000000; 0.000000;-1.000000;,\n"
Loops = 1
for i in VCoord:
    if Loops == VCoordNum:
        VCoordString += "; ".join(i) + ";;"
    else:
        VCoordString += "; ".join(i) + ";,\n"
    Loops += 1
Loops = 0
FaceVString = ""
VCornerString = ""
for i in FaceV:
    VCornerString = str(FaceCorner[Loops]) + ";"
    if Loops == (FaceNum - 1):
        FaceVString += VCornerString + ",".join(i) + ";;"
    else:
        FaceVString += VCornerString + ",".join(i) + ";,\n"
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
    NCornerString = str(FaceCorner[Loops]) + ";"
    if Loops == (FaceNum - 1):
        FaceNString += NCornerString + ",".join(i) + ";;"
    else:
        FaceNString += NCornerString + ",".join(i) + ";,\n"
    Loops += 1

TotalCorners = 0
for i in FaceCorner:
    TotalCorners += int(i)
    
TCoords = [None] * TotalCorners
TI = 0
ItemI = 0
for TList in FaceT:
    for Item in TList:
        TCoords[TI] = TCoord[int(Item) - 1]
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
    MatString += "Material Mat" + str(ObjLoops) + "[\n"
    MatAlias += "[Mat" + str(ObjLoops) + "]\n"
    for Prop in Obj:
        if PropLoops == 4:
            if Prop != None:
                MatString += "TextureFilename [\"" + Prop[:-1] + "\";]\n"
            MatString += "]\n"
        elif PropLoops == 1:
            MatString += Obj[1] + ";\n"
        elif PropLoops == 3:
            MatString += "0.000000; 0.000000; 0.000000;;\n"
        elif Prop != None:
            MatString += "; ".join(Prop) + ";;\n"
        PropLoops += 1
    ObjLoops += 1




XF = f'''xof 0303txt 0032

{MatString}

Frame Root [
  FrameTransformMatrix [
     1.000000, 0.000000, 0.000000, 0.000000,
     0.000000,-0.000000, 1.000000, 0.000000,
     0.000000, 1.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 1.000000;;
  ]
  Frame Cube [
    FrameTransformMatrix [
       1.000000, 0.000000, 0.000000, 0.000000,
       0.000000, 1.000000, 0.000000, 0.000000,
       0.000000, 0.000000, 1.000000, 0.000000,
       0.000000, 0.000000, 0.000000, 1.000000;;
    ]

    Mesh [ // Cube mesh
{VCoordNum + 1};
{VCoordString}
{FaceNum};
{FaceVString}
      MeshNormals [ // Cube normals
{NormNum + 1};
{NString}
{FaceNum}
{FaceNString}
      ] // End of Cube normals
      MeshTextureCoords [ // Cube UV coordinates
{TCoordNum};
{TString}
      ] // End of Cube UV coordinates
      MeshMaterialList [ // Cube material list
{MaterialNum};
{FaceNum};
{MatIString}
{MatAlias}
      ] // End of Cube material list
    ] // End of Cube mesh
  ] // End of Cube
] // End of Root'''

XF = XF.replace("[","{")
XF = XF.replace("]","}")

XFileAddress = "../data/" + ConvertFile[1][:-4] + "x"

with open(XFileAddress,'w') as X_File:
    print(X_File.write(XF))



#print(XF)



# pass .obj and .mtl files into script
# write XF to an .x file in desired location


# have .obj and .mtl files in a directory that the path knows to look in
# look in the directory, send those file names as variables to scipt
# at end of script, send write XF to a .x file in the same location as my other game assets




        
###    VERTICES
### number of vertices in each mesh in file 
 ### 3d pos each vertex 
### number of faces on polygon
### number of corners each faces has
### list of indices which correspond to the corners of each face
###     NORMALS
### number of unique normals in each mesh
### list of all 3d normals
### list of indices that correspond to the normals of each vertex on a face
###    MESH TEXTURE COORDS
### number total vertices in mesh
### 2D UV coordinates for each vertex
###    MESH MATERIAL LIST
### Number of materials used in mesh
### Number of faces in mesh
### index that tell which material was used for which face
###    MATERIAL OBJECT
### Material ID
### material RGBA value
### ??? value (96.0784)
### ??? 3d value (0.5)
### ??? 3d value (0.000)
### (Texture file name)

# each time it finds a block of relevant infomation, copy that block of information to your <.x file data struct>
# loop through the filled out data struct, writing all of the relevant information to an .x file in the appropriate order
# the end?

