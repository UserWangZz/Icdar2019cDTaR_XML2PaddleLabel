# Icdar2019cDTaR_XML2PaddleLabel
This repository uses Python to convert the annotation format of the icdar2019cDTaR dataset to the annotation format recognized by the PaddleOCR table

# 1. Download the dataset
Icdar2019 cDTaR dataset: [download](https://github.com/cndplab-founder/ICDAR2019_cTDaR)

# Usage

```bash
python xml2paddle.py
```

# the annotation format of the ICDAR2019_cTDaR

```xml
<?xml version="1.0" encoding="UTF-8"?>
<document filename="table.jpg">
    <table>
        <Coords points="92,442 92,528 350,528 350,442"/>
        <cell start-row="0" start-col="1" end-row="0" end-col="1">
            <Coords points="154,442 154,453 200,453 200,442"/>
            <content>IndustryA</content>
        </cell>
        ...
        <cell start-row="4" start-col="4" end-row="4" end-col="4">
            <Coords points="334,517 334,528 350,528 350,517"/>
            <content>660</content>
        </cell>
    </table>
    ...
    <table>
        <Coords points="414,442 414,528 673,528 673,442"/>
        <cell start-row="0" start-col="1" end-row="0" end-col="1">
            <Coords points="477,442 477,453 522,453 522,442"/>
            <content>IndustryB</content>
        </cell>
        ...
    </table>
    ...
</document>

```

# the anotation format of the PaddleOCR

Every line is a json code:
```json
{
   'filename': PMC5755158_010_01.png,                            # image name
   'split': ’train‘,                                     # train set or test set or val set
   'imgid': 0,                                         # The index of the image 
   'html': {
     'structure': {'tokens': ['<thead>', '<tr>', '<td>', ...]},             # Html structure of tabel
     'cells': [
       {
         'tokens': ['P', 'a', 'd', 'd', 'l', 'e', 'P', 'a', 'd', 'd', 'l', 'e'],     # single text of the sell in the table
         'bbox': [x0, y0, x1, y1]                              # bbox about text, support xywh,xyxy, xyxyxyxy
       }
     ]
   }
}
```
More information about the PaddleOCR table rec: [reference](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_ch/table_recognition.md)