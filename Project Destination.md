Project Destination

1. Read the image
2. Extract text/data from the image (OCR)
3. Save the extracted data into Excel

Since you already work with Python, Excel automation, and text-processing workflows, this project is a very good portfolio project for you.

---

# Architecture

```text
Image (receipt/invoice/table)
        ↓
Python OCR Engine
        ↓
Extracted Text / Structured Data
        ↓
Pandas DataFrame
        ↓
Excel (.xlsx)
```

---

# Python Libraries

## 1. OCR (Text Extraction)

### Easy Start

* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract?utm_source=chatgpt.com)
* Python package: `pytesseract`

Good for:

* receipts
* invoices
* screenshots
* printed text

---

## 2. Image Processing

### Recommended

* [OpenCV](https://opencv.org/?utm_source=chatgpt.com)
* Python package: `opencv-python`

Used for:

* grayscale conversion
* thresholding
* noise removal
* improving OCR accuracy

---

## 3. Excel Export

### Recommended

* [Pandas](https://pandas.pydata.org/?utm_source=chatgpt.com)
* `openpyxl`

Used for:

* creating tables
* exporting `.xlsx`
* formatting data

---

## Phase 1 — Simple OCR

Start with:

* one image
* extract all text
* save into one Excel column

### Install

```bash
pip install pytesseract pillow pandas openpyxl
```

Install Tesseract Engine:

* macOS:

```bash
brew install tesseract
```

* Ubuntu:

```bash
sudo apt install tesseract-ocr
```

---

# Your First Working Example

```python
from PIL import Image
import pytesseract
import pandas as pd

# Load image
img = Image.open("receipt.jpg")

# OCR
text = pytesseract.image_to_string(img)

# Convert into rows
lines = text.split("\n")

# Create dataframe
df = pd.DataFrame(lines, columns=["Extracted Text"])

# Export to Excel
df.to_excel("output.xlsx", index=False)

print("Done!")
```

---

# Example Output

| Extracted Text |
| -------------- |
| NTUC FAIRPRICE |
| APPLE          |
| $5.20          |
| BREAD          |
| $2.10          |

---

# Phase 2 — Improve OCR Accuracy

After basic OCR works, add preprocessing.

## Add OpenCV

```bash
pip install opencv-python
```

Example:

```python
import cv2

image = cv2.imread("receipt.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

cv2.imwrite("processed.jpg", thresh)
```

Then OCR `processed.jpg`.



| Tool                                                                          | Purpose                      |
| ----------------------------------------------------------------------------- | ---------------------------- |
| [EasyOCR](https://github.com/JaidedAI/EasyOCR?utm_source=chatgpt.com)         | Easier deep-learning OCR     |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR?utm_source=chatgpt.com) | Very strong OCR accuracy     |
| [Amazon Textract](https://aws.amazon.com/textract/?utm_source=chatgpt.com)    | Cloud OCR for invoices/forms |
| [Google Vision AI](https://cloud.google.com/vision?utm_source=chatgpt.com)    | High-quality OCR API         |



---

# Project Structure

```text
receipt-scanner/
│
├── app.py
├── requirements.txt
├── uploads/
├── outputs/
├── processor/
│   ├── ocr.py
│   ├── parser.py
│   └── excel_export.py
│
└── templates/
```

