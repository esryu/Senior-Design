import mostSig

if __name__ == "__main__":
    inputDir = sys.argv[1]
    outdir = sys.argv[2]
    files = findFiles(inputDir)
    for file in files:
        fileName = getFileName(file)
        header, up,down = parseGeneExp(file)
        outputTop(outdir,fileName,up,down,header)
