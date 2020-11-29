from lexer import create_tokens, Token, TokenType
from parser import parse_tokens
from ATS_nodes import ProgramNode, FunctionNode, ReturnNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node, VariableNode, DeclarationNode, AssignNode, IfNode, ConditionalNode, CompoundNode
from helpers import create_clause_label, create_end_label, create_false_branch_label, create_post_conditional_number

#


def generate(tree):
    variables_data = {}
    # variables_data.variables = variables_param

    result = ''
    result += process_node(tree, result, variables_data)
    result += '\n'
    return result


def process_node(node, result, variables_data):
    if isinstance(node, ProgramNode):
        result += '    .globl	_main\n'
        result = process_node(node.left, result, variables_data)
    elif isinstance(node, FunctionNode):
        result = process_function(node, result, variables_data)
    else:
        result = process_expression(node, result, variables_data)

    return result


def generate_declaration(node, result, var_map, stack_index, current_scope=None):
    if (current_scope == None):
        var_map[node.name] = stack_index
    else:
        current_scope[node.name] = stack_index

    result += f"    push %rax\n"

    if (hasattr(node, 'left')):
        result = process_expression(node.left, result, var_map)
        result += f"    movq %rax, {stack_index}(%rbp)\n"

    stack_index = stack_index - 8
    return result, var_map, stack_index, current_scope


def process_function(node, result, variables_data):
    funcName = node.name
    result += f"_{funcName}:\n"
    result += f"    push %rbp\n"
    result += f"    movq %rsp, %rbp\n"
    result += f"    movq $0, %rax\n"

    var_map = {}
    stack_index = -8

    for statement in node.statements:
        if isinstance(statement, DeclarationNode):
            result, var_map, stack_index, temp = generate_declaration(
                statement, result, var_map, stack_index)
        else:
            result, stack_index = generate_statement(
                statement, result,  var_map, stack_index)

    result += f"end_label:\n"
    result += f"    movq %rbp, %rsp\n"
    result += f"    pop %rbp\n"
    result += f"    ret"

    return result


def generate_block(block, result, var_map, stack_index):
    current_scope = {}

    for statement in block.statements:
        if isinstance(statement,   DeclarationNode):
            result, var_map, stack_index, current_scope = generate_declaration(
                statement, result, var_map, stack_index, current_scope)
        else:
            new_var_map =  var_map | current_scope
            result, stack_index = generate_statement(statement, result, new_var_map, stack_index)

    bytes_to_deallocate = 8 * len(current_scope)
    result += f"    add ${bytes_to_deallocate}, %rsp\n"
    stack_index = stack_index + 8 * len(current_scope)
    return result, stack_index


def generate_statement(block, result, var_map, stack_index, current_scope=None):
    if isinstance(block, CompoundNode):
        result, stack_index = generate_block(
            block, result, var_map, stack_index)
    elif isinstance(block, IfNode):
        result = process_expression(block.condition, result, var_map)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        result += f"    je {false_branch_label}\n"
        result, stack_index = generate_statement(block.true_branch, result, var_map, stack_index)
        post_conditional__label = create_post_conditional_number()
        result += f"    jmp {post_conditional__label}\n"
        result += f"{false_branch_label}:\n"

        if(block.false_branch != None):
            result, stack_index = generate_statement(
                block.false_branch, result, var_map, stack_index)

        result += f"{post_conditional__label}:\n"
    else:
        result = process_expression(block, result,  var_map)

    return result, stack_index


def process_expression(node, result, var_map):
    if isinstance(node, ConstantNode):
        result += f"    movq ${node.value}, %rax\n"
    elif isinstance(node, VariableNode):
        offset = var_map[node.name]
        result += f"    movq {offset}(%rbp), %rax\n"
    elif isinstance(node, ReturnNode):
        if node.name == TokenType.return_keyword:
            result = process_expression(node.left, result, var_map)
            result += "    jmp end_label\n"
    elif isinstance(node, AssignNode):
        result = process_expression(node.left, result, var_map)
        offset = var_map[node.name]
        result += f"    movq %rax, {offset}(%rbp)\n"
    elif isinstance(node, ConditionalNode):
        result = process_expression(node.condition, result, var_map)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        result += f"    je {false_branch_label}\n"
        result = process_expression(node.true_branch, result, var_map)
        post_conditional__label = create_post_conditional_number()
        result += f"    jmp {post_conditional__label}\n"
        result += f"{false_branch_label}:\n"
        result = process_expression(node.false_branch, result, var_map)
        result += f"{post_conditional__label}:\n"
    elif isinstance(node, UnaryOperatorNode):
        if node.name == TokenType.negation:
            result = process_expression(node.left, result, var_map)
            result += f"    neg %rax\n"
        elif node.name == TokenType.bitwise_complement:
            result = process_expression(node.left, result, var_map)
            result += f"    not %rax\n"
        elif node.name == TokenType.logical_negation:
            result = process_expression(node.left, result, var_map)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    sete %al\n"
    elif isinstance(node, BinaryOperatorNode):

        if node.name == TokenType.logical_or:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(node.left, result, var_map)
            result += f"    cmp $0, %rax\n"
            result += f"    je {clauseLabel}\n"
            result += f"    movq $1, %rax\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(node.right, result, var_map)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"

        elif node.name == TokenType.logical_and:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(node.left, result, var_map)
            result += f"    cmp $0, %rax\n"
            result += f"    jne {clauseLabel}\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(node.right, result, var_map)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"
        else:
            result = process_expression(node.right, result, var_map)
            result += f"    push %rax\n"
            result = process_expression(node.left, result, var_map)
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
