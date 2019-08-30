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
    parser.add_argument('--dir_name', default="samples", type=str, help='target dir name')
    parser.add_argument('--dir_path', type=str, help='path to target directory')
    return parser.parse_args()


def fetch_imgs(dir_name="", ext="", url="", pattern=""):
    if ext:
        pattern = r"[\"(](http[s]?://[^\s]{0,150}." + "{})[\")]".format(ext)

    res = requests.request(url=url,
                           method='GET').content.decode('utf-8')
    pprint.pprint(res)
    links = re.findall(pattern, res)
    os.system("mkdir {}".format(dir_name))
    os.system("chmod 777 {}".format(dir_name))
    counter = 0
    for link in links:
        print(link)
        if dir_path:
            path = dir_path
        else:
            path = os.path.abspath("".join(os.path.dirname(__file__).split("/")[0:-2]))
        filename = "{}{}img{}.{}".format(path, "/" + dir_name + "/" if dir_name else "", counter, ext)
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
                   dir_name=args.dir_name,
                   dir_path=args.dir_path)
        print("params of fetch:")
        [print("{}={}".format(key, value)) for key, value in args.__dict__.items()]
    except requests.exceptions.MissingSchema as e:
        print("Make sure you enter URL!")


if __name__ == '__main__':
    main()
