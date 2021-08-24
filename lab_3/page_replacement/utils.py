import pandas as pd

def check_reference_avaibility(df:pd.DataFrame, page_reference:str) -> int:
    for i, F in df.iterrows():
        if F["Frame"] == page_reference:
            return F["Status"]
    return None

def free_frame(df:pd.DataFrame) -> int:
    for i, F in df.iterrows():
        if F["Status"] == -1:
            return i
    return None

def get_frame_list(df:pd.DataFrame) -> list:
    frame = list(df["Frame"])
    for i in range(len(frame)):
        if  frame[i] == None:
            frame[i] = ''   
    return frame