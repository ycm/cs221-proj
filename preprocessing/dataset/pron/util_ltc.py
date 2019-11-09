#!/usr/bin/env python3
# CS 221
# Recreate ltc-pron scripts, in python3

import re

init_type = {
	'幫': 1, '帮': 1, '非': 1, '滂': 2, '敷': 2,
	'並': 3, '并': 3, '奉': 3, '明': 4, '微': 4,
	'端': 5, '透': 6, '定': 7, '泥': 8, '知': 9,
	'徹': 10, '澄': 11, '孃': 12, '娘': 12, '精': 13,
	'清': 14, '從': 15, '从': 15, '心': 16, '邪': 17,
	'莊': 18, '庄': 18, '初': 19, '崇': 20, '生': 21,
	'俟': 22, '章': 23, '昌': 24, '常': 25, '禪': 25,
	'禅': 25, '書': 26, '书': 26, '船': 27, '見': 28,
	'见': 28, '溪': 29, '谿': 29, '羣': 30, '群': 30,
	'疑': 31, '曉': 32, '晓': 32, '匣': 33, '影': 34,
	'于': 35, '云': 35, '雲': 35, '以': 36, '來': 37,
	'来': 37, '日': 38
}

fin_conv = {
	'冬': '沃', '東': '屋', '江': '覺', '鍾': '燭', '眞': '質',
	'臻': '櫛', '諄': '術', '痕': '麧', '魂': '沒', '欣': '迄',
	'文': '物', '寒': '曷', '桓': '末', '元': '月', '刪': '黠',
	'山': '鎋', '仙': '薛', '先': '屑', '唐': '鐸', '陽': '藥',
	'庚': '陌', '耕': '麥', '清': '昔', '青': '錫', '登': '德',
	'蒸': '職', '侵': '緝', '談': '盍', '嚴': '業', '凡': '乏',
	'銜': '狎', '咸': '洽', '鹽': '葉', '添': '怗', '覃': '合'
}

fin_type = {
	'冬': 5, '沃': 6, '鍾': 7, '燭': 8, '江': 9,
	'覺': 10, '之': 19, '魚': 22, '模': 23, '虞': 24,
	'咍': 41, '灰': 42, '臻': 46, '諄': 47, '櫛': 51,
	'術': 52, '痕': 53, '麧': 54, '魂': 55, '沒': 56,
	'欣': 57, '迄': 58, '文': 59, '物': 60, '寒': 61,
	'桓': 62, '曷': 63, '末': 64, '豪': 89, '肴': 90,
	'蕭': 93, '歌': 94, '蒸': 133, '尤': 136, '侯': 137,
	'幽': 138, '談': 143, '盍': 144, '嚴': 145, '凡': 146,
	'業': 147, '乏': 148, '銜': 149, '狎': 150, '咸': 151,
	'洽': 152, '添': 157, '怗': 158, '帖': 158, '覃': 159,
	'合': 160
}

fin_type_open = {
	'微開': 20, '微合': 21, '泰開': 25, '泰合': 26, '廢開': 27, '廢合': 28,
	'夬開': 29, '夬合': 30, '佳開': 31, '佳合': 32, '皆開': 33, '皆合': 34,
	'齊開': 39, '齊合': 40, '元開': 65, '元合': 66, '月開': 67, '月合': 68,
	'刪開': 69, '刪合': 70, '黠開': 71, '黠合': 72, '山開': 73, '山合': 74,
	'鎋開': 75, '鎋合': 76, '先開': 85, '先合': 86, '屑開': 87, '屑合': 88,
	'唐開': 101, '唐合': 102, '鐸開': 103, '鐸合': 104, '陽開': 105, '陽合': 106,
	'藥開': 107, '藥合': 108, '耕開': 117, '耕合': 118, '麥開': 119, '麥合': 120,
	'清開': 121, '清合': 122, '昔開': 123, '昔合': 124, '青開': 125, '青合': 126,
	'錫開': 127, '錫合': 128, '登開': 129, '登合': 130, '德開': 131, '德合': 132,
	'職開': 134, '職合': 135
}

fin_type_deng_open = {
	'支三開': 11, '支三合': 12, '支重鈕三開': 13, '支重鈕三合': 14,
	'脂三開': 15, '脂三合': 16, '脂重鈕四開': 15, '脂重鈕四合': 16,
		'脂重鈕三開': 17, '脂重鈕三合': 18,
	'祭三開': 35, '祭三合': 36, '祭重鈕四開': 35, '祭重鈕四合': 36, 
		'祭重鈕三開': 37, '祭重鈕三合': 38,
	'戈一合': 95, '戈三開': 96, '戈三合': 97,
	'仙三開': 77, '仙三合': 78, '仙重鈕三開': 79, '仙重鈕三合': 80,
	'薛三開': 81, '薛三合': 82, '薛重鈕三開': 83, '薛重鈕三合': 84,
	'麻二開': 98, '麻二合': 99, '麻三開': 100,
	'陌二開': 113, '陌二合': 114, '陌三開': 115, '陌三合': 116,
	'庚二開': 109, '庚二合': 110, '庚三開': 111, '庚三合': 112, 
		'庚重鈕三開': 111, '庚重鈕三合': 112
}

initialConv = {
	'Zhengzhang': {
		1: 'p', 2: 'pʰ', 3: 'b', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'd', 8: 'n', 9: 'ʈ', 10: 'ʈʰ',
		11: 'ɖ', 12: 'ɳ', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡z',
		16: 's', 17: 'z', 18: 't͡ʃ', 19: 't͡ʃʰ', 20: 'd͡ʒ',
		21: 'ʃ', 22: 'ʒ', 23: 't͡ɕ', 24: 't͡ɕʰ', 25: 'd͡ʑ',
		26: 'ɕ', 27: 'ʑ', 28: 'k', 29: 'kʰ', 30: 'ɡ',
		31: 'ŋ', 32: 'h', 33: 'ɦ', 34: 'ʔ', 35: 'ɦ',
		36: 'j', 37: 'l', 38: 'ȵ'
	},
	'Karlgren': {
		1: 'p', 2: 'pʰ', 3: 'bʱ', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'dʱ', 8: 'n', 9: 'ȶ', 10: 'ȶʰ',
		11: 'ȡʱ', 12: 'n', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡zʱ',
		16: 's', 17: 'z', 18: 'ʈ͡ʂ', 19: 'ʈ͡ʂʰ', 20: 'ɖ͡ʐʱ',
		21: 'ʂ', 22: 'ɖ͡ʐʰ', 23: 't͡ɕ', 24: 't͡ɕʰ', 25: 'ʑ',
		26: 'ɕ', 27: 'd͡ʑʰ', 28: 'k', 29: 'kʰ', 30: 'g',
		31: 'ŋ', 32: 'x', 33: 'ɣ', 34: 'ʔ', 35: '',
		36: '', 37: 'l', 38: 'ȵʑ'
	},
	'Li': {
		1: 'p', 2: 'pʰ', 3: 'b', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'd', 8: 'n', 9: 'ȶ', 10: 'ȶʰ',
		11: 'ȡ', 12: 'n', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡z',
		16: 's', 17: 'z', 18: 't͡ʃ', 19: 't͡ʃʰ', 20: 'd͡ʒ',
		21: 'ʃ', 22: 'ʒ', 23: 't͡ɕ', 24: 't͡ɕʰ', 25: 'ʑ',
		26: 'ɕ', 27: 'd͡ʑ', 28: 'k', 29: 'kʰ', 30: 'ɡ',
		31: 'ŋ', 32: 'x', 33: 'ɣ', 34: 'ʔ', 35: 'ɣ',
		36: '', 37: 'l', 38: 'ȵ'
	},
	'Pan': {
		1: 'p', 2: 'pʰ', 3: 'b', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'd', 8: 'n', 9: 'ʈ', 10: 'ʈʰ',
		11: 'ɖ', 12: 'ɳ', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡z',
		16: 's', 17: 'z', 18: 'ʈ͡ʂ', 19: 'ʈ͡ʂʰ', 20: 'ɖ͡ʐ',
		21: 'ʃ', 22: 'ʐ', 23: 't͡ɕ', 24: 't͡ɕʰ', 25: 'd͡ʑ',
		26: 'ɕ', 27: 'ʑ', 28: 'k', 29: 'kʰ', 30: 'ɡ',
		31: 'ŋ', 32: 'h', 33: 'ɦ', 34: 'ʔ', 35: 'ɦ',
		36: 'j', 37: 'l', 38: 'ȵ'
	},
	'Pulleyblank': {
		1: 'p', 2: 'pʰ', 3: 'b', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'd', 8: 'n', 9: 'ʈ', 10: 'ʈʰ',
		11: 'ɖ', 12: 'ɳ', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡z',
		16: 's', 17: 'z', 18: 'ʈ͡ʂ', 19: 'ʈ͡ʂʰ', 20: 'ɖ͡ʐ',
		21: 'ʂ', 22: 'ʐ', 23: 'c', 24: 'cʰ', 25: 'd͡ʑ',
		26: 'ɕ', 27: 'ʑ', 28: 'k', 29: 'kʰ', 30: 'g',
		31: 'ŋ', 32: 'h', 33: 'ɦ', 34: 'ʔ', 35: 'ɦ',
		36: 'j', 37: 'l', 38: 'ȵ'
	},
	'Wang': {
		1: 'p', 2: 'pʰ', 3: 'b', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'd', 8: 'n', 9: 'ȶ', 10: 'ȶʰ',
		11: 'ȡ', 12: 'n', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡z',
		16: 's', 17: 'z', 18: 't͡ʃ', 19: 't͡ʃʰ', 20: 'd͡ʒ',
		21: 'ʃ', 22: 'ʒ', 23: 't͡ɕ', 24: 't͡ɕʰ', 25: 'ʑ',
		26: 'ɕ', 27: 'd͡ʑ', 28: 'k', 29: 'kʰ', 30: 'ɡ',
		31: 'ŋ', 32: 'x', 33: 'ɣ', 34: '', 35: 'ɣ',
		36: 'j', 37: 'l', 38: 'ȵʑ'
	},
	'Shao': {
		1: 'p', 2: 'pʰ', 3: 'b', 4: 'm', 5: 't',
		6: 'tʰ', 7: 'd', 8: 'n', 9: 'ȶ', 10: 'ȶʰ',
		11: 'ȡ', 12: 'n', 13: 't͡s', 14: 't͡sʰ', 15: 'd͡z',
		16: 's', 17: 'z', 18: 't͡ʃ', 19: 't͡ʃʰ', 20: 'd͡ʒ',
		21: 'ʃ', 22: 'ʒ', 23: 't͡ɕ', 24: 't͡ɕʰ', 25: 'd͡ʑ',
		26: 'ɕ', 27: 'ʑ', 28: 'k', 29: 'kʰ', 30: 'ɡ',
		31: 'ŋ', 32: 'x', 33: 'ɣ', 34: 'ʔ', 35: 'ɣ',
		36: '', 37: 'l', 38: 'ȵʑ'
	}
}

finalConv = {
	"Zhengzhang": {
		1: "uŋ", 2: "ɨuŋ", 3: "uk̚", 4: "ɨuk̚", 5: "uoŋ",
		6: "uok̚", 7: "ɨoŋ", 8: "ɨok̚", 9: "ˠʌŋ", 10: "ˠʌk̚",
		11: "iᴇ", 12: "iuᴇ", 13: "ˠiᴇ", 14: "ˠiuᴇ", 15: "iɪ",
		16: "iuɪ", 17: "ˠiɪ", 18: "ˠiuɪ", 19: "ɨ", 20: "ɨi",
		21: "ʉi", 22: "ɨʌ", 23: "uo", 24: "ɨo", 25: "ɑi",
		26: "uɑi", 27: "ɨɐi", 28: "ʉɐi", 29: "ˠai", 30: "ˠuai",
		31: "ˠɛ", 32: "ˠuɛ", 33: "ˠɛi", 34: "ˠuɛi", 35: "iᴇi",
		36: "iuᴇi", 37: "ˠiᴇi", 38: "ˠiuᴇi", 39: "ei", 40: "wei",
		41: "ʌi", 42: "uʌi", 43: "iɪn", 44: "ˠiɪn", 45: "ˠiuɪn",
		46: "ɪn", 47: "iuɪn", 48: "iɪt̚", 49: "ˠiɪt̚", 50: "ˠiuɪt̚",
		51: "ɪt̚", 52: "iuɪt̚", 53: "ən", 54: "ət̚", 55: "uən",
		56: "uət̚", 57: "ɨn", 58: "ɨt̚", 59: "ɨun", 60: "ɨut̚",
		61: "ɑn", 62: "uɑn", 63: "ɑt̚", 64: "uɑt̚", 65: "ɨɐn",
		66: "ʉɐn", 67: "ɨɐt̚", 68: "ʉɐt̚", 69: "ˠan", 70: "ˠuan",
		71: "ˠat̚", 72: "ˠuat̚", 73: "ˠɛn", 74: "ˠuɛn", 75: "ˠɛt̚",
		76: "ˠuɛt̚", 77: "iᴇn", 78: "iuᴇn", 79: "ˠiᴇn", 80: "ˠiuᴇn",
		81: "iᴇt̚", 82: "iuᴇt̚", 83: "ˠiᴇt̚", 84: "ˠiuᴇt̚", 85: "en",
		86: "wen", 87: "et̚", 88: "wet̚", 89: "ɑu", 90: "ˠau",
		91: "iᴇu", 92: "ˠiᴇu", 93: "eu", 94: "ɑ", 95: "uɑ",
		96: "ɨɑ", 97: "ɨuɑ", 98: "ˠa", 99: "ˠua", 100: "ia",
		101: "ɑŋ", 102: "wɑŋ", 103: "ɑk̚", 104: "wɑk̚", 105: "ɨɐŋ",
		106: "ʉɐŋ", 107: "ɨɐk̚", 108: "ʉɐk̚", 109: "ˠæŋ", 110: "ˠwæŋ",
		111: "ˠiæŋ", 112: "ˠwiæŋ", 113: "ˠæk̚", 114: "ˠwæk̚", 115: "ˠiæk̚",
		116: "ˠwiæk̚", 117: "ˠɛŋ", 118: "ˠwɛŋ", 119: "ˠɛk̚", 120: "ˠwɛk̚",
		121: "iᴇŋ", 122: "wiᴇŋ", 123: "iᴇk̚", 124: "wiᴇk̚", 125: "eŋ",
		126: "weŋ", 127: "ek̚", 128: "wek̚", 129: "əŋ", 130: "wəŋ",
		131: "ək̚", 132: "wək̚", 133: "ɨŋ", 134: "ɨk̚", 135: "wɨk̚",
		136: "ɨu", 137: "əu", 138: "iɪu", 139: "iɪm", 140: "ˠiɪm",
		141: "iɪp̚", 142: "ˠiɪp̚", 143: "ɑm", 144: "ɑp̚", 145: "ɨɐm",
		146: "ɨɐm", 147: "ɨɐp̚", 148: "ɨɐp̚", 149: "ˠam", 150: "ˠap̚",
		151: "ˠɛm", 152: "ˠɛp̚", 153: "iᴇm", 154: "ˠiᴇm", 155: "iᴇp̚",
		156: "ˠiᴇp̚", 157: "em", 158: "ep̚", 159: "ʌm", 160: "ʌp̚"
	},
	"Karlgren": {
		1: "uŋ", 2: "i̯uŋ", 3: "uk̚", 4: "i̯uk̚", 5: "uoŋ",
		6: "uok̚", 7: "i̯woŋ", 8: "i̯wok̚", 9: "ɔŋ", 10: "ɔk̚",
		11: "ie̯", 12: "wie̯", 13: "ie̯", 14: "wie̯", 15: "i",
		16: "wi", 17: "i", 18: "wi", 19: "i", 20: "e̯i",
		21: "we̯i", 22: "i̯wo", 23: "uo", 24: "i̯u", 25: "ɑi",
		26: "uɑi", 27: "i̯ɐi", 28: "i̯wɐi", 29: "ai", 30: "wai",
		31: "ai", 32: "wai", 33: "ăi", 34: "wăi", 35: "i̯ɛi",
		36: "i̯wɛi", 37: "i̯ɛi", 38: "i̯wɛi", 39: "iei", 40: "iwei",
		41: "ɑ̆i", 42: "uɑ̆i", 43: "i̯ĕn", 44: "i̯ĕn", 45: "i̯ĕn",
		46: "i̯æn", 47: "i̯uĕn", 48: "i̯ĕt̚", 49: "i̯ĕt̚", 50: "i̯ĕt̚",
		51: "i̯æt̚", 52: "i̯uĕt̚", 53: "ən", 54: "ət̚", 55: "uən",
		56: "uət̚", 57: "i̯ən", 58: "i̯ət̚", 59: "i̯uən", 60: "i̯uət̚",
		61: "ɑn", 62: "uɑn", 63: "ɑt̚", 64: "uɑt̚", 65: "ɨ̯ɐn",
		66: "i̯wɐn", 67: "ɨ̯ɐt̚", 68: "i̯wɐt̚", 69: "an", 70: "wan",
		71: "ăt̚", 72: "wăt̚", 73: "ăn", 74: "wăn", 75: "at̚",
		76: "wat̚", 77: "i̯ɛn", 78: "i̯wɛn", 79: "i̯ɛn", 80: "i̯wɛn",
		81: "i̯ɛt̚", 82: "i̯wɛt̚", 83: "i̯ɛt̚", 84: "i̯wɛt̚", 85: "ien",
		86: "iwen", 87: "iet̚", 88: "iwet̚", 89: "ɑu", 90: "au",
		91: "i̯ɛu", 92: "i̯ɛu", 93: "ieu", 94: "ɑ", 95: "uɑ",
		96: "i̯ɑ", 97: "i̯wɑ", 98: "a", 99: "wa", 100: "i̯a",
		101: "ɑŋ", 102: "wɑŋ", 103: "ɑk̚", 104: "wɑk̚", 105: "i̯aŋ",
		106: "iwaŋ", 107: "i̯ak̚", 108: "iwak̚", 109: "ɐŋ", 110: "wɐŋ",
		111: "i̯ɐŋ", 112: "i̯wɐŋ", 113: "ɐk̚", 114: "wɐk̚", 115: "iɐk̚",
		116: "iwɐk̚", 117: "æŋ", 118: "wæŋ", 119: "æk̚", 120: "wæk̚",
		121: "i̯ɛŋ", 122: "i̯wɛŋ", 123: "i̯ɛk̚", 124: "i̯wɛk̚", 125: "ieŋ",
		126: "iweŋ", 127: "iek̚", 128: "iwek̚", 129: "əŋ", 130: "wəŋ",
		131: "ək̚", 132: "wək̚", 133: "i̯əŋ", 134: "i̯ək̚", 135: "i̯wək̚",
		136: "i̯ə̯u", 137: "ə̯u", 138: "ieu", 139: "i̯əm", 140: "i̯əm",
		141: "i̯əp̚", 142: "i̯əp̚", 143: "ɑm", 144: "ɑp̚", 145: "i̯ɐm",
		146: "i̯wɐm", 147: "i̯ɐp̚", 148: "i̯wɐp̚", 149: "am", 150: "ap̚",
		151: "ăm", 152: "ăp̚", 153: "i̯ɛm", 154: "i̯ɛm", 155: "i̯ɛp̚",
		156: "i̯ɛp̚", 157: "iem", 158: "iep̚", 159: "ăm", 160: "ăp̚"
	},
	"Li": {
		1: "uŋ", 2: "iuŋ", 3: "uk̚", 4: "iuk̚", 5: "oŋ",
		6: "ok̚", 7: "ioŋ", 8: "iok̚", 9: "ɔŋ", 10: "ɔk̚",
		11: "ie", 12: "iue", 13: "je", 14: "jue", 15: "i",
		16: "ui", 17: "ji", 18: "jui", 19: "iə", 20: "iəi",
		21: "iuəi", 22: "iɔ", 23: "o", 24: "io", 25: "ɑi",
		26: "uɑi", 27: "iɐi", 28: "iuɐi", 29: "ai", 30: "uai",
		31: "ɛ", 32: "uɛ", 33: "ɛi", 34: "uɛi", 35: "iɛi",
		36: "iuɛi", 37: "jɛi", 38: "juɛi", 39: "ei", 40: "uei",
		41: "ᴀi", 42: "uᴀi", 43: "iĕn", 44: "jĕn", 45: "juĕn",
		46: "iĕn", 47: "iuĕn", 48: "iĕt̚", 49: "jĕt̚", 50: "juĕt̚",
		51: "iĕt̚", 52: "iuĕt̚", 53: "ən", 54: "ət̚", 55: "uən",
		56: "uət̚", 57: "iən", 58: "iət̚", 59: "iuən", 60: "iuət̚",
		61: "ɑn", 62: "uɑn", 63: "ɑt̚", 64: "uɑt̚", 65: "iɐn",
		66: "iuɐn", 67: "iɐt̚", 68: "iuɐt̚", 69: "an", 70: "uan",
		71: "at̚", 72: "uat̚", 73: "ɛn", 74: "uɛn", 75: "ɛt̚",
		76: "uɛt̚", 77: "iɛn", 78: "iuɛn", 79: "jɛn", 80: "juɛn",
		81: "iɛt̚", 82: "iuɛt̚", 83: "jɛt̚", 84: "juɛt̚", 85: "en",
		86: "uen", 87: "et̚", 88: "uet̚", 89: "ɑu", 90: "au",
		91: "iɛu", 92: "jɛu", 93: "eu", 94: "ɑ", 95: "uɑ",
		96: "iɑ", 97: "iuɑ", 98: "a", 99: "ua", 100: "ia",
		101: "ɑŋ", 102: "uɑŋ", 103: "ɑk̚", 104: "uɑk̚", 105: "iaŋ",
		106: "iuaŋ", 107: "iak̚", 108: "iuak̚", 109: "ɐŋ", 110: "uɐŋ",
		111: "iɐŋ", 112: "iuɐŋ", 113: "ɐk̚", 114: "uɐk̚", 115: "iɐk̚",
		116: "iuɐk̚", 117: "ɛŋ", 118: "uɛŋ", 119: "ɛk̚", 120: "uɛk̚",
		121: "iɛŋ", 122: "iuɛŋ", 123: "iɛk̚", 124: "iuɛk̚", 125: "eŋ",
		126: "ueŋ", 127: "ek̚", 128: "uek̚", 129: "əŋ", 130: "uəŋ",
		131: "ək̚", 132: "uək̚", 133: "iəŋ", 134: "iək̚", 135: "iuək̚",
		136: "iu", 137: "u", 138: "iĕu", 139: "iəm", 140: "jəm",
		141: "iəp̚", 142: "jəp̚", 143: "ɑm", 144: "ɑp̚", 145: "iɐm",
		146: "iɐm", 147: "iap̚", 148: "iɐp̚", 149: "am", 150: "ap̚",
		151: "ɐm", 152: "ɐp̚", 153: "iɛm", 154: "jɛm", 155: "iɛp̚",
		156: "jɛp̚", 157: "em", 158: "ep̚", 159: "ᴀm", 160: "ᴀp̚"
	},
	"Pan": {
		1: "uŋ", 2: "iuŋ", 3: "uk̚", 4: "iuk̚", 5: "uoŋ",
		6: "uok̚", 7: "ioŋ", 8: "iok̚", 9: "ᵚɔŋ", 10: "ᵚɔk̚",
		11: "iɛ", 12: "ʷiɛ", 13: "ᵚiɛ", 14: "ʷᵚiɛ", 15: "i",
		16: "ʷi", 17: "ᵚi", 18: "ʷᵚi", 19: "ɨ", 20: "ɨi",
		21: "ʷɨi", 22: "iɔ", 23: "uo", 24: "io", 25: "ɑi",
		26: "ʷɑi", 27: "iɐi", 28: "ʷiɐi", 29: "ᵚai", 30: "ʷᵚai",
		31: "ᵚæ", 32: "ʷᵚæ", 33: "ᵚæi", 34: "ʷᵚæi", 35: "iɛi",
		36: "ʷiɛi", 37: "ᵚiɛi", 38: "ʷᵚiei", 39: "ei", 40: "ʷei",
		41: "əi", 42: "uoi", 43: "in", 44: "ᵚin", 45: "ʷᵚin",
		46: "ɪn", 47: "ʷin", 48: "it̚", 49: "ᵚit̚", 50: "ʷᵚit̚",
		51: "ɪt̚", 52: "ʷit̚", 53: "ən", 54: "ət̚", 55: "uon",
		56: "uot̚", 57: "ɨn", 58: "ɨt̚", 59: "iun", 60: "iut̚",
		61: "ɑn", 62: "ʷɑn", 63: "ɑt̚", 64: "ʷɑt̚", 65: "iɐn",
		66: "ʷiɐn", 67: "iɐt̚", 68: "ʷiɐt̚", 69: "ᵚan", 70: "ʷᵚan",
		71: "ᵚat̚", 72: "ʷᵚat̚", 73: "ᵚæn", 74: "ʷᵚæn", 75: "ᵚæt̚",
		76: "ʷᵚæt̚", 77: "iɛn", 78: "ʷiɛn", 79: "ᵚiɛn", 80: "ʷᵚiɛn",
		81: "iɛt̚", 82: "ʷiɛt̚", 83: "ᵚiɛt̚", 84: "ʷᵚiet̚", 85: "en",
		86: "ʷen", 87: "et̚", 88: "ʷet̚", 89: "ɑu", 90: "ᵚau",
		91: "iɛu", 92: "ᵚiɛu", 93: "eu", 94: "ɑ", 95: "uɑ",
		96: "iɑ", 97: "ʷiɑ", 98: "ᵚa", 99: "ʷᵚa", 100: "ia",
		101: "ɑŋ", 102: "ʷɑŋ", 103: "ɑk̚", 104: "ʷɑk̚", 105: "iɐŋ",
		106: "ʷiɐŋ", 107: "iɐk̚", 108: "ʷiɐk̚", 109: "ᵚaŋ", 110: "ʷᵚaŋ",
		111: "ᵚiaŋ", 112: "ʷᵚiaŋ", 113: "ᵚak̚", 114: "ʷᵚak̚", 115: "ᵚiak̚",
		116: "ʷᵚiak̚", 117: "ᵚæŋ", 118: "ʷᵚæŋ", 119: "ᵚæk̚", 120: "ʷᵚæk̚",
		121: "iɛŋ", 122: "ʷiɛŋ", 123: "iɛk̚", 124: "ʷiɛk̚", 125: "eŋ",
		126: "ʷeŋ", 127: "ek̚", 128: "ʷek̚", 129: "əŋ", 130: "ʷəŋ",
		131: "ək̚", 132: "ʷək̚", 133: "ɨŋ", 134: "ɨk̚", 135: "ʷɨk̚",
		136: "iu", 137: "əu", 138: "ɨu", 139: "im", 140: "ᵚim",
		141: "ip̚", 142: "ᵚip̚", 143: "ɑm", 144: "ɑp̚", 145: "iɐm",
		146: "iɐm", 147: "iɐp̚", 148: "iɐp̚", 149: "ᵚam", 150: "ᵚap̚",
		151: "ᵚæm", 152: "ᵚæp̚", 153: "iɛm", 154: "ᵚiɛm", 155: "iɛp̚",
		156: "ᵚiɛp̚", 157: "em", 158: "ep̚", 159: "əm", 160: "əp̚"
	},
	"Pulleyblank": {
		1: "əwŋ", 2: "uwŋ", 3: "əwk̚", 4: "uwk̚", 5: "awŋ",
		6: "awk̚", 7: "uawŋ", 8: "uawk̚", 9: "aɨwŋ", 10: "aɨwk̚",
		11: "iə̆", 12: "wiə̆", 13: "jiə̆", 14: "jwiə̆", 15: "i",
		16: "wi", 17: "ji", 18: "jwi", 19: "ɨ", 20: "ɨj",
		21: "uj", 22: "ɨə̆", 23: "ɔ", 24: "uə̆", 25: "aj",
		26: "waj", 27: "ɨaj", 28: "uaj", 29: "aɨjs", 30: "waɨjs",
		31: "aɨj", 32: "waɨj", 33: "əɨj", 34: "wəɨj", 35: "iaj",
		36: "wiaj", 37: "jiaj", 38: "jwiaj", 39: "ɛj", 40: "wɛj",
		41: "əj", 42: "wəj", 43: "in", 44: "jin", 45: "jin",
		46: "in", 47: "win", 48: "it̚", 49: "jit̚", 50: "jit̚",
		51: "it̚", 52: "wit̚", 53: "ən", 54: "ət̚", 55: "wən",
		56: "wət̚", 57: "ɨn", 58: "ɨt̚", 59: "un", 60: "ut̚",
		61: "an", 62: "wan", 63: "at̚", 64: "wat̚", 65: "ɨan",
		66: "uan", 67: "ɨat̚", 68: "uat̚", 69: "aɨn", 70: "waɨn",
		71: "aɨt̚", 72: "waɨt̚", 73: "əɨn", 74: "wəɨn", 75: "əɨt̚",
		76: "wəɨt̚", 77: "ian", 78: "wian", 79: "ian", 80: "wian",
		81: "iat̚", 82: "wiat̚", 83: "iat̚", 84: "wiat̚", 85: "ɛn",
		86: "wɛn", 87: "ɛt̚", 88: "wɛt̚", 89: "aw", 90: "aɨw",
		91: "iaw", 92: "iaw", 93: "ɛw", 94: "a", 95: "wa",
		96: "ɨa", 97: "ua", 98: "aɨ", 99: "waɨ", 100: "ia",
		101: "aŋ", 102: "waŋ", 103: "ak̚", 104: "wak̚", 105: "ɨaŋ",
		106: "uaŋ", 107: "ɨak̚", 108: "uak̚", 109: "aɨjŋ", 110: "waɨjŋ",
		111: "iajŋ", 112: "wiajŋ", 113: "aɨjk̚", 114: "waɨjk̚", 115: "iajk̚",
		116: "wiajk̚", 117: "əɨjŋ", 118: "wəɨjŋ", 119: "əɨjk̚", 120: "wəɨjk̚",
		121: "iajŋ", 122: "wiajŋ", 123: "iajk̚", 124: "wiajk̚", 125: "ɛjŋ",
		126: "wɛjŋ", 127: "ɛjk̚", 128: "wɛjk̚", 129: "əŋ", 130: "wəŋ",
		131: "ək̚", 132: "wək̚", 133: "iŋ", 134: "ik̚", 135: "wik̚",
		136: "uw", 137: "əw", 138: "jiw", 139: "im", 140: "jim",
		141: "ip̚", 142: "jip̚", 143: "am", 144: "ap̚", 145: "ɨam",
		146: "uam", 147: "ɨap̚", 148: "uap̚", 149: "aɨm", 150: "aɨp̚",
		151: "əɨm", 152: "əɨp̚", 153: "iam", 154: "jiam", 155: "iap̚",
		156: "jiap̚", 157: "ɛm", 158: "ɛp̚", 159: "əm", 160: "əp̚"
	},
	"Wang": {
		1: "uŋ", 2: "ĭuŋ", 3: "uk̚", 4: "ĭuk̚", 5: "uoŋ",
		6: "uok̚", 7: "ĭwoŋ", 8: "ĭwok̚", 9: "ɔŋ", 10: "ɔk̚",
		11: "ǐe", 12: "ǐwe", 13: "ǐe", 14: "ǐwe", 15: "i",
		16: "wi", 17: "i", 18: "wi", 19: "ĭə", 20: "ĭəi",
		21: "ĭwəi", 22: "ĭo", 23: "u", 24: "ĭu", 25: "ɑi",
		26: "uɑi", 27: "ĭɐi", 28: "ĭwɐi", 29: "æi", 30: "wæi",
		31: "ai", 32: "wai", 33: "ɐi", 34: "wɐi", 35: "ĭɛi",
		36: "ĭwɛi", 37: "ĭɛi", 38: "ĭwɛi", 39: "iei", 40: "iwei",
		41: "ɒi", 42: "uɒi", 43: "ĭĕn", 44: "ǐĕn", 45: "ǐĕn",
		46: "ĭen", 47: "ĭuĕn", 48: "ĭĕt̚", 49: "ĭĕt̚", 50: "ĭĕt̚",
		51: "ĭet̚", 52: "ĭuĕt̚", 53: "ən", 54: "ət̚", 55: "uən",
		56: "uət̚", 57: "ĭən", 58: "ĭət̚", 59: "ĭuən", 60: "ĭuət̚",
		61: "ɑn", 62: "uɑn", 63: "ɑt̚", 64: "uɑt̚", 65: "ĭɐn",
		66: "ĭwɐn", 67: "ĭɐt̚", 68: "ĭwɐt̚", 69: "an", 70: "wan",
		71: "at̚", 72: "wat̚", 73: "æn", 74: "wæn", 75: "æt̚",
		76: "wæt̚", 77: "ĭɛn", 78: "ĭwɛn", 79: "ĭɛn", 80: "ĭwɛn",
		81: "ĭɛt̚", 82: "ĭuɛt̚", 83: "ĭɛt̚", 84: "ĭuɛt̚", 85: "ien",
		86: "iwen", 87: "iet̚", 88: "iwet̚", 89: "ɑu", 90: "au",
		91: "ĭɛu", 92: "ĭɛu", 93: "ieu", 94: "ɑ", 95: "uɑ",
		96: "ǐɑ", 97: "ĭuɑ", 98: "a", 99: "wa", 100: "ĭa",
		101: "ɑŋ", 102: "uɑŋ", 103: "ɑk̚", 104: "uɑk̚", 105: "ĭaŋ",
		106: "ĭwaŋ", 107: "ĭak̚", 108: "ĭak̚", 109: "ɐŋ", 110: "wɐŋ",
		111: "ĭɐŋ", 112: "ĭwɐŋ", 113: "ɐk̚", 114: "wɐk̚", 115: "ĭɐk̚",
		116: "ĭwɐk̚", 117: "æŋ", 118: "wæŋ", 119: "æk̚", 120: "wæk̚",
		121: "ĭɛŋ", 122: "ĭwɛŋ", 123: "ĭɛk̚", 124: "ĭwɛk̚", 125: "ieŋ",
		126: "iweŋ", 127: "iek̚", 128: "iwek̚", 129: "əŋ", 130: "uəŋ",
		131: "ək̚", 132: "uək̚", 133: "ĭəŋ", 134: "ĭək̚", 135: "ĭwək̚",
		136: "ĭəu", 137: "əu", 138: "iəu", 139: "ĭĕm", 140: "ĭĕm",
		141: "ĭĕp̚", 142: "ĭĕp̚", 143: "ɑm", 144: "ɑp̚", 145: "ĭɐm",
		146: "ĭwɐm", 147: "ĭɐp̚", 148: "ĭwɐp̚", 149: "am", 150: "ap̚",
		151: "ɐm", 152: "ɐp̚", 153: "ĭɛm", 154: "ĭɛm", 155: "ĭɛp̚",
		156: "ĭɛp̚", 157: "iem", 158: "iep̚", 159: "ɒm", 160: "ɒp̚"
	},
	"Shao": {
		1: "uŋ", 2: "iuŋ", 3: "uk̚", 4: "iuk̚", 5: "oŋ",
		6: "ok̚", 7: "ioŋ", 8: "iok̚", 9: "ɔŋ", 10: "ɔk̚",
		11: "jɛ", 12: "juɛ", 13: "iɛ", 14: "iuɛ", 15: "jɪ",
		16: "juɪ", 17: "iɪ", 18: "iuɪ", 19: "ie", 20: "iəi",
		21: "iuəi", 22: "iɔ", 23: "o", 24: "io", 25: "ɑi",
		26: "uɑi", 27: "iɐi", 28: "iuɐi", 29: "ai", 30: "uai",
		31: "æi", 32: "uæi", 33: "ɐi", 34: "uɐi", 35: "jæi",
		36: "iuæi", 37: "iæi", 38: "iuæi", 39: "ɛi", 40: "uɛi",
		41: "ɒi", 42: "uɒi", 43: "jen", 44: "ien", 45: "iuen",
		46: "ien", 47: "juen", 48: "jet̚", 49: "iet̚", 50: "iuet̚",
		51: "iet̚", 52: "juet̚", 53: "ən", 54: "ət̚", 55: "uən",
		56: "uət̚", 57: "iən", 58: "iət̚", 59: "iuən", 60: "iuət̚",
		61: "ɑn", 62: "uɑn", 63: "ɑt̚", 64: "uɑt̚", 65: "iɐn",
		66: "iuɐn", 67: "iɐt̚", 68: "iuɐt̚", 69: "ɐn", 70: "uɐn",
		71: "ɐt̚", 72: "uɐt̚", 73: "æn", 74: "uæn", 75: "æt̚",
		76: "uæt̚", 77: "jæn", 78: "juæn", 79: "iæn", 80: "iuæn",
		81: "jæt̚", 82: "juæt̚", 83: "iæt̚", 84: "iuæt̚", 85: "ɛn",
		86: "uɛn", 87: "ɛt̚", 88: "uɛt̚", 89: "ɑu", 90: "au",
		91: "jæu", 92: "iæu", 93: "eu", 94: "ɑ", 95: "uɑ",
		96: "iɑ", 97: "iuɑ", 98: "a", 99: "ua", 100: "ia",
		101: "ɑŋ", 102: "uɑŋ", 103: "ɑk̚", 104: "uɑk̚", 105: "iɑŋ",
		106: "iuɑŋ", 107: "iɑk̚", 108: "iuɑk̚", 109: "aŋ", 110: "uaŋ",
		111: "iaŋ", 112: "iuaŋ", 113: "ak̚", 114: "uak̚", 115: "iak̚",
		116: "iuak̚", 117: "ɐŋ", 118: "uɐŋ", 119: "ɐk̚", 120: "uɐk̚",
		121: "iæŋ", 122: "iuæŋ", 123: "iæk̚", 124: "iuæk̚", 125: "ɛŋ",
		126: "uɛŋ", 127: "ɛk̚", 128: "uɛk̚", 129: "əŋ", 130: "uəŋ",
		131: "ək̚", 132: "uək̚", 133: "ieŋ", 134: "iek̚", 135: "iuek̚",
		136: "iəu", 137: "əu", 138: "ieu", 139: "jem", 140: "iem",
		141: "jep̚", 142: "iep̚", 143: "ɑm", 144: "ɑp̚", 145: "iɐm",
		146: "iɐm", 147: "iɐp̚", 148: "iɐp̚", 149: "am", 150: "ap̚",
		151: "ɐm", 152: "ɐp̚", 153: "jæm", 154: "iæm", 155: "jæp̚",
		156: "iæp̚", 157: "ɛm", 158: "ɛp̚", 159: "ɒm", 160: "ɒp̚"
	}
}

final_deng = {
	'東一': 1, '東三': 2, '屋一': 3, '屋三': 4,
	'宵三': 91, '宵重鈕四': 91, '宵重鈕三': 92,
	'侵三': 139, '侵重鈕三': 140, '緝三': 141, '緝重鈕三': 142,
	'葉三': 155, '葉重鈕三': 156, '鹽三': 153, '鹽重鈕三': 154,
	'真三': 43, '真重鈕四': 43,
	'眞三': 43, '眞重鈕四': 43,
	'質三': 48, '質重鈕四': 48
}

division = {
	'一': 'I', 
	'二': 'II', 
	'三': 'III', 
	'四': 'IV', 
	'重鈕三': "''Chongniu'' III",
	'重鈕四': "''Chongniu'' IV"
}

open_closed = {
	'開': 'Open',
	'合': 'Closed'
}

tonality = {
	'上': 'Rising (X)',
	'去': 'Departing (H)',
	'平': 'Level (Ø)',
	'入': 'Checked (Ø)'
}

tone_class = {
	'平': 'level',
	'上': 'rising',
	'去': 'departing',
	'入': 'checked'
}

tone_number = { '平': 1, '上': 2, '去': 3, '入': 4 }

final_openness = {
	'真開': 44, '真合': 45,
	'眞開': 44, '眞合': 45,
	'質開': 49, '質合': 50
}

final_type_1 = re.compile('[微泰廢夬佳皆齊元月刪黠山鎋先屑唐鐸陽藥耕麥清昔青錫登德職]')
final_type_2 = re.compile('[東屋宵侵緝葉鹽]')
final_type_3 = re.compile('[支脂祭戈仙薛麻陌庚]')
final_type_4 = re.compile('[真眞質]')
final_type_5 = re.compile('[冬沃鍾燭江覺之魚模虞咍灰臻諄櫛術痕麧魂沒欣迄文物寒桓曷末豪肴蕭歌蒸尤侯幽談盍嚴凡業乏銜狎咸洽添怗帖覃合]')

def load_resources():
	return {
		'init_type': init_type,
		'fin_type': fin_type,
		'fin_conv': fin_conv,
		'fin_type_open': fin_type_open,
		'fin_type_deng_open': fin_type_deng_open,
		'initialConv': initialConv,
		'finalConv': finalConv,
		'final_deng': final_deng,
		'division': division,
		'open_closed': open_closed,
		'tonality': tonality,
		'tone_class': tone_class,
		'tone_number': tone_number,
		'final_openness': final_openness,
		'final_type_1': final_type_1,
		'final_type_2': final_type_2,
		'final_type_3': final_type_3,
		'final_type_4': final_type_4,
		'final_type_5': final_type_5
	}
