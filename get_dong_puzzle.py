import os
import re
import requests
from time import sleep
import datetime
from datetime import datetime, time
import pandas as pd
from wechatarticles import PublicAccountsWeb


def get_dong_article(cookie, token, nickname="咚咚谜"):
    paw = PublicAccountsWeb(cookie=cookie, token=token)
    article_data = paw.get_urls(nickname, begin="0", count="5")
    d = {'update_time': [str(datetime.fromtimestamp(article_data[0]['update_time']))], 
        'title': [article_data[0]['title']], 
        'link': [article_data[0]['link']]}
    return pd.DataFrame(d)


def check_new_article(df, file_path):
    local_df = pd.read_csv(file_path)
    if local_df.iloc[0, 1] == df.iloc[0, 1]:
        return False # not new
    else:
        return True # new article
    

def save_article(df, file_path):
    new_df = pd.concat([df, pd.read_csv(file_path)])
    new_df.to_csv(file_path, index=False)


def get_image_url(url):
    response = requests.get(url)
    sleep(3)
    pattern = r'<img[^>]*class="rich_pages wxw-img js_insertlocalimg"[^>]*data-src="([^"]+)"'
    match = re.search(pattern, response.text)
    return match.group(1)


def get_dong_puzzle():
    cookie = "noticeLoginFlag=1; remember_acct=biancochiu%40outlook.com; pgv_pvid=3271664380; _qimei_uuid42=1831a0e1a11100f1fe93e0b6bbef68f99377e3aee8; _qimei_q36=; _qimei_h38=3ee1864efe93e0b6bbef68f90300000fe1831a; RK=dN8BqT2mxt; ptcz=9061404304cb6071def1d2a4f25432c4f16dab8c288a4d878abccccc2a08fa5f; rewardsn=; wxtokenkey=777; mail5k=a1f2dee5; fqm_pvqid=017de1d4-cdc4-4ad8-9dcd-eb658292a600; fqm_sessionid=cdeea11e-c533-4486-b3d5-a23c88b61d9a; pgv_info=ssid=s3838081076; tmeLoginType=2; psrf_access_token_expiresAt=1727682802; euin=owSqoKSs7KolNn**; qq_domain_video_guid_verify=fbbcd3ef0c2cc1cb; vversion_name=8.2.95; video_omgid=fbbcd3ef0c2cc1cb; _qimei_fingerprint=7ec1d02401894c3395acececf244ce60; o_cookie=2791765378; pac_uid=0_FM6Ma7kKRAiKS; poc_sid=HOntumajrY-wQE9fkk_U2OGDWEOV6v3i3xVg3IIP; ua_id=sd1xts83Q4qGFN2bAAAAAONyBxZHDMI-XDNwY3-a0-Q=; wxuin=23549449344505; cert=gQOAiRwdJg4zlzHnM3JOxcZbIZ8g9YVY; sig=h01582458ddd04a846aff161b927944495809411530fbcd46a30f7cec0be4fbe1c7fca9485106db5b75; pvpqqcomrouteLine=herodetail; eas_sid=s1A772G3x7n0b327V0J959C1b5; mm_lang=zh_CN; _clck=kju24n|1|foh|0; uuid=3a9126f844e49e0f3a368d43cfc772e3; bizuin=3926744197; ticket=8a80f645e0db2ae017a84a47008437746fa75d65; ticket_id=gh_7aea65737913; slave_bizuin=3926744197; rand_info=CAESIJLtb73z5/kR3w0ORdCJhPg71ihdsvxlPEOWodbeTR8N; data_bizuin=3926744197; data_ticket=xb+pZ3saeTDwm8aQIsAgFHDs7CoC1M2/0bap2Bc+RJthJjH8qSx0kX575tL6m8tc; slave_sid=OFd2cUl2Qktxdm56NTI5Z0UzZDlxYmVJNTM0Uk5DVmVVdnBVMllVQ1pBRUxaTGJCVk1OQzRCczNFeElXMGl0U05NR2t0dTk3MkRTbEoxUUFaRUl2blUwbjBEaTlidDNmNnlSYlJGbEVyQzJhWGxBZ09scEx4Zjc5ZzBRV0lGVVNCTzhhUnFCMnNySk1HekxE; slave_user=gh_7aea65737913; xid=649fca5279cd69851558a35601ec32cc; openid2ticket_ohVwN6huup8Wp6SkQthOfO-liilA=weWyAgFCjACoMFhdNq1duHQUnRpZIozUhqBkZ1y75+A=; _clsk=slr7qn|1724163860853|9|1|mp.weixin.qq.com/weheat-agent/payload/record"
    token = "600595438"
    # nickname = "咚咚谜"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "dong_puzzle.csv")

    now = datetime.now().time()
    start_time = time(10, 59)
    end_time = time(23, 5)
    
    while start_time <= now <= end_time:
        latest_article = get_dong_article(cookie, token)
        if check_new_article(latest_article, file_path):
            save_article(latest_article, file_path)
            # date, title, link
            return latest_article.iloc[0, 0][:10], latest_article.iloc[0, 1], get_image_url(latest_article.iloc[0, 2])
        
        else:
            sleep(5)
        now = datetime.now().time()
    return 
