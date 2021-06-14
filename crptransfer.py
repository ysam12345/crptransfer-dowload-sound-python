import requests
import re
import urllib.request
import os
from tqdm import tqdm


OUTPUT_FOLDER = "output"


def download_file(url:str, save_filename:str) -> True:
    try:
        os.listdir(OUTPUT_FOLDER)
    except FileNotFoundError:
        os.mkdir(OUTPUT_FOLDER)
    with urllib.request.urlopen(url) as response, open(os.path.join(OUTPUT_FOLDER, save_filename), 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    return True

def transfer(text: str, show_tone_notation: bool = True) -> bool:
    # show tone notation: sound = 1,
    # don't show tone notation: sound = 2
    response = requests.get(
        url=f"https://crptransfer.moe.gov.tw/index.jsp?SN={text}&sound={int(show_tone_notation)+1}")
    sound_id = int(re.search("getSound.jsp\\?ID=(\d+)", response.text).group(1))
    # 0 indicate there's no sound file for this text
    if sound_id == 0:
        return False
    else:
        download_file(f"https://crptransfer.moe.gov.tw/getSound.jsp?ID={sound_id}", f"{text}.wav")
        return True

def main():
    words = ["今天","天氣","很好"]
    t_words = tqdm(words)
    has_sound_count = 0
    for idx, word in enumerate(t_words):
        if transfer(word):
            has_sound_count += 1
        t_words.set_description(f"total:{has_sound_count}/{idx+1}, rate:{has_sound_count/(idx+1):.2f}")

if __name__ == "__main__":
    main()
