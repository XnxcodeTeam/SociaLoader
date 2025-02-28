#!usr/bin/env python3
# Free Tools Media Social Downloader
# Coded by WahyuDin Ambia
# Jum'at, 28 February 2025

# <-- Import Module -->
import requests
import os, time, json, sys, random, base64
from datetime import datetime
from time import sleep, strftime
import threading
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.tree import Tree
from rich import print as cihuy

console = Console()
sys.stdout.write('\x1b]2; SociaLoader | XNXCodeTeam Social Media Downloader \x07')

# <--- Waktu --->
bulan = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10': 'October', '11': 'November', '12': 'December'}
tgl = datetime.now().day
bln = bulan[(str(datetime.now().month))]
thn = datetime.now().year
tanggal = (str(tgl)+' '+str(bln)+' '+str(thn))
waktu = strftime('%H:%M:%S')
hari = datetime.now().strftime("%A")

# <---  Warna  --->

H = "\x1b[38;5;46m"  # Hijau
P = "\x1b[38;5;231m" # Putih
A = "\x1b[38;5;248m" # Abu-Abu


# <!--  Warna 2  -->

A2 = "[#AAAAAA]" # ABU-ABU
M2, H2, K2, P2, B2, U2, O2 = ["[#FF0000]", "[#00FF00]", "[#FFFF00]", "[#FFFFFF]", "[#00C8FF]", "[#AF00FF]", "[#00FFFF]"]
acak = [M2, H2, K2, B2, U2, O2, P2]
warna = random.choice(acak)
til =f"{M2}● {K2}● {H2}●"
ken = f'{M2}›{K2}›{H2}› '
tod = f' {H2}‹{K2}‹{M2}‹'


exec(base64.b64decode(b'QVBJX1VSTCA9ICJodHRwczovL3NvY2lhbC1kb3dubG9hZC1hbGwtaW4tb25lLnAucmFwaWRhcGkuY29tL3YxL3NvY2lhbC9hdXRvbGluayIKQVBJX0tFWSA9ICI5NWZkNjE2NTYxbXNoOThlOTJiZGEwZDc2ZTQwcDE3MGQwNmpzbjYwOGJlYjVlMDhhZiIg'))
LOG_FILE = "download_history.json"

# <!--  Banner  -->
def Banner():
    logo = f"""{til}                                          
     {warna}____   __    ___  __   __   __     __    __   ____  ____  ____ 
    / ___) /  \  / __)(  ) / _\ (  )   /  \  / _\ (    \(  __)(  _ \_
    \___ \(  O )( (__  )( /    \/ (_/\(  O )/    \ ) D ( ) _)  )   /
    (____/ \__/  \___)(__)\_/\_/\____/ \__/ \_/\_/(____/(____)(__\_)
                  {P2}Free Tools Social Media Downloader
"""
    cihuy(Panel(logo, title=f"{ken}{P2}{hari}, {tanggal}{tod}", width=80,style="#AAAAAA"))
    cihuy(Panel(f"{P2}[italic]Tools Ini Dapat Digunakan Untuk Mendownload Media Foto Dan Video Dari Bebagai Platform Seperti {H2}Facebook{P2}, {H2}Instagram{P2}, {H2}Tiktok{P2}, Dll Secara Gratis.\nPastikan Mengunduh Dari Url Yang Bersifat Publik / TIdak Private![/]", title=f"{ken}{P2}Information{tod}", width=80,style="#AAAAAA"))

# <!--  Direct link API  -->
def njikot_source(link_dawg):
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    payload = {"url": link_dawg}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "medias" in data and data["medias"]:
            video_medias = [m for m in data["medias"] if m.get("type") == "video"]
            if not video_medias:
                cihuy(Panel.fit(f"{M2}[italic]Tidak dapat menemukan Video[/]", title=f"{ken}{M2}Error 404{tod}", style="#AAAAAA"))
                return None
            return {
                "platform": data.get("source", "Unknown"),
                "title": data.get("title", "Tidak ada judul"),
                #"caption": data.get("caption", "Tidak ada caption"),
                "link_dawg": video_medias[0]["url"],
                "quality": {m["quality"]: m["url"] for m in video_medias if "quality" in m},
                "is_video": True,
                "size": round(int(video_medias[0].get("size", 0)) / (1024 * 1024), 2) if "size" in video_medias[0] else "Unknown",
                "thumbnail": video_medias[0].get("thumbnail", "Tidak tersedia")
            }
        else:
            cihuy(Panel.fit(f"{M2}[italic]Not Found. Kemungkinan Video bersifat private[/]", title=f"{ken}{M2}Error 404{tod}", style="#AAAAAA"))
            return None
    except requests.exceptions.Timeout:
        cihuy(Panel.fit(f"{M2}[italic]Tidak dapat menemukan Video[/]", style="#AAAAAA"))
    except requests.exceptions.RequestException as e:
        cihuy(Panel.fit(f"{K2}{e}", title=f"{ken}{M2}Error{tod}", style="#AAAAAA"))
    return None

# <!--  Tamilkan Detail Media  -->
def detail_media(media_data):
    angjay = Tree(f"{K2}Detail Media")
    angjay.add(f"{P2}Platform: {H2}{media_data['platform']}")
    angjay.add(f"{P2}Caption: {H2}{media_data['title']}")
    #angjay.add(f"[bold yellow]📝 Caption:[/bold yellow] {media_data['caption']}")
    wahyu = angjay.add(f"{P2}Direct Link")
    wahyu.add(f"{B2}{media_data['link_dawg']}")
    ukuran = angjay.add(f"{P2}Ukuran File:{H2} {media_data['size']}{P2} MB")
    #ukuran.add(f"{media_data['size']} MB")
    tumnai = angjay.add(f"{P2}Thumbnail")
    tumnai.add(f"[blue]{media_data['thumbnail']}[/blue]")
    cihuy(Panel(angjay, title=f"{ken}{B2}Media Info{tod}", expand=False))

# <!--  Pilih resolusi  -->
def resolsi(kualitas_dict):
    if not kualitas_dict:
        cihuy(Panel.fit(f"[italic]{M2}Tidak ada pilihan kualitas, menggunakan default.", style="#AAAAAA"))
        return None
   # res = Panel.fit(f"{P2}Mau Pake Resolusi Apa?", style="#AAAAAA")
    cihuy(Panel.fit(f"{P2}Mau Pake Resolusi Apa?", style="#AAAAAA"))
    print("")
    #kual = Tree(res)
    kualitas_keys = list(kualitas_dict.keys())
    for i, q in enumerate(kualitas_keys):
        #kual = Tree(res)
        cihuy(f"{P2}{i + 1}. {H2}{q}{P2}")
    while True:
        try:
            milih = input(f'{P}╰─> {H}').strip()
            if milih == "":
                return kualitas_dict[kualitas_keys[0]]
            milih = int(milih)
            if 1 <= milih <= len(kualitas_keys):
                return kualitas_dict[kualitas_keys[milih - 1]]
        except ValueError:
            pass
        cihuy(Panel.fit(f"{M2}Pilihan tidak valid, coba lagi", style="#AAAAAA"))
# <!--  Gaskeunn  -->
def main():
    os.system("cls" if os.name == "nt" else "clear")
    Banner()
    cihuy(Panel.fit(f"{P2}Input Folder Tujuan (Kosongkan Untuk '{H2}Downloads{P2}')", subtitle=f"{A2}╭─", subtitle_align="left", style="#AAAAAA"))
    penyimpanan = input(f"{A}   ╰─> {H}").strip()
    if not penyimpanan:
        penyimpanan = os.path.join(os.getcwd(), "Downloads")
    cihuy(Panel.fit(f"{P2}Masukkan URL media", subtitle=f"{A2}╭─", subtitle_align="left", style="#AAAAAA"))
    link_dawg = input(f"{A}   ╰─> {H}{P}").strip()
    if not link_dawg.startswith("http"):
        cihuy(Panel.fit(f"{M2}Invalid Url!", style="#AAAAAA"))
        return
    media_data = njikot_source(link_dawg)
    if media_data:
        detail_media(media_data)  
        link_dawg = resolsi(media_data["quality"]) or media_data["link_dawg"]
        file_name = f"{media_data['platform'].lower()}_{int(time.time())}.mp4"
        download_thread = threading.Thread(target=download_media, args=(link_dawg, file_name, penyimpanan, media_data["platform"]))
        download_thread.start()

# <!--  Donglot Wak  -->
def download_media(link_dawg, file_name, penyimpanan, platform):
    os.makedirs(penyimpanan, exist_ok=True)
    file_path = os.path.join(penyimpanan, file_name)
    response = requests.get(link_dawg, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    size_in_mb = total_size / (1024 * 1024) if total_size > 0 else "Unknown"
    with open(file_path, "wb") as file, Progress(
        SpinnerColumn("dots", style="bold magenta"),
        TextColumn("[bold cyan]{task.fields[filename]}[/bold cyan]"),
        BarColumn(),
        TextColumn("[bold green]{task.percentage:.2f}%[/bold green]"),
        console=console
    ) as progress:
        task = progress.add_task("Download", total=total_size, filename=file_name)
        for chunk in response.iter_content(1024):
            file.write(chunk)
            progress.update(task, advance=len(chunk))
    cihuy(Panel.fit(f"{P2}Download selesai! File disimpan sebagai: {H2}{file_path}", style="#AAAAAA"))

if __name__ == "__main__":
    main()
