with open('itay.txt', 'w') as f:
    f.write('1+1=11')

# Verify the file was created and show its contents
with open('itay.txt', 'r') as f:
    print("File contents:", repr(f.read()))
