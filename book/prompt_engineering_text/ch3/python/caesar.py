def caesar_cipher(text, shift):
    encrypted_text = ""
    
    for char in text:
        # 文字がアルファベットの場合のみ暗号化を行います
        if char.isalpha():
            # 文字が大文字か小文字かを確認し、アルファベットの範囲内でシフトします
            if char.isupper():
                encrypted_char = chr(((ord(char) - 65 + shift) % 26) + 65)
            else:
                encrypted_char = chr(((ord(char) - 97 + shift) % 26) + 97)
        else:
            # アルファベットでない文字は変更せずにそのまま追加します
            encrypted_char = char
        
        encrypted_text += encrypted_char
    
    return encrypted_text

# テスト用の文字列とシフト値を設定します
text = "Hello, World!"
shift = 3

# テキストをシーザー暗号で暗号化します
encrypted_text = caesar_cipher(text, shift)

print("暗号化された文字列:", encrypted_text)

