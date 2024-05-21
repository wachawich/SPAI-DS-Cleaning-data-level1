import pandas as pd
import regex as re

def remove_spaces(string):
    if string == '':
        return ''
    elif string == ' ':
        return ''
    if string[0] == ' ':
        string = string[1:]
    if string[-1] == ' ':
        string = string[:-1]
    return string


def check_space(string):
  count = 0
  for i in string:
    if i == ' ':
      count += 1
  if count > 2 or len(string) <= 3:
    return ''
  else : return string


def format_name(string):
    name_parts = string.split()
    corrected_name = ' '.join([part.capitalize() for part in name_parts])
    return corrected_name

def remove_digit(string):
    if string and string[-1].isdigit():
        string = string[:-1]
    return string

def have_alpha(string):
  count = 0
  other_count = 0
  for i in string:
    if all(ord(c) < 128 for c in i) and i != ' ':
      count += 1
    else : other_count += 1
  if count > 2 and other_count > 4:
    return True
  else : return False

def dispart_name(string):
    
    string = string.replace('[', '').replace(']', '')
    string = string.replace('(', '').replace(')', '')

    thai_name = ''
    eng_name = ''
    parts = string.split()
    for part in parts:
        if all(ord(c) < 128 for c in part):
            eng_name += part + ' '
        else:
            thai_name += part + ' '
    return thai_name.strip(), eng_name.strip()

def delete_dash(string):
  count = 0
  j = 0
  dash = 0
  for i in string:
    if i == ' ':
      count = 1
    if count == 1:
      j += 1
    if i == '-':
      dash += 1
  if j <= 2 or dash >= 1:
    return string.replace(' -', '').replace('.','')
  else : return string.replace(' - ', ' ').replace(' 1 ', ' ')


def delete_title(string):
    
    #list คำนำหน้าต่างๆที่พบไว้
    name_titles = ["Dr." , "Mr.", "M.r.","M.r. " ,"Ms.", "รศ.", "นาย", "นาง", "ดร.", "นางสาว", 
                   "พระครู", "พระมหา", "พระปลัด" ,"พระ", "Phrakru","Phra","ผู้ช่วยศาสตราจารย์","รองศาสตราจารย์" , 
                   "และคณะ", "ว่าที่ร้อยตรี" , "ผศ.", ":", "Assoc.prof.dr." ,"อาจารย์" , "พันเอกหญิง", "พันเอก", 
                   "M.I." , "อ.", "กสทช." , "Authors :", "Author :","Authors","Author"]


    delete_list = ["บรรณาธิการ","ผู้ทรงคุณวุฒิ","วิทยาลัย","แนะนำ","และหีม","วารสาร","เจ้าหน้าที่","สำนักส่งเสริม",
                   "Cover Vol.12","ศูนย์บริการ","About","@","Editorial","สารบัญ"]

    if '*' in string:
      string = string.replace('*', '')
    
    for del_word in delete_list:
      if del_word in string:
        return ''
    
    for title in name_titles:
        string = string.replace(title, "")
        
    return string

if __name__ == '__main__':
    char = {'id': [], 'name': []}
    df = pd.read_csv('/kaggle/input/thaijo-researcher-for-code-submission/test.csv')
    df = df.fillna('')
    
    for idx, row in df.iterrows():
        
        names = []
        char['id'].extend([f"{row['_id']}_{i+1}" for i in range(10)])
        co_author = row['_source.co-author']
        
        if co_author != '':
            ca = co_author.split(',')
            for c in ca:
                if have_alpha(c):
                  #เราจะลบแค่ประโยคที่มีภาษาอังกฤษ เพราะว่า ภาษาไทยไม่จำเป็นต้องลบ เนื่องจากมีแค่ () ตามหลังชื่อพระ
                  c = delete_title(c) 
                    
                  x = dispart_name(c)
                  if x[0] != '': names.append(x[0])
                  if x[1] != '': names.append(x[1])
                    
                elif c not in names:
                  names.append(c)
                
        if len(names) == 0:
            char['name'].extend([None]*10)
            continue

        processors = [remove_spaces, delete_dash, delete_title, check_space, format_name, remove_digit]
        for processor in processors:
            names = [processor(name) for name in names]


        if len(names) > 10:
            names = names[:10]
        elif len(names) < 10:
            names.extend(['']*(10-len(names)))
            
        char['name'].extend(names)
        
    char = pd.DataFrame(char)
    char.to_csv('submission.csv', index=False)