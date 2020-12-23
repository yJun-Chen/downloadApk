import requests
import re


class DownloadApk:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    def log(self,log):
        print(log)
        with open("./log.txt","a+") as f:
            f.write(log+"\n")

    def request_web(self, url):
        # request web resource
        try:
            return requests.get(url=url, headers=self.headers)
        except Exception as e:
            print(e)
            self.log(str(e))
            return None

    def download_software(self,software_name, save_dir):
        save_path = save_dir + "/"+software_name + '.apk'
        software_url = self.search_software_url(software_name)
        print(software_url)
        # if not software_url:return
        # # request software resource
        # response = self.request_web(software_url)
        # # save software to file
        # try:
        #     with open(save_path, mode='wb+') as f:
        #         f.write(response.content)
        #     print("download {} success".format(software_name))
        # except Exception as e:
        #     print(e)
        #     print("download {} failed".format(software_name))

    def search_software_url(self, software_name):
        url = 'https://sj.qq.com/myapp/searchAjax.htm?kw={}'.format(software_name)

        response = self.request_web(url)
        software_url = self.parse_download_url(response,software_name)
        if not software_url:
            self.log("{} doesn't exist".format(software_name))
            return None
        return software_url

    @staticmethod
    def parse_download_url(response,software_name):
        urls = re.findall(r'"apkUrl":"(.*?)","appDownCount":.*?,"appId":.*?,"appName":"{}"'.format(software_name), response.text)
        if len(urls) > 0: return urls[0]
        return None

    @staticmethod
    def read_txt(file_path):
        with open(file_path, "r") as f:
            software_list = f.read()
        return software_list.split('\n')

    @staticmethod
    def read_excel(file_path):
        import pandas
        data = pandas.read_excel(file_path)
        columns = data.columns.values[0]
        return data[columns].values

    def read_file(self, file_path):
        file_type_dict = {
            'txt': 'txt',
            'xlsx': 'excel',
            'xls': 'excel'
        }

        suffix = file_path.split('.')[-1]
        if file_type_dict.get(suffix):
            file_type = file_type_dict.get(suffix)
        else:
            return "Unsupported file types"

        if file_type == 'txt':
            return self.read_txt(file_path)
        else:
            return self.read_excel(file_path)

if __name__ == '__main__':
    import sys
    import os
    download = DownloadApk()
    file_path = None
    save_software_dir = None

    if len(sys.argv)>1 : file_path = sys.argv[1]
    else:
        print("Missing input file parameters ")
        sys.exit()

    if len(sys.argv)>2 :
        save_software_dir = sys.argv[2]
        if not os.path.exists(save_software_dir):os.mkdir(save_software_dir)
    else:
        save_software_dir = "./"

    software_list = download.read_file(file_path)
    print("read file success")


    for software_name in software_list:
        download.download_software(str(software_name),save_software_dir)
