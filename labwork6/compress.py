import zlib

def compress(input_files, dest_file):
    """Compress files
    
    Parameters
    ----------
    input_files : list of input files src
    dest_file : destination of file src
    """
    input_data = b""
    for file_src in input_files:

        file = open(file_src, "rb")
        input_data += bytes(file.name, "utf-8")
        input_data += b"__FILECONTENT__"
        input_data += file.read()
        input_data += b"__FILEEND__"
        file.close()

    compressed_data = zlib.compress(input_data, zlib.Z_BEST_COMPRESSION)

    with open(dest_file, "wb") as f:
        f.write(compressed_data)

def decompress(compressed_file):
    """Decompress a file
    
    Parameters
    ----------
    compressed_file : compressed file src
    """
    f = open(compressed_file, "rb")
    compressed_data = f.read()
    f.close()
    decompressed_data = zlib.decompress(compressed_data)
    decompressed_files = decompressed_data.split(b"__FILEEND__")[:-1]
    for decompressed_file in decompressed_files:
        file_name, file_content = decompressed_file.split(b"__FILECONTENT__")
        with open(file_name.decode("utf-8"), "wb") as write_file:
            write_file.write(file_content)
        

