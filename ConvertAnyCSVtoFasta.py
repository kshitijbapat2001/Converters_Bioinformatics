import os
import pandas as pd
import argparse

def convert_csv_to_fasta(input_file, output_file=None, sequence_column=None, id_column=None):
    """
    Convert a CSV file containing protein sequences to FASTA format.
    
    Parameters:
    -----------
    input_file : str
        Path to the input CSV file
    output_file : str, optional
        Path to the output FASTA file. If not provided, uses input filename with .fasta extension
    sequence_column : str, optional
        Name of the column containing protein sequences. 
        If not specified, attempts to auto-detect based on common column names
    id_column : str, optional
        Name of the column containing sequence identifiers.
        If not specified, uses the index or attempts to auto-detect
    
    Returns:
    --------
    str
        Path to the generated FASTA file
    """
    # Read the CSV file
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # Automatically detect sequence column if not specified
    if sequence_column is None:
        sequence_columns = [
            col for col in df.columns 
            if any(keyword in col.lower() for keyword in ['sequence', 'seq', 'protein', 'aa'])
        ]
        if not sequence_columns:
            raise ValueError("Could not automatically detect sequence column. Please specify manually.")
        sequence_column = sequence_columns[0]

    # Automatically detect ID column if not specified
    if id_column is None:
        id_columns = [
            col for col in df.columns 
            if any(keyword in col.lower() for keyword in ['id', 'identifier', 'name', 'accession'])
        ]
        id_column = id_columns[0] if id_columns else None

    # Prepare output filename
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.fasta"

    # Write FASTA file
    with open(output_file, 'w') as f:
        for index, row in df.iterrows():
            # Determine sequence identifier
            if id_column:
                seq_id = str(row[id_column])
            else:
                seq_id = f"Sequence_{index+1}"
            
            # Get sequence
            sequence = str(row[sequence_column])
            
            # Write FASTA entry
            f.write(f">{seq_id}\n{sequence}\n")

    print(f"Converted {input_file} to FASTA format: {output_file}")
    return output_file

def batch_convert(input_directory, output_directory=None, 
                  sequence_column=None, id_column=None):
    """
    Convert multiple CSV files in a directory to FASTA format.
    
    Parameters:
    -----------
    input_directory : str
        Path to directory containing CSV files
    output_directory : str, optional
        Path to directory for output FASTA files. 
        If not provided, uses input directory
    sequence_column : str, optional
        Name of the column containing protein sequences
    id_column : str, optional
        Name of the column containing sequence identifiers
    
    Returns:
    --------
    list
        List of output FASTA file paths
    """
    # Validate input directory
    if not os.path.isdir(input_directory):
        raise ValueError(f"Input path {input_directory} is not a valid directory")

    # Set output directory
    if output_directory is None:
        output_directory = input_directory

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Find CSV files
    csv_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.csv')]

    # Convert files
    converted_files = []
    for csv_file in csv_files:
        input_path = os.path.join(input_directory, csv_file)
        output_path = os.path.join(output_directory, os.path.splitext(csv_file)[0] + '.fasta')
        
        converted_file = convert_csv_to_fasta(
            input_path, 
            output_file=output_path, 
            sequence_column=sequence_column, 
            id_column=id_column
        )
        
        if converted_file:
            converted_files.append(converted_file)

    return converted_files

def main():
    """
    Command-line interface for CSV to FASTA conversion
    """
    parser = argparse.ArgumentParser(description='Convert protein CSV files to FASTA format')
    parser.add_argument('input', help='Input CSV file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-s', '--sequence-column', help='Name of sequence column')
    parser.add_argument('-i', '--id-column', help='Name of identifier column')

    args = parser.parse_args()

    # Determine if input is a file or directory
    if os.path.isfile(args.input):
        # Single file conversion
        convert_csv_to_fasta(
            args.input, 
            output_file=args.output, 
            sequence_column=args.sequence_column, 
            id_column=args.id_column
        )
    elif os.path.isdir(args.input):
        # Batch conversion
        batch_convert(
            args.input, 
            output_directory=args.output, 
            sequence_column=args.sequence_column, 
            id_column=args.id_column
        )
    else:
        print("Error: Input must be a valid file or directory")

if __name__ == "__main__":
    main()
