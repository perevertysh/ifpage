import requests
import pprint
import re
import os
import argparse


def set_parser():
    parser = argparse.ArgumentParser(description="program for grab files by links from webpage "
                                                 "by default used universal regexp")
    parser.add_argument('--url', type=str,  help='page address')
    parser.add_argument('--pattern', default="", type=str, help='r-string pattern to re.findall()')
    parser.add_argument('--ext', type=str, help='file extension')

    parser.add_argument('--dir_path', type=str, help='path to target directory')
    return parser.parse_args()
def fetch_imgs(dir_path="", ext="", url="", pattern=""):
    if ext:
        pattern = r"[\"(](http[s]?://[^\s]{0,150}." + "{})[\")]".format(ext)

    res = requests.request(url=url,
                           method='GET').content.decode('utf-8')
    pprint.pprint(res)
    links = re.findall(pattern, res)
    counter = 0
    for link in links:
        print(link)
        path = os.path.abspath(os.path.dirname(__file__))
        if dir_path:
            path = dir_path 
        filename = "{}/img{}.{}".format(path, counter, ext)
        os.system("touch {}".format(filename))
        with open(filename, 'wb') as file:
            file.write(requests.request(url=link, method='GET').content)
        counter += 1


def main():
    args = set_parser()
    try:

        fetch_imgs(url=args.url,
                   pattern=args.pattern if args.pattern else None,
                   ext=args.ext,         
                   dir_path=args.dir_path)
        print("params of fetch:")
        [print("{}={}".format(key, value)) for key, value in args.__dict__.items()]
    except requests.exceptions.MissingSchema as e:
        print("Make sure you enter URL!")


if __name__ == '__main__':
    main()
