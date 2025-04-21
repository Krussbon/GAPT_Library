class Node:
    def __init__(self):
        self.name = "Node"
class ProgramNode(Node):
    def __init__(self,stmts):
        self.name="ProgramNode"
        self.stmts = stmts
    def accept(self,visitor):
        visitor.visit_program(self)
class StatementNode(Node):
    def __init__(self):
        self.name = "StatenentNode"
class ExpressionNode(Node):
    def __init__(self,lhs,op,rhs):
        self.name = "ExpressionNode"
        self.lhs = lhs
        self.op = op
        self.rhs=rhs
    def accept(self,visitor):
        visitor.visit_expr_node(self)
class SimpleExpressionNode(Node):
    def __init__(self,lhs,op,rhs):
        self.name = "SimpleExpressionNode"
        self.lhs = lhs
        self.op = op
        self.rhs=rhs
    def accept(self,visitor):
        visitor.visit_simple_expr_node(self)
class TermNode(Node):
    def __init__(self,lhs,op,rhs):
        self.name = "TermNode"
        self.lhs = lhs
        self.op = op
        self.rhs=rhs
    def accept(self,visitor):
        visitor.visit_term_node(self)
class IntegerNode(Node):
    def __init__(self,v):
        self.name="IntegerNode"
        self.value = v
    def accept(self,visitor):
        visitor.visit_int_node(self)
class FloatNode(Node):
    def __init__(self,v):
        self.name="FloatNode"
        self.value = v
    def accept(self,visitor):
        visitor.visit_float_node(self)
class ColourNode(Node):
    def __init__(self,v):
        self.name="ColourNode"
        self.value = v
    def accept(self,visitor):
        visitor.visit_colour_node(self)
class BoolNode(Node):
    def __init__(self,value):
        self.name="BoolNode"
        self.value = value
    def accept(self,visitor):
        visitor.visit_bool_node(self)
class VariableNode(StatementNode):
    def __init__(self, lexeme):
        self.name = "variable_node"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_variable_node(self)
class IdentifierNode(Node):
    def __init__(self,value):
        self.name="IdentifierNode"
        self.value=value

    def accept(self,visitor):
        visitor.visit_identifier_node(self)
class DeclarationNode(Node):
    def __init__(self,name,type,expr):
        self.name="declaration_node"
        self.name = name
        self.type = type
        self.expr = expr
    def accept(self,visitor):
        visitor.visit_decl_node(self)
class AssignmentNode(StatementNode):
    def __init__(self,var_node,exp_node):
        self.name = "AssignmentNode"
        self.id = var_node
        self.expr=exp_node
    def accept(self,visitor):
        visitor.visit_assignment_node(self)
class FunctionDeclNode(Node):
    def __init__(self,name,params,return_type,block):
        self.name = "FunctionDeclNode"
        self.name = name
        
        self.params=params
        self.return_type=return_type
        self.block=block
    def accept(self,visitor):
        visitor.visit_func_decl_node(self)
class IfNode(StatementNode):
    def __init__(self,exp):
        self.name="IfNode"
        self.expr = exp
    def accept(self,visitor):
        visitor.visit_if_node(self)
class PadReadNode(StatementNode):
    def __init__(self,x,y):
        self.name="PadReadNode"
        self.x=x
        self.y=y
    def accept(self,visitor):
        visitor.visit_read_node(self)
class PrintNode(StatementNode):
    def __init__(self,value):
        self.name = "PrintNode"
        self.value =value
    def accept(self,visitor):
        visitor.visit_print_node(self)
class FunctionCallNode(Node):
    def __init__(self,fun_name,params,block):
        self.name="FunctionNode"
        self.fun_name= fun_name
        self.params=params
        self.block=block

    def accept(self,visitor):
        visitor.visit_function_call_node(self)
class HeightNode(Node):
    def __init__(self):
        self.name="HeightNode"
    def accept(self,visitor):
        visitor.visit_height_node(self)
class BinOpNode(Node):
    def __init__(self,value,left,right):
        self.name = "Bin_op"
        self.value=value
        self.left=left
        self.right=right
    def accept(self,visitor):
        visitor.visit_binop_node(self)
class IdentifierNode(Node):
    def __init__(self,value):
        self.name = "IdentifierNode"
        self.value=value
        
    def accept(self,visitor):
        visitor.visit_identifier(self)
class TypeCastBinOpNode(Node):
    def __init__(self,binop,type):
        self.name="TypecastBinOp"
        self.binop=binop
        self.type=type
    def accept(self,visitor):
        visitor.visit_typecast_node(self)
class WidthNode(Node):
    def __init__(self):
        self.name="WidthNode"
    def accept(self,visitor):
        visitor.visit_width_node(self)
class DelayNode(StatementNode):
    def __init__(self,value):
        self.name = "DelayNode"
        self.value =value
    def accept(self,visitor):
        visitor.visit_delay_node(self)
class BlockNode(Node):
    def __init__(self,stmts):
        self.name = "BlockNode"
        self.stmts = stmts
    
    def accept(self,visitor):
        visitor.visit_block_node(self)
class Visitor():
    def __init__(self):
        self.name="Visitor"
        self.node_count = 0
        self.tab_count = 0
    
    def inc_tab_count(self):
        self.tab_count += 1
    def dec_tab_count(self):
        self.tab_count -= 1
    def visit_program(self,program_node):
        self.tab_count += 1
        for stmt in program_node.stmts:
            print(stmt)
    def visit_identifier(self,iden):
        self.tab.count += 1
        print('\t'*self.tab_count, iden.value)
    def visit_decl_node(self,decl_node):
        self.tab_count += 1
        print('\t'*self.tab_count,"let ",decl_node.name,":",decl_node.type,"=",decl_node.expr)
        self.tab_count -= 1
    def visit_expr_node(self,expr_node):
        self.node_count+=1
        print('\t'*self.tab_count,expr_node.lhs,expr_node.op,expr_node.rhs)
    def visit_simple_expr_node(self,simple_expr_node):
        self.node_count+=1
        print('\t'*self.tab_count,simple_expr_node.lhs,simple_expr_node.op,simple_expr_node.rhs)
    def visit_term_node(self,term_node):
        self.node_count+=1
        print('\t'*self.tab_count,term_node.lhs,term_node.op,term_node.rhs)
    def visit_int_node(self,int_node):
        self.node_count += 1
        print('\t'*self.tab_count,"Int value=", int_node.value)
    def visit_float_node(self,float_node):
        self.node_count += 1
        print('\t'*self.tab_count,"Float value=", float_node.value)
    def visit_height_node(self,width):
        self.node_count +=1
        print('\t'*self.tab_count,"HEIGHT")
    def visit_width_node(self,width):
        self.node_count +=1
        print('\t'*self.tab_count,"WIDTH")
    def visit_colour_node(self,color_node):
        self.node_count += 1
        print('\t'*self.tab_count,"Color value=", color_node.value)
    def visit_bool_node(self,bool_node):
        self.node_count += 1
        print('\t'*self.tab_count,"Bool value=", bool_node.value)
    def visit_assignment_node(self,ass_node):
        self.node_count+=1
        print('\t'*self.tab_count, "Ass Node=>")
        self.inc_tab_count()
        ass_node.id.accept(self)
        ass_node.expr.accept(self)
        self.dec_tab_count()
    def visit_func_decl_node(self,fun_decl_node):
        self.node_count+=1
        print("\t"*self.tab_count,"Function ",fun_decl_node.name,list(f"{fun_decl_node.params[x]}" for x in range(len(fun_decl_node.params))),"=>",fun_decl_node.return_type)
        
    def visit_function_call_node(self,fun_call_node):
        self.node_count += 1
        print('\t'*self.tab_count,"function is called",fun_call_node.fun_name,fun_call_node.params)
    def visit_identifier_node(self,id_node):
        self.node_count+=1
        print('\t'*self.tab_count, "identifier Node=>",id_node)
    def visit_delay_node(self,delay_node):
        self.node_count+=1
        print('\t'*self.tab_count,"Delaying by",delay_node.value,"seconds")
    def visit_binop_node(self,binop_node):
        self.node_count+=1
        print('\t' * self.tab_count,  binop_node.left,binop_node.value,binop_node.right)
    def visit_typecast_node(self,typecast_node):
        self.node_count+=1
        print('\t' * self.tab_count,typecast_node.binop.left,typecast_node.binop.value,typecast_node.binop.right,"as",typecast_node.type)
    def visit_variable_node(self,var_node):
        self.node_count+=1
        print('\t' * self.tab_count, "Variable => ", var_node.lexeme)
    def visit_if_node(self,expr):
        self.node_count +=1
        print('\t'*self.tab_count,"IF", self.expr,"THEN")
    def visit_print_node(self,print_node):
        self.node_count+=1
        print('\t' * self.tab_count, "Printing ",print_node.value)
    def visit_read_node(self,read_node):
        self.node_count+=1
        print(f'\t'*self.tab_count,f"Reading at ({read_node.x},{read_node.y}).")
    def visit_block_node(self,block_node):
        self.node_count += 1
        print('\t'*self.tab_count,"New Block =>")
        self.inc_tab_count()
        for st in block_node.stmts:
            st.accept(self)
        self.dec_tab_count()