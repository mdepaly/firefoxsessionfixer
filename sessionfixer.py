import lz4.frame
import json
import argparse


def repack_session_restore(filename):
    with open(filename, "rb") as in_file:
        buffer = in_file.read()
        in_file.close()

        # we use lz4.frame for decompression to avoid memory issues with large sessions
        buffer = bytearray(lz4.frame.decompress(buffer[8:]))

        content = json.loads(buffer)

        # handle failed session restore states
        try:
            content = content["windows"][0]["tabs"][0]["formdata"]["id"]["sessionData2"]
        except KeyError:
            pass

        buffer = json.dumps(content).encode()

        result = lz4.frame.compress(buffer)
        with open(filename + ".rep", "wb") as out_file:
            out_file.write(b"mozLz40\0"+result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Fixer for broken Firefox session restore points")
    parser.add_argument('filename', nargs='?', help="session file to be fixed",
                        default="sessionstore.jsonlz4", type=str)
    args = parser.parse_args()

    repack_session_restore(args.filename)
