# nucle3d
DNA 3D Structure

## Nucle3D Structure Text Format
```
GENOME  hg38          # Tab split
[FEATURE1]  [VALUE1]  # User define features, tab split (CHR and GENOME COL[\d+] key word reserved)
[FEATURE2]  [VALUE2]
...
COL0 [NAME]  [TYPE(int,string,float)] [DEFAULT VALUE IF MISSING or "NA"]   # Tab Split
COL1 [NAME]  [TYPE] [DEFAULT VALUE IF MISSING or "NA"]
...
CHR chr1  250,000(or 250000)  # Tab split
i,x,y,z
i,x,y,z,col0,col1...  # Other annotation permitted
..
```
i is 0-index, gap of index i permitted

Multi Resolution for same chromosome permitted


## Nucle3D Structure Binary Format


## Nucle3D Data Structure

### JavaScript

### GoLang
