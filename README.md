# nucle3d
DNA 3D Structure

## Nucle3D Structure Format
```
GENOME  hg38          #Tab split
[FEATURE1]  [VALUE1]  # User define features, tab split (CHR and GENOME key word reserved)
[FEATURE2]  [VALUE2]
...
CHR chr1  250,000(or 250000)  # Tab split
i,x,y,z
..
```
i is 0-index, gap of index i permitted

Multi Resolution for same chromosome permitted
