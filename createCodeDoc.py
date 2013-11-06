#!/usr/bin/env python

import os
import fnmatch
import subprocess

def convertToLatex(markdownFile):
    """
    Converts a markdown file to latex
    """
    drive, path = os.path.splitdrive(markdownFile)
    path, filename = os.path.split(path)
    filename, ext = os.splitext(filename)
    outFile = os.path.join(path,filename+'.tex')
    print 'In file: {} outfile: {}'.format(markdownFile,outFile)
    cmd = 'pandoc -f markdown -t latex {} > {}'.format(markdownFile,outFile)
    #subprocess.call(cmd,shell=True)

def getAllFiles(directory):
    file_paths = list()
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    print file_paths
    return file_paths       

def getListOfFiles(directory):
    matches = list()
    files = getAllFiles(directory)
    for f in files:
        if f.endswith('.md'):
            matches.append(f)
    return matches
        
if __name__ == '__main__':
    files = getListOfFiles('/Users/murffer/Documents/Dissertation/code')
    print files
    for f in files:
        convertToLatex(f)