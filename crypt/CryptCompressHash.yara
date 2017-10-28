// Denis Legezo, Kaspersky Lab, 2017

rule Crypt_Blowfish {
	strings:
		$BlowfishPBoxInt = { 24 00 00 00 3F 00 00 00 6A 00 00 00 88 00 00 00 85 00 00 00 A3 00 00 00 08 00 00 00 D3 00 00 00 13 00 00 00 }
		$BlowfishPBoxShort = { 24 00 3F 00 6A 00 88 00 85 00 A3 00 08 00 D3 00 13 00 19 00 8A 00 2E 00 03 00 70 00 73 00 44 00 }
		$BlowfishPBoxByte = { 24 3F 6A 88 85 A3 08 D3 13 19 8A 2E 03 70 73 44 A4 09 38 22 29 9F 31 D0 08 2E FA 98 EC 4E 6C 89 }
		$BlowfishSBoxInt = { D1 00 00 00 31 00 00 00 0B 00 00 00 A6 00 00 00 98 00 00 00 DF 00 00 00 B5 00 00 00 AC 00 00 00 2F 00 00 00 }
		$BlowfishSBoxShort = { D1 00 31 00 0B 00 A6 00 98 00 DF 00 B5 00 AC 00 2F 00 FD 00 72 00 DB 00 D0 00 1A 00 DF 00 B7 00 }
		$BlowfishSBoxByte = { D1 31 0B A6 98 DF B5 AC 2F FD 72 DB D0 1A DF B7 B8 E1 AF ED 6A 26 7E 96 BA 7C 90 45 F1 2C 7F 99 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them		
}

rule Crypt_RC4_Init_Autoincrement {
	strings:
		$RC4_Init_Autoinc = { 88 04 30 40 3D 00 01 00 00 7C F5 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them	
}

rule Crypt_SHA256 {
	strings:
		$SHA256_const1 = { 67 E6 09 6A }
		$SHA256_const2 = { 85 AE 67 BB }
		$SHA256_const3 = { 72 F3 6E 3C }
		$SHA256_const4 = { 3A F5 4F A5 }
		$SHA256_const5 = { 7F 52 0E 51 }
		$SHA256_const6 = { 8C 68 05 9B }
		$SHA256_const7 = { AB D9 83 1F }
		$SHA256_const8 = { 19 CD E0 5B }
		$SHA256_code1 = { C1 ?? 13 ?? ?? C1 ?? 0A C1 ?? 11 }
		$SHA256_code2 = { C1 ?? 12 ?? ?? C1 ?? 07 ?? ?? C1 ?? 03 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		( all of ($SHA256_const*) or any of ($SHA256_code*))
}

rule Crypt_Camellia {
	strings:
		$CamelliaInt = { 70 00 00 00 82 00 00 00 2C 00 00 00 EC 00 00 00 B3 00 00 00 27 00 00 00 C0 00 00 00 E5 00 00 00 }
		$CamelliaShort = { 70 00 82 00 2C 00 EC 00 B3 00 27 00 C0 00 E5 00 E4 00 85 00 57 00 35 00 EA 00 0C 00 AE 00 41 00 }
		$CamelliaByte = { 70 82 2C EC B3 27 C0 E5 E4 85 57 35 EA 0C AE 41 23 EF 6B 93 45 19 A5 21 ED 0E 4F 4E 1D 65 92 BD }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them	
}

rule Crypt_Gost15 {
	strings:
		$GOST15Int = { FC 00 00 00 EE 00 00 00 DD 00 00 00 11 00 00 00 CF 00 00 00 6E 00 00 00 31 00 00 00 16 00 00 00 }
		$GOST15Short = { FC 00 EE 00 DD 00 11 00 CF 00 6E 00 31 00 16 00 FB 00 C4 00 FA 00 DA 00 23 00 C5 00 04 00 4D 00 }
		$GOST15Byte = { FC EE DD 11 CF 6E 31 16 FB C4 FA DA 23 C5 04 4D E9 77 F0 DB 93 2E 99 BA 17 36 F1 14 CD 5F C1 F9 }

	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}

rule Crypt_Gost89 {
	strings:
		$GOST89RFC4357Byte = { 04 0A 09 02 0D 08 00 0E 06 0B 01 0C 07 0F 05 03 0E 0B 04 0C 06 0D 0F 0A 02 03 08 01 00 07 05 09 }
		$GOST89RFC4357Short = { 04 00 0A 00 09 00 02 00 0D 00 08 00 00 00 0E 00 06 00 0B 00 01 00 0C 00 07 00 0F 00 05 00 03 00 }
		$GOST89RFC4357Int = { 04 00 00 00 0A 00 00 00 09 00 00 00 02 00 00 00 0D 00 00 00 08 00 00 00 00 00 00 00 0E 00 00 00 }
		$GOST89CryptoProByte = { 09 06 03 02 08 0B 01 07 0A 04 0E 0F 0C 00 0D 05 03 07 0E 09 08 0A 0F 00 05 02 06 0C 0B 04 0D 01 }
		$GOST89CryptoProShort = { 09 00 06 00 03 00 02 00 08 00 0B 00 01 00 07 00 0A 00 04 00 0E 00 0F 00 0C 00 00 00 0D 00 05 00 }
		$GOST89CryptoProInt = { 09 00 00 00 06 00 00 00 03 00 00 00 02 00 00 00 08 00 00 00 0B 00 00 00 01 00 00 00 07 00 00 00 }
		$GOST89TC26Byte = { 0C 04 06 02 0A 05 0B 09 0E 08 0D 07 00 03 0F 01 06 08 02 03 09 0A 05 0C 01 0E 04 07 0B 0D 00 0F }
		$GOST89TC26Short = { 0C 00 04 00 06 00 02 00  0A 00 05 00 0B 00 09 00 0E 00 08 00 0D 00 07 00 00 00 03 00 0F 00 01 00 }
		$GOST89TC26Int = { 0C 00 00 00 04 00 00 00 06 00 00 00 02 00 00 00 0A 00 00 00 05 00 00 00 0B 00 00 00 09 00 00 00 }

	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}

rule Crypt_DataEncryptionStandard {
	strings:
		$DESInitialPermutationInt = { 3A 00 00 00 32 00 00 00 2A 00 00 00 22 00 00 00 1A 00 00 00 12 00 00 00 0A 00 00 00 02 00 00 00 }
		$DESInitialPermutationShort = { 3A 00 32 00 2A 00 22 00 1A 00 12 00 0A 00 02 00 3C 00 34 00 2C 00 24 00 1C 00 14 00 0C 00 04 00 }
		$DESInitialPermutationByte = { 3A 32 2A 22 1A 12 0A 02 3C 34 2C 24 1C 14 0C 04 }
		$DESInitialPermutationMov = { C6 ?? ?? 3A C6 ?? ?? 32 C6 ?? ?? 2A C6 ?? ?? 22 C6 ?? ?? 1A C6 ?? ?? 12 C6 ?? ?? 0A C6 ?? ?? 02 C6 ?? ?? 3C }
		$DESFinalPermutationInt = { 28 00 00 00 08 00 00 00 30 00 00 00 10 00 00 00 38 00 00 00 18 00 00 00 40 00 00 00 20 00 00 00}
		$DESFinalPermutationShort = { 28 00 08 00 30 00 10 00 38 00 18 00 40 00 20 00 27 00 07 00 2F 00 0F 00 37 00 17 00 3F 00 1F 00 }
		$DESFinalPermutationByte = { 28 08 30 10 38 18 40 20 27 07 2F 0F 37 17 3F 1F }
		$DESFinalPermutationMov = { C6 ?? ?? 28 C6 ?? ?? 08 C6 ?? ?? 30 C6 ?? ?? 10 C6 ?? ?? 38 C6 ?? ?? 18 C6 ?? ?? 40 C6 ?? ?? 20 }
		$DESExpansionPermutationInt = { 20 00 00 00 01 00 00 00 02 00 00 00 03 00 00 00 04 00 00 00 05 00 00 00 04 00 00 00 05 00 00 00 }
		$DESExpansionPermutationShort = { 20 00 01 00 02 00 03 00 04 00 05 00 04 00 05 00 06 00 07 00 08 00 09 00 08 00 09 00 0A 00 0B 00 }
		$DESExpansionPermutationMov = { C6 ?? ?? 20 C6 ?? ?? 01 C6 ?? ?? 02 C6 ?? ?? 03 C6 ?? ?? 04 C6 ?? ?? 05 C6 ?? ?? 04 C6 ?? ?? 05 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}

// Compression section

rule Crypt_Compress_NotReallyVanished_UPX {
	strings:
		$NRV_code1 = { 8B ?? C1 ?? 08 83 ?? 01 41 }
		$NRV_CalcMaxExpansion = { 8B ?? ?? ?? 8B ?? C1 ?? 03 8D ?? ?? 00 02 00 00 C3 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}

// Crypto hashes section

rule Crypt_Hash_CRC32 {
	strings:
		$CRC32_m_tab = { 2C 61 0E EE BA 51 09 99 19 C4 6D 07 8F F4 6A 70 35 A5 63 E9 A3 95 64 9E 32 88 DB 0E A4 B8 DC 79 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}

rule Crypt_Hash_Haval {
	strings:
		$RK2 = { 45 28 21 E6 38 D0 13 77 BE 54 66 CF 34 E9 0C 6C }
		$RK5 = { BA 3B F0 50 7E FB 2A 98 A1 F1 65 1D 39 AF 01 76 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}

rule Crypt_Hash_MD5_MD4 {
	strings:
		$md5_magic1 = { 67 45 23 01 }
		$md5_magic2 = { ef cd ab 89 }
		$md5_magic3 = { 98 ba dc fe }
		$md5_magic4 = { 10 32 54 76 }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		all of them
}

// Encoding section

rule Crypt_Encode_Base64 {
	strings:
		$Base64Algo = { C0 ?? 04 C0 ?? 02 0A }
	condition:
		filesize < 10MB and
		(uint16(0)==0x457F or uint16(0)==0x5A4D) and
		any of them
}
