from lexer import create_tokens, Token, TokenType
from parser import parse_tokens
from ATS_nodes import ProgramNode, FunctionNode, ReturnNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node, VariableNode, DeclarationNode, AssignNode, IfNode, ConditionalNode
from helpers import create_clause_label, create_end_label, create_false_branch_label, create_post_conditional_number

variables = {}
stack_index = -8

def generate(tree, variables_param):
    global variables
    variables = variables_param

    result = ''
    result += process_node(tree, result)
    result += '\n'
    return result


def process_node(node, result):
    if isinstance(node, ProgramNode):
        result += '    .globl	_main\n'
        result = process_node(node.left, result)
    elif isinstance(node, FunctionNode):
        funcName = node.name
        result += f"_{funcName}:\n"
        result += f"    push %rbp\n"
        result += f"    movq %rsp, %rbp\n"
        result += f"    movq $0, %rax\n"

        for statement in node.block_items:
            result = process_node(statement, result)

        result += f"    movq %rbp, %rsp\n"
        result += f"    pop %rbp\n"
        result += f"    ret"
    elif isinstance(node, DeclarationNode):
        global stack_index
        variables[node.name] = stack_index
        result += f"    push %rax\n"
        
        if (hasattr(node, 'left')):
            result = process_expression(node.left, result)
            result += f"    movq %rax, {stack_index}(%rbp)\n"
        stack_index = stack_index - 8
    else:
        result = process_expression(node, result)

    return result


def process_expression(node, result):
    if isinstance(node, ConstantNode):
        result += f"    movq ${node.value}, %rax\n"
    elif isinstance(node, ReturnNode):
        if node.name == TokenType.return_keyword:
            result = process_expression(node.left, result)
    elif isinstance(node, VariableNode):
        offset = variables[node.name]
        result += f"    movq {offset}(%rbp), %rax\n"
    elif isinstance(node, AssignNode):
        result = process_expression(node.left, result)
        offset = variables[node.name]
        result += f"    movq %rax, {offset}(%rbp)\n"
    elif isinstance(node, ConditionalNode):
        result = process_expression(node.condition, result)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        result += f"    je {false_branch_label}\n"
        result = process_expression(node.true_branch, result)
        post_conditional__label = create_post_conditional_number()
        result += f"    jmp {post_conditional__label}\n"
        result += f"{false_branch_label}:\n"
        result = process_expression(node.false_branch, result)
        result += f"{post_conditional__label}:\n"
    elif isinstance(node, IfNode):
        result = process_expression(node.condition, result)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        result += f"    je {false_branch_label}\n"
        result = process_expression(node.true_branch, result)
        post_conditional__label = create_post_conditional_number()
        result += f"    jmp {post_conditional__label}\n"
        result += f"{false_branch_label}:\n"

        if(node.false_branch != None):
            result = process_expression(node.false_branch, result)

        result += f"{post_conditional__label}:\n"
    elif isinstance(node, UnaryOperatorNode):
        if node.name == TokenType.negation:
            result = process_expression(node.left, result)
            result += f"    neg %rax\n"
        elif node.name == TokenType.bitwise_complement:
            result = process_expression(node.left, result)
            result += f"    not %rax\n"
        elif node.name == TokenType.logical_negation:
            result = process_expression(node.left, result)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    sete %al\n"
    elif isinstance(node, BinaryOperatorNode):

        if node.name == TokenType.logical_or:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(node.left, result)
            result += f"    cmp $0, %rax\n"
            result += f"    je {clauseLabel}\n"
            result += f"    movq $1, %rax\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(node.right, result)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"

        elif node.name == TokenType.logical_and:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(node.left, result)
            result += f"    cmp $0, %rax\n"
            result += f"    jne {clauseLabel}\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(node.right, result)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"
        else:
            result = process_expression(node.right, result)
            result += f"    push %rax\n"
            result = process_expression(node.left, result)
            result += f"    pop %rbx\n"

            if node.name == TokenType.negation:
                result += f"    sub %rbx, %rax\n"

            elif node.name == TokenType.addition:
                result += f"    add %rbx, %rax\n"

            elif node.name == TokenType.multiplication:
                result += f"    imul %rbx, %rax\n"

            elif node.name == TokenType.division:
                result += f"    movq $0, %rdx\n"
                result += f"    cqo\n"
                result += f"    idiv %rbx\n"

            elif node.name == TokenType.equal:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    sete %al\n"

            elif node.name == TokenType.not_equal:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setne %al\n"

            elif node.name == TokenType.greater_then:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setg %al\n"

            elif node.name == TokenType.greater_than_or_equal:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setge %al\n"

            elif node.name == TokenType.less_than:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setl %al\n"

            elif node.name == TokenType.less_than_equal:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setle %al\n"
            else:
                raise 'wrong node'
    return result
