from enum import Enum

class TokenType(Enum):
    identifier = 1
    whitespace = 2
    bool_literal = 4
    int_literal=5
    float_literal=6
    colour_literal=7
    equals=8
    semicolon=9
    colon=10
    rel_op=11
    open_par=12
    close_par=13
    open_brac=14
    close_brac=15
    comma=16
    additive=17
    multiplicative=18
    sing_quotes=19
    double_quotes=20
    arrow=21
    err=99
    end=100
class Token:
    def __init__(self,t,l):
        self.type = t
        self.lexeme = l
class Lexer:
    def __init__(self):
        self.lexeme_list = ["_","=","additive","multiplicative","letter","number",",","hex","\"","\'","(",")","{","}","#",".",":",";",">","-","ws","rel_op","rel_op2","other"]
        self.states_list = list(range(20))
        self.cols =50
        self.rows=50
        self.states_accp = [1,2,4,11,12,13,14,16,17,19,20,21,22,23,24,25,26,27,28,30]

        self.Tx = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.initialise_Tx()
    def initialise_Tx(self):
        #identifiers [FINAL]
        self.Tx[0][self.lexeme_list.index("letter")]=1
        self.Tx[0][self.lexeme_list.index("_")]=1
        self.Tx[1][self.lexeme_list.index("letter")]=1
        self.Tx[1][self.lexeme_list.index("_")]=1
        self.Tx[1][self.lexeme_list.index("number")]=1
                
        self.Tx[0][self.lexeme_list.index("hex")]=1
        self.Tx[1][self.lexeme_list.index("hex")]=1
        
        #integers [FINAL]
        self.Tx[0][self.lexeme_list.index("number")]=2
        self.Tx[2][self.lexeme_list.index("number")]=2
        self.Tx[15][self.lexeme_list.index("number")]=2
        
        
        #decimal points
        self.Tx[0][self.lexeme_list.index(".")]=3
        self.Tx[2][self.lexeme_list.index(".")]=3
        self.Tx[15][self.lexeme_list.index(".")]=3
        
        #floating point numbers [FINAL]
        self.Tx[3][self.lexeme_list.index("number")]=4
        self.Tx[4][self.lexeme_list.index("number")]=4
        #pound sign for colour
        self.Tx[0][self.lexeme_list.index("#")]=5
        self.Tx[15][self.lexeme_list.index("#")] = 5  

        #hex num for colour [11 is FINAL] 
        for i in range(5,11):
            for r in range(self.cols):
                self.Tx[i][r]=23
                self.Tx[i][r]=23
        for i in range(5,12):
            
            self.Tx[i][self.lexeme_list.index("hex")]=i+1
            self.Tx[i][self.lexeme_list.index("number")]=i+1
        

        #equal sign
        self.Tx[0][self.lexeme_list.index("=")]=13
        
        #semicolon
        self.Tx[0][self.lexeme_list.index(";")]=14

        #whitespace
        
        self.Tx[0][self.lexeme_list.index("ws")]=0
        
        
        
        self.Tx[0][self.lexeme_list.index(":")]=16
        self.Tx[0][self.lexeme_list.index("rel_op")]=17
        self.Tx[0][self.lexeme_list.index(">")]=17
        self.Tx[17][self.lexeme_list.index("=")]=17
        self.Tx[17][self.lexeme_list.index("ws")]=-1
        self.Tx[17][self.lexeme_list.index("letter")]=-1
        self.Tx[0][self.lexeme_list.index("rel_op2")]=18
        for x in range(self.rows):
            self.Tx[18][x]=23
        
        self.Tx[18][self.lexeme_list.index("=")]=17

        self.Tx[0][self.lexeme_list.index("(")]=19
        self.Tx[0][self.lexeme_list.index(")")]=20
        self.Tx[0][self.lexeme_list.index("{")]=21
        self.Tx[0][self.lexeme_list.index("}")]=22
        self.Tx[0][self.lexeme_list.index(",")]=24
        self.Tx[0][self.lexeme_list.index("additive")]=25
        self.Tx[0][self.lexeme_list.index("multiplicative")]=26
        self.Tx[0][self.lexeme_list.index("\"")]=27
        self.Tx[0][self.lexeme_list.index("\'")]=28

        
        self.Tx[0][self.lexeme_list.index("-")]=29
        self.Tx[29][self.lexeme_list.index(">")]=30
        
        
        
        
        
        
        
    def accepting_state(self,state):
        try:
            self.states_accp.index(state)
            return True
        except:
            return False
    def return_token_by_final_state(self,state,lexeme):
        
        if state == 1:
            return Token(TokenType.identifier,lexeme)
        elif state == 2:
            return Token(TokenType.int_literal,lexeme)
        elif state == 4:
            return Token(TokenType.float_literal,lexeme)
        elif state==11 or state == 12:
            return Token(TokenType.colour_literal,lexeme)
        elif state == 13:
            return Token(TokenType.equals,lexeme)
        elif state == 14:
            return Token(TokenType.semicolon,lexeme)
        elif state ==  0:
            return Token(TokenType.whitespace,lexeme)
        elif state == 16:
            return Token(TokenType.colon,lexeme)
        elif state == 17:
            return Token(TokenType.rel_op,lexeme)
        elif state == 19:
            return Token(TokenType.open_par,lexeme)
        elif state == 20:
            return Token(TokenType.close_par,lexeme)
        elif state == 21:
            return Token(TokenType.open_brac,lexeme)
        elif state == 22:
            return Token(TokenType.close_brac,lexeme)
        elif state == 23:
            return Token(TokenType.err,lexeme)
        elif state ==24:
            return Token(TokenType.comma,lexeme)
        elif state ==25:
            return Token(TokenType.additive,lexeme)
        elif state ==26:
            return Token(TokenType.multiplicative,lexeme)
        elif state ==27:
            return Token(TokenType.double_quotes,lexeme)
        elif state ==28:
            return Token(TokenType.sing_quotes,lexeme)
        elif state ==30:
            return Token(TokenType.arrow,lexeme)
        else:
            return 'Default Result'
    def cat_char(self,char):
        if char in '->_:=.#;(){},\"\'':
            return char
        elif char in [" ","\t","\n"]:
            return "ws"
        elif char.lower() in 'abcdef':
            return "hex"
        elif char.isdigit():
            return "number"
        elif char.isalpha():
            return "letter"
        elif char in ["<"]:
            return "rel_op"
        elif char == "!":
            return "rel_op2"
        elif char in "+":
            return "additive"
        elif char in "*/":
            return "multiplicative"
        else:
            return "other"
        
    def end_of_input(self,src_program_str,src_program_idx):
        return (src_program_idx > len(src_program_str)-1)
    def next_char(self,src_program_str,src_program_idx):
        if not self.end_of_input(src_program_str,src_program_idx):
            return True,src_program_str[src_program_idx]
        else:
            return False, "."
    def next_token(self,src_program_str, src_program_idx):
        state=0 #intitial state is 0
        stack = []
        lexeme=""
        stack.append(-2)
        if self.end_of_input(src_program_str,src_program_idx):
            return Token(TokenType.end,"end"),"end"
        while state != -1:
            if self.accepting_state(state):
                stack.clear()
            stack.append(state)
            exists, character = self.next_char(src_program_str,src_program_idx)
            #print(character)
            lexeme += character
            if not exists:
                break
            src_program_idx+=1
            cat = self.cat_char(character)
            
            state = self.Tx[state][self.lexeme_list.index(cat)]
            
            
        lexeme = lexeme[:-1]
        syntax_error = False
        
        while len(stack) >0:
            if stack[-1]==-2:
                syntax_error=True
                
                break
            if not self.accepting_state(stack[-1]):
                stack.pop()
                lexeme = lexeme[:-1]
            else:
                state = stack.pop()
                break
        if syntax_error:
            return Token(TokenType.err,"error"),"error"
        if self.accepting_state(state):
            return self.return_token_by_final_state(state,lexeme),lexeme
        else:
            return Token(TokenType.err,"error"),"error"
    def gen_tokens(self,src_program_str):
        tokens_list=[]
        lines = 1
        program_idx = 0
        error = False
        while True:
            token, lexeme = self.next_token(src_program_str,program_idx)
            
            lines += lexeme.count("\n")
            if token.type == TokenType.end:
                break
            
            if token.type == TokenType.whitespace:
                program_idx += len(lexeme)
                continue
            if token.type == TokenType.err:
                print("error")
                error=True
                break
            tokens_list.append(token)
            program_idx += len(lexeme)
            
            if program_idx >= len(src_program_str):
                break
        if error:
            return [Token(TokenType.err,f"error at {lines}")]
        return tokens_list
        
        
# l=Lexer()
# toks = l.gen_tokens("""let m:colour = #7ff454;
#             let r:int = 16;
#             let f:float = 19.8;
#             if(sex!=4){
#             penis(4,#3efeee);
#             }
#             fun penis(r:int,c:colour){
#                 return fill(r-1,c);
#             }
#             __print("penis");""")
# for t in toks:
#     print(t.type,t.lexeme.replace(" ","").replace("\n","").replace("\t",""))

    