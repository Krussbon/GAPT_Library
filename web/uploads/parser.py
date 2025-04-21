import lexer
import ast
# program="""let x :bool = false;
# let x : int = __width;
# let col: colour = #0fffff;"""
# for token in lexer.Lexer().gen_tokens(program):
#     print(token.type,token.lexeme.replace(" ","").replace("\n","").replace("\t",""))
class Parser:
    def __init__(self,program):
        self.name="prsr"
        self.lexer = lexer.Lexer()
        self.index = -1
        self.src_program = program
        self.tokens = self.lexer.gen_tokens(self.src_program)
        self.crt = None
        self.nxt = ""
        self.ASTroot = ast.BlockNode
    def next_token_skip_ws(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.crt = self.tokens[self.index]
        else:
            self.crt = lexer.Token(lexer.TokenType.end,"END")
    def next_token(self):
        self.next_token_skip_ws()
        while self.crt.type == lexer.TokenType.whitespace:
            self.next_token_skip_ws()
    def parse_literal(self):
        if self.crt.type == lexer.TokenType.int_literal:
            value = self.crt.lexeme
            self.next_token()
            return ast.IntegerNode(value)
        if self.crt.type == lexer.TokenType.float_literal:
            value = self.crt.lexeme
            self.next_token()
            return ast.FloatNode(value)
        if self.crt.type == lexer.TokenType.colour_literal:
            value = self.crt.lexeme
            self.next_token()
            return ast.ColourNode(value)
        if self.crt.type == lexer.TokenType.identifier and (self.crt.lexeme == 'true' or self.crt.lexeme == 'false' ):
            value = self.crt.lexeme
            self.next_token()
            return ast.BoolNode(value)
    def parse_identifier(self):
        if self.crt.type == lexer.TokenType.identifier and self.crt.lexeme not in ["let","true","false","fun"]:
            value=self.crt.lexeme
            return ast.IdentifierNode(value)
    def parse_factor(self):
        try:
            return self.parse_literal()
        except Exception as e:
            print("err", e)
        try:
            return self.parse_identifier()
        except Exception as e:
            print("err", e)
        try:
            return self.parse_function_call()
        except Exception as e:
            print("err", e)
    def parse_function_call(self):
        
        function_name = self.crt.lexeme
        self.next_token()
        if self.crt.type != lexer.TokenType.open_par:
            raise SyntaxError(f"Expected '('")
        self.next_token()
        params = []
        while self.crt.type != lexer.TokenType.close_par:
            params.append(self.parse_expression())
            if self.crt.type == lexer.TokenType.comma:
                self.next_token()
        self.next_token()
        return ast.FunctionCallNode(function_name,params)

    def parse_expression(self):
        expr = self.parse_simple_expr()
        self.next_token()
        op = None
        while self.crt.type == lexer.TokenType.rel_op:
            op=  self.crt.lexeme
            self.next_token()
            rhs = self.parse_simple_expr()
            expr = ast.Expression(expr,op,rhs)
        return expr
    def parse_simple_expr(self):
        simp_expr = self.parse_term()
        self.next_token()
        op = None
        while self.crt.type == lexer.TokenType.additive:
            op = self.crt.lexeme
            self.next_token()
            rhs = self.parse_term()
            simp_expr=ast.SimpleExpressionNode(simp_expr,op,rhs)
        
        return simp_expr
    def parse_term(self):
        term = self.parse_factor()
        self.next_token()
        op = None
        while self.crt.type == lexer.TokenType.multiplicative:
            op = self.crt.lexeme
            self.next_token()
            rhs = self.parse_factor()
            term = ast.TermNode(term,op,rhs)
        return term
    def parse_print_stat(self):
        self.next_token()
        print_text=self.parse_expression()
        return ast.PrintNode(print_text)
    

    def parse_assignment(self):
        lhs = ast.IdentifierNode(self.crt.lexeme)
        if self.crt.type == lexer.TokenType.identifier:
            print("parsing assignment")
            lhs = ast.VariableNode(self.crt.lexeme)
            self.next_token()
        if self.crt.type == lexer.TokenType.equals:
            self.next_token()
        rhs = self.parse_expression()
        return ast.AssignmentNode(lhs,rhs)
    def parse_fun_decl(self):
        
        self.next_token()
        params = []
        if self.crt.type == lexer.TokenType.identifier:
            fun_name = self.crt.lexeme
            self.next_token()
        if self.crt.type == lexer.TokenType.open_par:
            self.next_token()
        if self.crt.type == lexer.TokenType.identifier:
            params.append(self.crt.lexeme)
            self.next_token()
        if self.crt.type == lexer.TokenType.close_par:
            self.next_token()
        else:
            while self.crt.type != lexer.TokenType.close_par:
                if self.crt.type == lexer.TokenType.identifier:
                    params.append(self.crt.lexeme)
                self.next_token()
            self.next_token()
        if self.crt.type == lexer.TokenType.arrow:
            self.next_token()
        
        if self.crt.type==lexer.TokenType.identifier:
            return_type = self.crt.lexeme
        
        
        self.next_token()
        print(self.crt.lexeme)
        block = self.parse_block()
        
        return ast.FunctionDeclNode(fun_name,params,return_type,block)
    def parse_decl(self):
        var_type=None
        if self.crt.type == lexer.TokenType.identifier and self.crt.lexeme=='let':
            self.next_token()
        if self.crt.type == lexer.TokenType.identifier:
            
            name = ast.VariableNode(self.crt.lexeme)
            self.next_token()
        if  self.crt.type==lexer.TokenType.colon:
            self.next_token()
        if self.crt.type==lexer.TokenType.identifier:
            var_type = self.crt.lexeme
            self.next_token()
        if  self.crt.type==lexer.TokenType.equals:
            self.next_token()
        expr = self.parse_expression()
        
        return ast.DeclarationNode(name,var_type,expr)
    def parse_height(self):
        if self.crt.lexeme == "__height":
            return ast.HeightNode()
    def parse_width(self):
        if self.crt.lexeme == "__width":
            return ast.WidthNode()
    def parse_read(self):
        self.next_token()
        x = self.crt.lexeme()
        self.next_token()
        self.next_token()
        y=self.crt.lexeme()
        return ast.PadReadNode(x,y)


    
    def parse_statement(self):
        print(self.crt.lexeme)
        if self.crt.type==lexer.TokenType.identifier:
            if self.crt.lexeme=='let':
                return self.parse_decl()
            elif self.crt.lexeme=='__print':
                return self.parse_print_stat()
            elif self.crt.lexeme=='__height':
                return self.parse_height()
            elif self.crt.lexeme=='__width':
                return self.parse_width()
            elif self.crt.lexeme=='__read':
                return self.parse_read()
            elif self.crt.lexeme=='fun':
                return self.parse_fun_decl()
            else:
                return self.parse_assignment()
            
    def parse_block(self):
        print(self.crt.lexeme)
        if self.crt.type != lexer.TokenType.open_brac:
            raise SyntaxError("Expected {")
        self.next_token()
        statements=[]

        while self.crt.type != lexer.TokenType.close_brac:
            statements.append(self.parse_assignment())
        if self.crt.type != lexer.TokenType.close_brac:
            raise SyntaxError("Expected }")
        return ast.BlockNode(statements)
    def parse_program(self):
        stmts=[]
        if self.crt is None:
            self.next_token()
        while self.crt is not None and  self.crt.type != lexer.TokenType.end:
            
            stmt = self.parse_statement()
            stmts.append(stmt)
            self.next_token()
        return ast.ProgramNode(stmts)
            

            
    def parse(self):
        self.ASTroot = self.parse_program()
        return self.ASTroot
program = """fun ballsack(letter,minecradt,zobbi)->colour{
              x=2
              }"""
# lexr = lexer.Lexer()
# for x in  lexr.gen_tokens(program):
#     print(x.type,x.lexeme)
prsr = Parser(program)

res = prsr.parse()

print_visitor = ast.Visitor()
prsr.ASTroot.accept(print_visitor)