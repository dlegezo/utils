#include <idc.idc>

static locateResolver() {
        auto    addrStartVA = 0x401000,
                addrLoadLibrary = 0x00,
                addrResolverFunc = 0x00;                
        addrLoadLibrary = find_text(addrStartVA, SEARCH_DOWN, 0, 0, "LoadLibrary");
        addrResolverFunc = get_next_func(addrLoadLibrary);
        addrResolverFunc = get_prev_func(addrResolverFunc);
        set_name(addrResolverFunc, "Resolver");
        return addrResolverFunc;
}

static getStrTillZero(addrStrStart) {
        auto    strServerAPIFunc = "",
                curr = 0;                
        while (byte(addrStrStart+curr) != 0) {
                strServerAPIFunc = strServerAPIFunc + byte(addrStrStart+curr);
                curr = curr + 1;
        }        
        return strServerAPIFunc;
}

static renameMovArg(addrInsn, strName) {
        auto    Insn = 0x00,
                addrToRename = 0x00;        
        Insn = decode_insn(addrInsn);
        addrToRename = Insn.Op0.addr;
        set_name(addrToRename, strName);        
        return addrToRename;
}

static renameServerAPIName(addrResolverStart, addrResolverEnd) {
        auto    addrServerAPIName = 0x00,
                strServerAPIName = "",
                addrGPA = 0x00,
                addrMovServerAPIName = 0x00,
                addrInsnCurrent = addrResolverStart,
                insnCurrent = 0x00;                
        while (addrInsnCurrent < addrResolverEnd) {
                addrGPA = find_text(addrInsnCurrent, SEARCH_DOWN, 0, 0, "GetProcAddress");
                insnCurrent = decode_insn(addrGPA);
                while (insnCurrent.mnem != "call") {
                        addrInsnCurrent = addrInsnCurrent + insnCurrent.size;
                        addrGPA = find_text(addrInsnCurrent, SEARCH_DOWN, 0, 0, "GetProcAddress");
                        insnCurrent = decode_insn(addrGPA);
                }
                addrInsnCurrent = addrInsnCurrent + insnCurrent.size;
                addrServerAPIName = prev_head(addrGPA, addrResolverStart);
                addrServerAPIName = prev_head(addrServerAPIName, addrResolverStart);
                insnCurrent = decode_insn(addrServerAPIName);
                addrServerAPIName = insnCurrent.Op0.value;
                strServerAPIName = getStrTillZero(addrServerAPIName);
                addrMovServerAPIName = next_head(addrGPA, addrResolverEnd);
                renameMovArg(addrMovServerAPIName, strServerAPIName);
        }
        
}

static main() {
    auto        addrResolverStart = 0x00,
                addrResolverEnd = 0x00,
                addrServerAPIName = 0x00;                
        addrResolverStart = locateResolver();
        addrResolverEnd = find_func_end(addrResolverStart);
        renameServerAPIName(addrResolverStart, addrResolverEnd);
}


