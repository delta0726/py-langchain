def decrypt_caesar_cipher(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # 文字がアルファベットの場合のみ処理を行う
            if char.islower():
                # 小文字の場合
                decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            else:
                # 大文字の場合
                decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            plaintext += decrypted_char
        else:
            # アルファベット以外の文字はそのまま追加
            plaintext += char
    return plaintext

# 暗号文とシフト数の推定
def estimate_caesar_shift(ciphertext):
    # アルファベットの出現頻度を計算
    frequency = {}
    for char in ciphertext:
        if char.isalpha():
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
    
    # 最も頻出するアルファベットを'e'と仮定してシフト数を計算
    most_common = max(frequency, key=frequency.get)
    shift = (ord(most_common) - ord('e')) % 26
    return shift

# 暗号文を入力として受け取り、シフト数を推定し、解読する
ciphertext = '''Ulaly sld l aczgpcm esle dljd, "Pgpy l ozr htww cfy tyez l detnv hspy te hlwvd." Te txawtpd esle hspy jzf elvp lnetzy, jzf xtrse pynzfyepc yze zywj rzzo zfenzxpd mfe lwdz mlo zypd zc fypiapnepo pgpyed. Dapntqtnlwwj, hspy jzf ecj dzxpestyr yph zc mpslgp otqqpcpyewj esly fdflw, jzf xtrse piapctpynp yze zywj azdtetgp cpdfwed zc zaazcefytetpd mfe lwdz aczmwpxd, nslwwpyrpd, zc nctetntdxd.'''
shift = estimate_caesar_shift(ciphertext)
decrypted_text = decrypt_caesar_cipher(ciphertext, shift)
print("解読結果:")
print(decrypted_text)
