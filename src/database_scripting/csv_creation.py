# IMPORTS
import pandas as pd


# GETTING BOOK DATA
txt_filepath = "data/books.txt"
csv_filepath = "data/books.csv"

books_df = pd.read_csv(
    txt_filepath,
    sep="\t",
    header=None,
    names=["wikipedia_id", "Freebase_id", "Book Title", "Book Author", "Publication Date", "Genres", "Summary"],
    index_col=False
)

'''
INPUT:
print("HEAD")
print(books_df.head())
print("INFO")
print(books_df.info())

# we wanna see number of nan values per row
print("DESCRIBE")
print(books_df.describe())
print("NULL VALUES")
print(books_df.isnull().sum())
'''
'''
OUTPUT:
HEAD
   wikipedia_id Freebase_id                                 Book Title      Book Author Publication Date                                             Genres                                            Summary
0           620     /m/0hhy                                Animal Farm    George Orwell       1945-08-17  {"/m/016lj8": "Roman \u00e0 clef", "/m/06nbt":...   Old Major, the old boar on the Manor Farm, ca...
1           843     /m/0k36                         A Clockwork Orange  Anthony Burgess             1962  {"/m/06n90": "Science Fiction", "/m/0l67h": "N...   Alex, a teenager living in near-future Englan...
2           986     /m/0ldx                                 The Plague     Albert Camus             1947  {"/m/02m4t": "Existentialism", "/m/02xlf": "Fi...   The text of The Plague is divided into five p...
3          1756     /m/0sww  An Enquiry Concerning Human Understanding       David Hume              NaN                                                NaN   The argument of the Enquiry proceeds by a ser...
4          2080     /m/0wkt                       A Fire Upon the Deep     Vernor Vinge              NaN  {"/m/03lrw": "Hard science fiction", "/m/06n90...   The novel posits that space around the Milky ...
INFO
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 16559 entries, 0 to 16558
Data columns (total 7 columns):
 #   Column            Non-Null Count  Dtype 
---  ------            --------------  ----- 
 0   wikipedia_id      16559 non-null  int64 
 1   Freebase_id       16559 non-null  object
 2   Book Title        16559 non-null  object
 3   Book Author       14177 non-null  object
 4   Publication Date  10949 non-null  object
 5   Genres            12841 non-null  object
 6   Summary           16559 non-null  object
dtypes: int64(1), object(6)
memory usage: 905.7+ KB
None
DESCRIBE
       wikipedia_id
count  1.655900e+04
mean   1.101506e+07
std    9.537337e+06
min    6.200000e+02
25%    2.913627e+06
50%    7.948709e+06
75%    1.789919e+07
max    3.715950e+07
NULL VALUES
wikipedia_id           0
Freebase_id            0
Book Title             0
Book Author         2382
Publication Date    5610
Genres              3718
Summary                0
dtype: int64
'''
# We have more than enough books to simulate our bookstore so i will be dropping all null values
books_df = books_df.dropna()
# I know there are no duplicated because I have worked on this dataset before

def convert_genres_to_list(genres):
    if isinstance(genres, str):
        genres_dict = eval(genres)
        genres_list = list(genres_dict.values())
        return genres_list
    return None

books_df["Genres"] = books_df["Genres"].apply(convert_genres_to_list)
# We don't need wikipedia_id or freebase_id, but I might keep wiki id for some future fun stuff
books_df.drop(columns=["Freebase_id"], inplace=True)
books_df.to_csv(csv_filepath, index=False)







