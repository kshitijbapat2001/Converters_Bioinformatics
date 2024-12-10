# CSV to FASTA Converter

## Overview

This Python script provides a flexible tool for converting CSV files containing protein sequences to FASTA format. It supports both single file and batch conversion, with intelligent column detection and customization options.

## Features

- Convert individual CSV files to FASTA format
- Batch convert multiple CSV files in a directory
- Automatic detection of sequence and identifier columns
- Customizable column selection
- Command-line interface for easy usage

## Requirements

- Python 3.7+
- pandas
- argparse (standard library)

## Installation

1. Ensure you have Python installed
2. Install required dependencies:
   ```
   pip install pandas
   ```

## Usage

### Command-Line Interface

#### Single File Conversion
```bash
python script.py input.csv
python script.py input.csv -o output.fasta
python script.py input.csv -s sequence_column -i id_column
```

#### Batch Conversion
```bash
python script.py /path/to/csv/directory
python script.py /path/to/csv/directory -o /path/to/output/directory
```

### Command-Line Arguments

- `input`: Input CSV file or directory (required)
- `-o, --output`: Output file or directory (optional)
- `-s, --sequence-column`: Name of sequence column (optional)
- `-i, --id-column`: Name of identifier column (optional)

## Column Detection

The script automatically attempts to detect:
- Sequence columns (keywords: 'sequence', 'seq', 'protein', 'aa')
- ID columns (keywords: 'id', 'identifier', 'name', 'accession')

If automatic detection fails, specify columns manually using command-line arguments.

## Example

Convert a protein sequence CSV to FASTA:
```bash
python script.py protein_sequences.csv -s protein_seq -i protein_id
```

## Error Handling

- Raises informative errors for invalid inputs
- Handles missing or unspecified columns
- Creates output directory if it doesn't exist

## Notes

- Sequence identifiers use column values or generated index if no ID column is found
- Output filename defaults to input filename with .fasta extension

## License

MIT License

## Contributing

Contributions welcome! Please submit pull requests or open issues on the project repository.
