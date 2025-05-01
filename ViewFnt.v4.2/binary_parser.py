#binary_parser.py
import struct  
from character import FontCharacter  

def parse_binary_fnt(filename, chars, pages):  
    with open(filename, "rb") as f:  
        header = f.read(4)  
        if header != b"BMF\x03":  
            raise ValueError("این فایل باینری معتبر نیست یا نسخه پشتیبانی نشده")  
        while True:  
            block_id_b = f.read(1)  
            if not block_id_b:  
                break  
            block_id = block_id_b[0]  
            block_size = struct.unpack("<I", f.read(4))[0]  
            block_data = f.read(block_size)  

            if block_id == 1:  # info block (می‌توان نادیده گرفت یا ذخیره کرد)  
                continue  
            
            elif block_id == 2:  # common block (می‌توانید فقط بررسی کنید)  
                # می‌توان اینجا بررسی بخشی داشت یا ذخیره کرد  
                continue  
            
            elif block_id == 3:  # pages block  
                # چند نام صفحه null-terminated که کنار هم ذخیره شدند  
                page_names = []  
                start = 0  
                for i in range(block_size):  
                    if block_data[i] == 0:  
                        name = block_data[start:i].decode("windows-1252")  
                        page_names.append(name)  
                        start = i + 1  
                for i, name in enumerate(page_names):  
                    pages[i] = name  
            
            elif block_id == 4:  # chars block  
                # ساختار هر کاراکتر 20 بایت است:  
                # id:uint32 x:uint16 y:uint16 width:uint16 height:uint16 xoffset:int16 yoffset:int16 xadvance:uint16 page:uint8 chnl:uint8  
                char_struct_fmt = "<IHHHHhhHBB"  
                char_size = struct.calcsize(char_struct_fmt)  
                count = block_size // char_size  
                for i in range(count):  
                    offset = i * char_size  
                    entry = block_data[offset:offset + char_size]  
                    unpacked = struct.unpack(char_struct_fmt, entry)  
                    c = FontCharacter(  
                        id=unpacked[0],  
                        x=unpacked[1],  
                        y=unpacked[2],  
                        width=unpacked[3],  
                        height=unpacked[4],  
                        xoffset=unpacked[5],  
                        yoffset=unpacked[6],  
                        xadvance=unpacked[7],  
                        page=unpacked[8],  
                    )  
                    chars[c.id] = c  
            else:  
                # بلوک های دیگر (kerning و ...)  
                continue