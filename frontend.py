#note: need to run this in command prompt with the line: streamlit run frontend.py 
#The server will show an error but that is because the default value of the threshold shares and no of shares being 0
#Also edit the os.path.join to choose where one is reading the file
#currently hosted on a local serve
#By Veda D
import streamlit as st
import os
import filecmp
from main import shortshare
from main import reconstructshortshare
line = []
minimum_shares = 1
no_shares = 2

st.write("For now the files are only being taken in are text")
uploaded_file = st.file_uploader("Please upload file")
if uploaded_file is not None:
    file = open(os.path.join(r"C:\Users\vitru\OneDrive\Documents",uploaded_file.name),"r+")
    line =  file.readlines()

f = open("test.txt", "w")
for i in range(len(line)):
    f.write(line[i])
f.close()
minimum_shares = st.number_input("Please enter threshold number of shares", step=1)
no_shares = st.number_input("Please enter number of shares", step=1)



file = "test.txt"
combined_files = shortshare(file,minimum_shares,no_shares)
st.write("Encrypted file:")
f = open("encrypted.txt", "r+")
line =  f.readlines()
for i in range(len(line)):
    w = st.write(line[i])
f.close()
st.write("These are the shares, copy and save it")
for i in range(len(combined_files)):
    st.write(str(combined_files[i]))
    st.download_button('Download share'+str(i), str(combined_files[i]))
st.write()
st.write("For ease of simplicity, we are for now assuming you have given the requires shares")
file1  = reconstructshortshare(combined_files,minimum_shares)
st.write("Was this the file you uploaded?")
f = open(file1, "r+")
line =  f.readlines()
for i in range(len(line)):
    w = st.write(line[i])
f.close()
result = filecmp.cmp(file, file1)
st.write("We think so. The diagnostic test says we're",result)




