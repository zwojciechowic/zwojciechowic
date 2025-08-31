import re
def shift_srt_file(path):
    with open(path,encoding="utf-8") as f: text=f.read()
    def shift(m):
        h,mn,s,ms=map(int,(m.group(1),m.group(2),m.group(3),m.group(4)))
        total=h*3600+mn*60+s+60
        if total<0: total=0
        nh=total//3600; nm=(total%3600)//60; ns=total%60
        return f"{nh:02d}:{nm:02d}:{ns:02d},{ms:03d}"
    fixed=re.sub(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})',shift,text)
    with open(path,"w",encoding="utf-8") as f: f.write(fixed)
shift_srt_file("/Users/tmczs/Downloads/termi/tt1340138-pl.srt")
