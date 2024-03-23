import os
import pandas as pd


def search_and_replace(directory, df):
    output_data = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".md"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                for index, duplicate in df.iterrows():
                    if duplicate['Original'] in content:
                        output_data.append([duplicate['Duplicate'], duplicate['Original'], file_path])

                print(f'# {file_name} is checked')

    print("Last Checked Directory ", root)
    headers = ['Original', 'Duplicate', 'file_name']
    output_df = pd.DataFrame(output_data, columns=headers)
    output_file = 'ToBeReplacedWithOriginal.csv'
    output_df.to_csv(output_file, index=False)


def select_directory(df):
    # print(df)
    #root = tk.Tk()
    #root.withdraw()
    #directory = filedialog.askdirectory(title="Select Directory")
    directory =os.getcwd()

    if directory:
        search_and_replace(directory, df)


if __name__ == "__main__":
    # url = "https://raw.githubusercontent.com/PasinduJayalal/images/duplicate_image_identifier_test/DuplicateImages.csv"
    try:
        # response = requests.get(url)
        # response.raise_for_status()
        # df = pd.read_csv(StringIO(response.text))
        # file = filedialog.askopenfile(title="Select Directory")
        df = pd.read_csv("C:\\Users\\dhpas\\Downloads\\DuplicateImages.csv")
        select_directory(df)
    except Exception as e:
        print(f"An error occurred: {e}")
