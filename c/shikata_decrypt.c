
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define shikata_decryptor 0xDA, 0xD4, 0xD9, 0x74, 0x24, 0xF4, 0x5B, 0xBF
#define shikata_initial_key_offset 0x08
#define shikata_decryption_len_offset 0x10
#define shikata_encrypted_block_offset 0x1A

struct shikata_header_struct {
	uint8_t first_code[8];
	uint8_t initial_key[4];
	uint8_t second_code[4];
	uint8_t decryption_len[2];
	uint8_t third_code[8];
	uint8_t *encrypted_block;
} shikata_header;

uint8_t *knuth_morris_pratt_failure(uint8_t *pattern, int pattern_length) {
	uint8_t *failure = (uint8_t *)malloc(pattern_length);
	uint8_t j = 0;

	for (uint8_t i = 1; i < pattern_length; i++) {
		while (j > 0 && pattern[j] != pattern[i]) {
			j = failure[j - 1];
		}
		if (pattern[j] == pattern[i]) {
			j++;
		}
		failure[i] = j;
	}
	return(failure);
}

int knuth_morris_pratt_search(uint8_t *data, uint8_t *pattern, int data_length, int pattern_length) {
	uint8_t *failure = knuth_morris_pratt_failure(pattern, pattern_length);
	int j = 0;

	if (data[0] == 0x00) 
		return(-1);
	for (int i = 0; i < data_length; i++) {
		while (j > 0 && pattern[j] != data[i]) {
			j = failure[j - 1];
		}
		if (pattern[j] == data[i]) {
			j++;
		}
		if (j == pattern_length) {
			return(i - pattern_length + 1);
		}
	}
	free(failure);
	return(-1);
}

int get_file_size(FILE *hEncoded) {
	int file_size = -1;
	fseek(hEncoded, 0L, SEEK_END);
	file_size = ftell(hEncoded);
	fseek(hEncoded, 0L, SEEK_SET);
	return(file_size);
}

int find_shikata(uint8_t *shikata_file_code, int data_length) {
	uint8_t decryptor_code[8] = { shikata_decryptor };
	int pattern_length = 8;	
	int shikata_offset = knuth_morris_pratt_search(shikata_file_code, decryptor_code, data_length, pattern_length);		
	return(shikata_offset);
}

int get_shikata_initial_key(uint8_t *shikata_file_code, int shikata_offset) {
	int initial_key;
	initial_key = shikata_file_code[shikata_offset + shikata_initial_key_offset + 3];
	initial_key <<= 8;
	initial_key |= shikata_file_code[shikata_offset + shikata_initial_key_offset + 2];
	initial_key <<= 8;
	initial_key |= shikata_file_code[shikata_offset + shikata_initial_key_offset + 1];
	initial_key <<= 8;
	initial_key |= shikata_file_code[shikata_offset + shikata_initial_key_offset];
	return(initial_key);
}

int get_shikata_decryption_len(uint8_t *shikata_file_code, int shikata_offset) {
	int decryption_len;
	decryption_len = shikata_file_code[shikata_decryption_len_offset + 1];
	decryption_len <<= 8;
	decryption_len |= shikata_file_code[shikata_decryption_len_offset];
	return(decryption_len);
}

uint8_t decrypt_shikata(uint8_t *shikata_file_code, int shikata_offset, int shikata_initial_key, int decryption_len) {
	int i = 0;
	int xor_key = shikata_initial_key,
		new_int_value;
	while (i < decryption_len) {
		shikata_file_code[shikata_offset + shikata_encrypted_block_offset + i*4] ^= xor_key;
		shikata_file_code[shikata_offset + shikata_encrypted_block_offset + i*4 + 1] ^= (xor_key >> 8);
		shikata_file_code[shikata_offset + shikata_encrypted_block_offset + i*4 + 2] ^= (xor_key >> 16);
		shikata_file_code[shikata_offset + shikata_encrypted_block_offset + i*4 + 3] ^= (xor_key >> 24);
		new_int_value = get_shikata_initial_key(shikata_file_code, shikata_offset + shikata_encrypted_block_offset + i*4 - shikata_initial_key_offset);
		xor_key += new_int_value;
		++i;
	}
	return(0);
}

int main(int argc, char const *argv[])
 {
	uint8_t *shikata_file_code;
	int encoded_file_size,
		shikata_offset,
		shikata_initial_key,
		shikata_decryption_len;
	FILE *hEncoded, *hDecoded;

	if (argc != 3)	{
		printf("Usage: shikata_decrypt <encrypted_file_name> <decrypted_file_name>\n");
		return(1);
	}

	hEncoded = fopen(argv[1], "rb");
	hDecoded = fopen(argv[2], "wb");

	encoded_file_size = get_file_size(hEncoded);
	shikata_file_code = (uint8_t *)malloc(encoded_file_size);
	fread(shikata_file_code, 1, encoded_file_size, hEncoded);

	shikata_offset = find_shikata(shikata_file_code, encoded_file_size);
	printf("encoder/x86/shikata_ga_nai found at offset: %x\n", shikata_offset);

	shikata_initial_key = get_shikata_initial_key(shikata_file_code, shikata_offset);
	printf("shikata initial xor key: %x\n", shikata_initial_key);
	shikata_decryption_len = get_shikata_decryption_len(shikata_file_code, shikata_offset);
	printf("shikata decryption length: %x\n", shikata_decryption_len);
	decrypt_shikata(shikata_file_code, shikata_offset, shikata_initial_key, shikata_decryption_len);
	printf("decrypted file: %s\n", argv[2]);
	fwrite(shikata_file_code, 1, encoded_file_size, hDecoded);
	
	fclose(hDecoded);
	fclose(hEncoded);
	free(shikata_file_code);
	return(0);
}
