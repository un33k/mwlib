/* Generated by re2c 0.13.2 */
#line 1 "_expander.re"
// -*- mode: c++ -*-
// Copyright (c) 2007-2008 PediaPress GmbH
// See README.txt for additional licensing information.

#include <Python.h>

#include <iostream>
#include <assert.h>
#include <vector>

using namespace std;

#define RET(x) {found(x); return x;}

struct Token
{
	int type;
	int start;
	int len;
};


class MacroScanner
{
public:

	MacroScanner(Py_UNICODE *_start, Py_UNICODE *_end) {
		source = start = _start;
		end = _end;
		cursor = start;
	}

	int found(int val) {
		if (val==5 && tokens.size()) {
			Token &previous_token (tokens[tokens.size()-1]);
			if (previous_token.type==val) {
				previous_token.len += cursor-start;
				return tokens.size()-1;
			}
		}
		Token t;
		t.type = val;
		t.start = (start-source);
		t.len = cursor-start;			
		tokens.push_back(t);
		return tokens.size()-1;
	}

	inline int scan();

	Py_UNICODE *source;

	Py_UNICODE *start;
	Py_UNICODE *cursor;
	Py_UNICODE *end;
	vector<Token> tokens;
};


int MacroScanner::scan()
{

std:

	start=cursor;
	
	Py_UNICODE *marker=cursor;

	Py_UNICODE *save_cursor = cursor;


#define YYCTYPE         Py_UNICODE
#define YYCURSOR        cursor
#define YYMARKER	marker
#define YYLIMIT   (end)
// #define YYFILL(n) return 0;

#line 80 "_expander.re"





#line 87 "_expander.cc"
{
	YYCTYPE yych;

	yych = *YYCURSOR;
	if (yych <= '\\') {
		if (yych <= '<') {
			if (yych <= 0x0000) goto yy10;
			if (yych <= ';') goto yy12;
			goto yy9;
		} else {
			if (yych == '[') goto yy5;
			goto yy12;
		}
	} else {
		if (yych <= '{') {
			if (yych <= ']') goto yy6;
			if (yych <= 'z') goto yy12;
		} else {
			if (yych <= '|') goto yy7;
			if (yych <= '}') goto yy4;
			goto yy12;
		}
	}
	++YYCURSOR;
	if ((yych = *YYCURSOR) == '{') goto yy78;
yy3:
#line 99 "_expander.re"
	{RET(5);}
#line 116 "_expander.cc"
yy4:
	yych = *++YYCURSOR;
	if (yych == '}') goto yy75;
	goto yy3;
yy5:
	yych = *++YYCURSOR;
	if (yych == '[') goto yy73;
	goto yy3;
yy6:
	yych = *++YYCURSOR;
	if (yych == ']') goto yy73;
	goto yy3;
yy7:
	++YYCURSOR;
#line 88 "_expander.re"
	{RET(6);}
#line 133 "_expander.cc"
yy9:
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych <= 'M') {
		if (yych <= 'G') {
			if (yych == '!') goto yy13;
			if (yych <= 'F') goto yy3;
			goto yy15;
		} else {
			if (yych == 'I') goto yy17;
			if (yych <= 'L') goto yy3;
			goto yy16;
		}
	} else {
		if (yych <= 'h') {
			if (yych <= 'N') goto yy18;
			if (yych == 'g') goto yy15;
			goto yy3;
		} else {
			if (yych <= 'l') {
				if (yych <= 'i') goto yy17;
				goto yy3;
			} else {
				if (yych <= 'm') goto yy16;
				if (yych <= 'n') goto yy18;
				goto yy3;
			}
		}
	}
yy10:
	++YYCURSOR;
#line 98 "_expander.re"
	{RET(0);}
#line 166 "_expander.cc"
yy12:
	yych = *++YYCURSOR;
	goto yy3;
yy13:
	yych = *++YYCURSOR;
	if (yych == '-') goto yy60;
yy14:
	YYCURSOR = YYMARKER;
	goto yy3;
yy15:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy51;
	if (yych == 'a') goto yy51;
	goto yy14;
yy16:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy45;
	if (yych == 'a') goto yy45;
	goto yy14;
yy17:
	yych = *++YYCURSOR;
	if (yych == 'M') goto yy35;
	if (yych == 'm') goto yy35;
	goto yy14;
yy18:
	yych = *++YYCURSOR;
	if (yych == 'O') goto yy19;
	if (yych != 'o') goto yy14;
yy19:
	yych = *++YYCURSOR;
	if (yych <= 'W') {
		if (yych == 'I') goto yy21;
		if (yych <= 'V') goto yy14;
	} else {
		if (yych <= 'i') {
			if (yych <= 'h') goto yy14;
			goto yy21;
		} else {
			if (yych != 'w') goto yy14;
		}
	}
	yych = *++YYCURSOR;
	if (yych == 'I') goto yy30;
	if (yych == 'i') goto yy30;
	goto yy14;
yy21:
	yych = *++YYCURSOR;
	if (yych == 'N') goto yy22;
	if (yych != 'n') goto yy14;
yy22:
	yych = *++YYCURSOR;
	if (yych == 'C') goto yy23;
	if (yych != 'c') goto yy14;
yy23:
	yych = *++YYCURSOR;
	if (yych == 'L') goto yy24;
	if (yych != 'l') goto yy14;
yy24:
	yych = *++YYCURSOR;
	if (yych == 'U') goto yy25;
	if (yych != 'u') goto yy14;
yy25:
	yych = *++YYCURSOR;
	if (yych == 'D') goto yy26;
	if (yych != 'd') goto yy14;
yy26:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy27;
	if (yych != 'e') goto yy14;
yy27:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy14;
	++YYCURSOR;
#line 90 "_expander.re"
	{goto noinclude;}
#line 242 "_expander.cc"
yy30:
	yych = *++YYCURSOR;
	if (yych == 'K') goto yy31;
	if (yych != 'k') goto yy14;
yy31:
	yych = *++YYCURSOR;
	if (yych == 'I') goto yy32;
	if (yych != 'i') goto yy14;
yy32:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy14;
	++YYCURSOR;
#line 91 "_expander.re"
	{goto nowiki;}
#line 257 "_expander.cc"
yy35:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy36;
	if (yych != 'a') goto yy14;
yy36:
	yych = *++YYCURSOR;
	if (yych == 'G') goto yy37;
	if (yych != 'g') goto yy14;
yy37:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy38;
	if (yych != 'e') goto yy14;
yy38:
	yych = *++YYCURSOR;
	if (yych == 'M') goto yy39;
	if (yych != 'm') goto yy14;
yy39:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy40;
	if (yych != 'a') goto yy14;
yy40:
	yych = *++YYCURSOR;
	if (yych == 'P') goto yy41;
	if (yych != 'p') goto yy14;
yy41:
	++YYCURSOR;
	yych = *YYCURSOR;
	if (yych <= '<') {
		if (yych <= 0x0000) goto yy14;
		if (yych <= ';') goto yy41;
		goto yy14;
	} else {
		if (yych != '>') goto yy41;
	}
	++YYCURSOR;
#line 92 "_expander.re"
	{goto imagemap;}
#line 295 "_expander.cc"
yy45:
	yych = *++YYCURSOR;
	if (yych == 'T') goto yy46;
	if (yych != 't') goto yy14;
yy46:
	yych = *++YYCURSOR;
	if (yych == 'H') goto yy47;
	if (yych != 'h') goto yy14;
yy47:
	++YYCURSOR;
	yych = *YYCURSOR;
	if (yych <= '<') {
		if (yych <= 0x0000) goto yy14;
		if (yych <= ';') goto yy47;
		goto yy14;
	} else {
		if (yych != '>') goto yy47;
	}
	++YYCURSOR;
#line 93 "_expander.re"
	{goto math;}
#line 317 "_expander.cc"
yy51:
	yych = *++YYCURSOR;
	if (yych == 'L') goto yy52;
	if (yych != 'l') goto yy14;
yy52:
	yych = *++YYCURSOR;
	if (yych == 'L') goto yy53;
	if (yych != 'l') goto yy14;
yy53:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy54;
	if (yych != 'e') goto yy14;
yy54:
	yych = *++YYCURSOR;
	if (yych == 'R') goto yy55;
	if (yych != 'r') goto yy14;
yy55:
	yych = *++YYCURSOR;
	if (yych == 'Y') goto yy56;
	if (yych != 'y') goto yy14;
yy56:
	++YYCURSOR;
	yych = *YYCURSOR;
	if (yych <= '<') {
		if (yych <= 0x0000) goto yy14;
		if (yych <= ';') goto yy56;
		goto yy14;
	} else {
		if (yych != '>') goto yy56;
	}
	++YYCURSOR;
#line 94 "_expander.re"
	{goto gallery;}
#line 351 "_expander.cc"
yy60:
	yych = *++YYCURSOR;
	if (yych != '-') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '[') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '^') goto yy14;
	yych = *++YYCURSOR;
	if (yych >= 0x0001) goto yy14;
	yych = *++YYCURSOR;
	if (yych != '<') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '>') goto yy14;
	yych = *++YYCURSOR;
	if (yych != ']') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '*') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '-') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '-') goto yy14;
	yych = *++YYCURSOR;
	if (yych != '>') goto yy14;
	++YYCURSOR;
#line 96 "_expander.re"
	{RET(5);}
#line 378 "_expander.cc"
yy73:
	++YYCURSOR;
#line 87 "_expander.re"
	{RET(3);}
#line 383 "_expander.cc"
yy75:
	++YYCURSOR;
	yych = *YYCURSOR;
	if (yych == '}') goto yy75;
#line 86 "_expander.re"
	{RET(2);}
#line 390 "_expander.cc"
yy78:
	++YYCURSOR;
	yych = *YYCURSOR;
	if (yych == '{') goto yy78;
#line 85 "_expander.re"
	{RET(1);}
#line 397 "_expander.cc"
}
#line 101 "_expander.re"




noinclude:

#line 406 "_expander.cc"
{
	YYCTYPE yych;
	yych = *YYCURSOR;
	if (yych <= 0x0000) goto yy86;
	if (yych != '<') goto yy85;
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych == '/') goto yy88;
yy84:
#line 108 "_expander.re"
	{goto noinclude;}
#line 417 "_expander.cc"
yy85:
	yych = *++YYCURSOR;
	goto yy84;
yy86:
	++YYCURSOR;
#line 109 "_expander.re"
	{cursor=start+11; RET(5);}
#line 425 "_expander.cc"
yy88:
	yych = *++YYCURSOR;
	if (yych == 'N') goto yy90;
	if (yych == 'n') goto yy90;
yy89:
	YYCURSOR = YYMARKER;
	goto yy84;
yy90:
	yych = *++YYCURSOR;
	if (yych == 'O') goto yy91;
	if (yych != 'o') goto yy89;
yy91:
	yych = *++YYCURSOR;
	if (yych == 'I') goto yy92;
	if (yych != 'i') goto yy89;
yy92:
	yych = *++YYCURSOR;
	if (yych == 'N') goto yy93;
	if (yych != 'n') goto yy89;
yy93:
	yych = *++YYCURSOR;
	if (yych == 'C') goto yy94;
	if (yych != 'c') goto yy89;
yy94:
	yych = *++YYCURSOR;
	if (yych == 'L') goto yy95;
	if (yych != 'l') goto yy89;
yy95:
	yych = *++YYCURSOR;
	if (yych == 'U') goto yy96;
	if (yych != 'u') goto yy89;
yy96:
	yych = *++YYCURSOR;
	if (yych == 'D') goto yy97;
	if (yych != 'd') goto yy89;
yy97:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy98;
	if (yych != 'e') goto yy89;
yy98:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy89;
	++YYCURSOR;
#line 107 "_expander.re"
	{goto std;}
#line 471 "_expander.cc"
}
#line 110 "_expander.re"


nowiki:

#line 478 "_expander.cc"
{
	YYCTYPE yych;
	yych = *YYCURSOR;
	if (yych <= 0x0000) goto yy106;
	if (yych != '<') goto yy105;
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych == '/') goto yy108;
yy104:
#line 115 "_expander.re"
	{goto nowiki;}
#line 489 "_expander.cc"
yy105:
	yych = *++YYCURSOR;
	goto yy104;
yy106:
	++YYCURSOR;
#line 116 "_expander.re"
	{RET(0);}
#line 497 "_expander.cc"
yy108:
	yych = *++YYCURSOR;
	if (yych == 'N') goto yy110;
	if (yych == 'n') goto yy110;
yy109:
	YYCURSOR = YYMARKER;
	goto yy104;
yy110:
	yych = *++YYCURSOR;
	if (yych == 'O') goto yy111;
	if (yych != 'o') goto yy109;
yy111:
	yych = *++YYCURSOR;
	if (yych == 'W') goto yy112;
	if (yych != 'w') goto yy109;
yy112:
	yych = *++YYCURSOR;
	if (yych == 'I') goto yy113;
	if (yych != 'i') goto yy109;
yy113:
	yych = *++YYCURSOR;
	if (yych == 'K') goto yy114;
	if (yych != 'k') goto yy109;
yy114:
	yych = *++YYCURSOR;
	if (yych == 'I') goto yy115;
	if (yych != 'i') goto yy109;
yy115:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy109;
	++YYCURSOR;
#line 114 "_expander.re"
	{RET(5);}
#line 531 "_expander.cc"
}
#line 117 "_expander.re"


math:

#line 538 "_expander.cc"
{
	YYCTYPE yych;
	yych = *YYCURSOR;
	if (yych <= 0x0000) goto yy123;
	if (yych != '<') goto yy122;
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych == '/') goto yy125;
yy121:
#line 122 "_expander.re"
	{goto math;}
#line 549 "_expander.cc"
yy122:
	yych = *++YYCURSOR;
	goto yy121;
yy123:
	++YYCURSOR;
#line 123 "_expander.re"
	{RET(0);}
#line 557 "_expander.cc"
yy125:
	yych = *++YYCURSOR;
	if (yych == 'M') goto yy127;
	if (yych == 'm') goto yy127;
yy126:
	YYCURSOR = YYMARKER;
	goto yy121;
yy127:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy128;
	if (yych != 'a') goto yy126;
yy128:
	yych = *++YYCURSOR;
	if (yych == 'T') goto yy129;
	if (yych != 't') goto yy126;
yy129:
	yych = *++YYCURSOR;
	if (yych == 'H') goto yy130;
	if (yych != 'h') goto yy126;
yy130:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy126;
	++YYCURSOR;
#line 121 "_expander.re"
	{RET(5);}
#line 583 "_expander.cc"
}
#line 124 "_expander.re"


gallery:

#line 590 "_expander.cc"
{
	YYCTYPE yych;
	yych = *YYCURSOR;
	if (yych <= 0x0000) goto yy138;
	if (yych != '<') goto yy137;
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych == '/') goto yy140;
yy136:
#line 129 "_expander.re"
	{goto gallery;}
#line 601 "_expander.cc"
yy137:
	yych = *++YYCURSOR;
	goto yy136;
yy138:
	++YYCURSOR;
#line 130 "_expander.re"
	{RET(0);}
#line 609 "_expander.cc"
yy140:
	yych = *++YYCURSOR;
	if (yych == 'G') goto yy142;
	if (yych == 'g') goto yy142;
yy141:
	YYCURSOR = YYMARKER;
	goto yy136;
yy142:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy143;
	if (yych != 'a') goto yy141;
yy143:
	yych = *++YYCURSOR;
	if (yych == 'L') goto yy144;
	if (yych != 'l') goto yy141;
yy144:
	yych = *++YYCURSOR;
	if (yych == 'L') goto yy145;
	if (yych != 'l') goto yy141;
yy145:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy146;
	if (yych != 'e') goto yy141;
yy146:
	yych = *++YYCURSOR;
	if (yych == 'R') goto yy147;
	if (yych != 'r') goto yy141;
yy147:
	yych = *++YYCURSOR;
	if (yych == 'Y') goto yy148;
	if (yych != 'y') goto yy141;
yy148:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy141;
	++YYCURSOR;
#line 128 "_expander.re"
	{RET(5);}
#line 647 "_expander.cc"
}
#line 131 "_expander.re"


imagemap:

#line 654 "_expander.cc"
{
	YYCTYPE yych;
	yych = *YYCURSOR;
	if (yych <= 0x0000) goto yy156;
	if (yych != '<') goto yy155;
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych == '/') goto yy158;
yy154:
#line 136 "_expander.re"
	{goto imagemap;}
#line 665 "_expander.cc"
yy155:
	yych = *++YYCURSOR;
	goto yy154;
yy156:
	++YYCURSOR;
#line 137 "_expander.re"
	{RET(0);}
#line 673 "_expander.cc"
yy158:
	yych = *++YYCURSOR;
	if (yych == 'I') goto yy160;
	if (yych == 'i') goto yy160;
yy159:
	YYCURSOR = YYMARKER;
	goto yy154;
yy160:
	yych = *++YYCURSOR;
	if (yych == 'M') goto yy161;
	if (yych != 'm') goto yy159;
yy161:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy162;
	if (yych != 'a') goto yy159;
yy162:
	yych = *++YYCURSOR;
	if (yych == 'G') goto yy163;
	if (yych != 'g') goto yy159;
yy163:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy164;
	if (yych != 'e') goto yy159;
yy164:
	yych = *++YYCURSOR;
	if (yych == 'M') goto yy165;
	if (yych != 'm') goto yy159;
yy165:
	yych = *++YYCURSOR;
	if (yych == 'A') goto yy166;
	if (yych != 'a') goto yy159;
yy166:
	yych = *++YYCURSOR;
	if (yych == 'P') goto yy167;
	if (yych != 'p') goto yy159;
yy167:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy159;
	++YYCURSOR;
#line 135 "_expander.re"
	{RET(5);}
#line 715 "_expander.cc"
}
#line 138 "_expander.re"


pre:

#line 722 "_expander.cc"
{
	YYCTYPE yych;
	yych = *YYCURSOR;
	if (yych <= 0x0000) goto yy175;
	if (yych != '<') goto yy174;
	yych = *(YYMARKER = ++YYCURSOR);
	if (yych == '/') goto yy177;
yy173:
#line 143 "_expander.re"
	{goto pre;}
#line 733 "_expander.cc"
yy174:
	yych = *++YYCURSOR;
	goto yy173;
yy175:
	++YYCURSOR;
#line 144 "_expander.re"
	{RET(0);}
#line 741 "_expander.cc"
yy177:
	yych = *++YYCURSOR;
	if (yych == 'P') goto yy179;
	if (yych == 'p') goto yy179;
yy178:
	YYCURSOR = YYMARKER;
	goto yy173;
yy179:
	yych = *++YYCURSOR;
	if (yych == 'R') goto yy180;
	if (yych != 'r') goto yy178;
yy180:
	yych = *++YYCURSOR;
	if (yych == 'E') goto yy181;
	if (yych != 'e') goto yy178;
yy181:
	yych = *++YYCURSOR;
	if (yych != '>') goto yy178;
	++YYCURSOR;
#line 142 "_expander.re"
	{RET(5);}
#line 763 "_expander.cc"
}
#line 145 "_expander.re"

	
}


PyObject *py_scan(PyObject *self, PyObject *args) 
{
	PyObject *arg1;
	if (!PyArg_ParseTuple(args, "O:_expander.scan", &arg1)) {
		return 0;
	}
	PyUnicodeObject *unistr = (PyUnicodeObject*)PyUnicode_FromObject(arg1);
	if (unistr == NULL) {
		PyErr_SetString(PyExc_TypeError,
				"parameter cannot be converted to unicode in _expander.scan");
		return 0;
	}

	Py_UNICODE *start = unistr->str;
	Py_UNICODE *end = start+unistr->length;
	

	MacroScanner scanner (start, end);
	Py_BEGIN_ALLOW_THREADS
	while (scanner.scan()) {
	}
	Py_END_ALLOW_THREADS
	Py_XDECREF(unistr);
	
	// return PyList_New(0); // uncomment to see timings for scanning

	int size = scanner.tokens.size();
	PyObject *result = PyList_New(size);
	if (!result) {
		return 0;
	}
	
	for (int i=0; i<size; i++) {
		Token t = scanner.tokens[i];
		PyList_SET_ITEM(result, i, Py_BuildValue("iii", t.type, t.start, t.len));
	}
	
	return result;
}



static PyMethodDef module_functions[] = {
	{"scan", (PyCFunction)py_scan, METH_VARARGS, "scan(text)"},
	{0, 0},
};



extern "C" void init_expander(void);

DL_EXPORT(void) init_expander(void)
{
	/*PyObject *m =*/ Py_InitModule("_expander", module_functions);
}
