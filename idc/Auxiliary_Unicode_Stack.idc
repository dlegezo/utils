static ToChars(value) {
    auto Chars = "",
        CurrVal = 0x00;
    CurrVal = value&0xFF;
    if (CurrVal) {
        Chars = Chars + CurrVal;
    }
    CurrVal = value>>16;
    if (CurrVal) {
        Chars = Chars + CurrVal;
    }
    return(Chars);
}

static GetBytes(InstAddr) {
    auto Bytes = "",
        CurrInst = 0;
    CurrInst = decode_insn(InstAddr);
    if (Byte(InstAddr) == 0xC7) {
        Bytes = Bytes + ToChars(CurrInst.Op1.value);
    }
    return(Bytes);
}
    
static main() {
    auto StartAddr = 0x1000A5DE,
        GoogleURL = "",
        Bytes = "",
        InstAddr = StartAddr;
    while (Byte(InstAddr)!=0xE8) {
        Bytes = GetBytes(InstAddr);
        if (Bytes) {
            GoogleURL = GoogleURL + Bytes;
        }
        InstAddr = next_head(InstAddr, InstAddr+0x100);
    }
    print(GoogleURL);
}