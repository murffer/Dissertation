#!/usr/bin/env python

import os
import subprocess
import glob

def convertToLatex(markdownFile):
    """
    Converts a markdown file to latex
    """
    drive, path = os.path.splitdrive(markdownFile)
    path, filename = os.path.split(path)
    filename, ext = os.path.splitext(filename)
    outDir = 'doc/'
    outFile = os.path.join(outDir+os.path.basename(path)+'.tex')
    cmd = 'pandoc -f markdown -t latex {} > {}'.format(markdownFile,outFile)
    subprocess.call(cmd,shell=True)
    lines = list()
    with open(outFile,'r') as fin:
        lines = fin.readlines()
    firstSection = True
    with open(outFile,'w') as out:
        for line in lines:
            if 'label' in line:
                if firstSection:
                    tokens = line.split('\label{')
                    line = tokens[0]+'\n\\label{sec:'+tokens[1]
                    firstSection = False
                else:
                    line = line.split('\label')[0]
            out.write(line)
#        out.write('\label{{sec:{}}}'.format(os.path.basename(path)))
#        out.write(createListingsString(path))
    return os.path.basename(path)

def getAllFiles(directory):
    """
    Gets all of the files (recursivley) in a directory
    """
    file_paths = list()
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths       

def getSourceFiles(path):
    """
    Gets the source, header, macros and run files of a directory
    """
    matches = set()
    print 'The source files path is '+str(path)
    files = getAllFiles(path)
    print 'The files found are:'
    print files
    for f in files:
        if f.endswith(('.mac','.py','.cc','.hh','.mcnp')):
            matches.add(f)
    print matches
    return matches
    
def createListingsString(path):
    srcs = getSourceFiles(path)
    fmtString = '\lstinputlisting[language={}]{{{}}}\n'
    s = ''
    for src in srcs:
        if src.endswith('.py'):
            language='Python'
        elif src.endswith(('.cc','.hh')):
            language='C++'
        else:
            language='bash'
        s += fmtString.format(language,src)
    return s
            

def getListOfFiles(directory):
    matches = list()
    files = getAllFiles(directory)
    for f in files:
        if f.endswith('.md'):
            matches.append(f)
    return matches

def sanitize(path):
    """
    Cleans up all of the latex documents in path

    Currently just cleans up the figures and makes the verbatim tiny
    """
    files = glob.glob(path+'/*.tex')
    for fname in files:
        # Cleaning up
        with open(fname,'r') as fin, open('temp','w') as fout:
            for line in fin:
                # Verbatim enviorments
                if line.startswith('\\begin{verbatim}'):
                    fout.write('{\\small')
                    fout.write(line)
                elif line.startswith('\\end{verbatim}'):
                    fout.write(line)
                    fout.write('}')
                # Figures
                elif 'includegraphics' in line:
                    line,graphics = line.split('\includegraphics')
                    fout.write(line)
                    fout.write('\n\\begin{figure}\n')
                    fout.write('\\includegraphics[width=\\textwidth]'+graphics)
                    fout.write('\\end{figure}\n')
                # Business as normal
                else:
                    fout.write(line)
        # Renaming
        os.rename('temp',fname)

if __name__ == '__main__':
    files = getListOfFiles('code')
    toWrite = set()
    for f in files:
        flatex = convertToLatex(f)
        toWrite.add(flatex)
    with open('doc/CodeDoc.tex','w') as out:
        for f in toWrite:
            out.write('\input{doc/'+f+'}\n')
    sanitize('doc')
