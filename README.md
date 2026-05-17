# Receipt Scanner

This app reads a receipt image, runs OCR, and exports extracted lines to Excel.

## Where to put image files

Put your receipt images in the `uploads/` folder at the project root:

- `uploads/receipt1.jpg`
- `uploads/receipt2.png`

Then run the app with that path, for example:

```bash
python app.py uploads/receipt1.jpg --output outputs/receipt1.xlsx
```

## Notes

- `uploads/` is the recommended input location.
- `outputs/` is the default location for generated Excel files.
- You can still pass any image path; it does not have to be inside `uploads/`.
