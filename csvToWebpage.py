import pandas as pd
import sys

def read_local_csv(file_path):
    # Read the csv file into a DataFrame
    df = pd.read_csv(file_path)

    # Trim leading and trailing spaces from column names and data
    df.columns = df.columns.str.strip()
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    # Fill missing values with a placeholder
    df.fillna(' ', inplace=True)

    return df

def generate_html_report(df, output_file, header_title="Report"):
    # Create an HTML string template
    html_template = """
    <html>
    <head>
        <title>Form Responses Report</title>
        <style>
            body {{
                max-width: 1200px;
                margin-left: auto;
                margin-right: auto;
            }}
            h1 {{
                text-align: center;
            }}
            table {{
                table-layout: fixed;
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid black;
            }}
            th {{
                text-align: center;
                padding: .5rem;
            }}
            td{{
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <h1>{header_title}</h1>
        <table>
            <thead>
                <tr>
                    {headers}
                </tr>
            </thead>
            <tbody>
                {body}
            </tbody>
        </table>
    </body>
    </html>
    """
    # Get the list of headers from the DataFrame
    headers_html = "".join(f"<th>{header}</th>" for header in df.columns)

    # Initialize a string variable to store the HTML table rows
    body_html = ""

    # Generate table rows for each data entry
    for row in df.itertuples(index=False):
        # Get the values of the data row based on the DataFrame columns
        data_cells_html = "".join([f"<td>{row[i]}</td>" for i in range(len(df.columns))])

        # Create an HTML table row for the current data entry
        row_html = f"<tr>{data_cells_html}</tr>"

        # Append the current row HTML to the body HTML
        body_html += row_html

    # Replace the headers and body placeholders in the HTML template with the generated content
    html_report = html_template.format(headers=headers_html, body=body_html, header_title=header_title)

    # Save report to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_report)

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 4:
        print("Usage: python3 csvToWebpage.py <CSV file path> <Report Title>")
        sys.exit(1)

    csv_file_path = sys.argv[1]  # First argument after the script name
    header_title = sys.argv[2]   # Second argument after the script name
    output_html_file = sys.argv[3] # Third argument after the script name

    # Read the CSV file and generate the HTML report
    #df = read_local_csv("C:\\Users\\keeganu\\Desktop\\TestForm\\Script\\Plateauswdev RUS Rnd 5 BLS.csv")
    df = read_local_csv(csv_file_path)
    generate_html_report(df, output_html_file + ".html", header_title)

    # Save the cleaned DataFrame to a new CSV file
    cleaned_csv_path = output_html_file + ".csv"
    df.to_csv(cleaned_csv_path, index=False, encoding='utf-8')  # Set index=False to avoid saving DataFrame index as a column