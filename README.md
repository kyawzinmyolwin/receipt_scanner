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

## Convert to Money Manager TSV

If you already generated receipt `.xlsx` files in `outputs/`, convert them into a Money Manager-compatible `.tsv` file:

```bash
python convert_to_money_manager.py --inputs-dir outputs --output outputs/money_manager.tsv
```

Rules applied by this converter:

- `Period`: detected date from each source `.xlsx` text (falls back to file modified date)
- `Accounts`: `ASB`
- `Income/Expense`: `Exp.`
- `Currency`: `NZD`
- `Subcategory`, `Note`, `Description`: blank
- `Category`: detected using keyword mapping in `CATEGORY_KEYWORDS` (extendable)
