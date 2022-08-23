import subprocess
import shutil
import sys
import os

fileName = sys.argv[1]

with open(fileName) as inFile:
    inFile = inFile.read().splitlines()

res = []
for line in inFile:
    if line.strip():
        res.append(line.strip())
inFile = res

newFile = []
newFile.append(f'package {inFile[0].split(" ")[1]}')

for line in inFile:
    if line.startswith('print'):
        newFile.append(f'import "fmt"')
        break

newFile.append('func main() {')

variables = []
for line in inFile:
    if line.startswith('integer') or line.startswith('character') or line.startswith('real') or line.startswith('complex') or line.startswith('logical'):
        if line.startswith('character'):
            if line[line.find('(')+1:line.find(')')] == 'len=*':
                newFile.append(f'\tvar {line.split(" ")[3]} string ={line.split("=")[-1]}')
                variables.append(line.split(" ")[3])
            else:
                newFile.append(f'\tvar {line.split(" ")[2]} string ={line.split("=")[-1]}')
                variables.append(line.split(' ')[2])
        elif line.startswith('integer'):
            newFile.append(f'\tvar {line.split(" ")[1]} int')
            variables.append(line.split(' ')[1])
    elif line.startswith('print'):
        newFile.append(f'\tfmt.Println({line.split(",")[1].strip()})')
    elif line.split('=')[0].strip() in variables:
        newFile.append(f'\t{line}')
        
newFile.append('}')

res = []
for line in newFile:
    res.append(f'{line}\n')
newFile = res

if os.path.exists('output'):
    shutil.rmtree('output')
os.mkdir('output')

subprocess.Popen(['go', 'mod', 'init', fileName.split('.')[0]], cwd=os.getcwd()+'/output').wait()

with open('output/output.go', 'w+') as output:
    output.write("\n".join(newFile))

# subprocess.Popen(['go', 'run', '.'], cwd=os.getcwd()+'/output').wait()