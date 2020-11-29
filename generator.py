from lexer import create_tokens, Token, TokenType
from parser import parse_tokens
from ATS_nodes import ProgramNode, FunctionNode, ReturnNode, ConstantNode, UnaryOperatorNode, BinaryOperatorNode, Node, VariableNode, DeclarationNode, AssignNode, IfNode, ConditionalNode, CompoundNode, NullNode,  ForNode, ForDeclarationNode, WhileNode, DoWhileNode, BreakNode, ContinueNode, FunctionCallNode
from helpers import create_clause_label, create_end_label, create_false_branch_label, create_post_conditional_number, create_clause_while_start_number, create_clause_while_end_number, create_clause_for_start_number, create_clause_for_end_number, create_clause_for_post_expression_number
import copy


class Labels:
    def __init__(self, start_label, end_label, post_expression_label):
        self.start_label = start_label
        self.end_label = end_label
        self.post_expression_label = post_expression_label


class Context:
    def __init__(self, variables_data, labels, stack_index, current_scope, function_name):
        self.variables_data = variables_data
        self.labels = labels
        self.stack_index = stack_index
        self.current_scope = current_scope
        self.function_name = function_name


def generate(tree):
    context = Context({}, Labels(None, None, None), 0, None, None)

    result = ''
    result += process_node(tree, result, context)
    result += '\n'
    return result


def process_node(node, result, context):
    context
    if isinstance(node, ProgramNode):
        result += '    .globl	_main\n'
        for statement in node.statements:
            result = process_node(statement, result, context)
    elif isinstance(node, FunctionNode):
        result = process_function(node, result, context)
    else:
        result = process_expression(node, result, context)

    return result


def generate_declaration(node, result, context):

    if (context.current_scope == None):
        context.variables_data[node.name] = f"{context.stack_index}(%rbp)"
    else:
        context.current_scope[node.name] = f"{context.stack_index}(%rbp)"

    result += f"#Declaration start\n"
    result += f"    push %rax\n"

    if (hasattr(node, 'left')):
        result = process_expression(node.left, result, context)
        result += f"    movq %rax, {context.stack_index}(%rbp)\n\n"

    result += f"#Declaration end\n"

    context.stack_index = context.stack_index - 8
    return result, context


def process_function(node, result, context):

    new_context = copy.deepcopy(context)

    function_name = node.name

    new_context.function_name = function_name

    result += f"_{function_name}:\n"
    result += f"    push %rbp\n"
    result += f"    movq %rsp, %rbp\n"
    result += f"    movq $0, %rax\n\n"

    variables = node.variables
    if (len(variables) > 0):
        new_context.variables_data[variables[0]] = "%rdi"
    if (len(variables) > 1):
        new_context.variables_data[variables[1]] = "%rsi"
    if (len(variables) > 2):
        new_context.variables_data[variables[2]] = "%rdx"

    new_context.stack_index = -8

    for statement in node.statements:
        if isinstance(statement, DeclarationNode):
            result, new_context = generate_declaration(
                statement, result, new_context)

        else:
            result, new_context = generate_statement(
                statement, result,  new_context)

    result += f"\nend_label_{new_context.function_name}:\n"
    result += f"    movq %rbp, %rsp\n"
    result += f"    pop %rbp\n"
    result += f"    ret\n"

    return result


def generate_block(block, result, context):
    new_context = copy.deepcopy(context)
    new_context.current_scope = {}

    for statement in block.statements:
        if isinstance(statement,   DeclarationNode):
            result, new_context = generate_declaration(
                statement, result, new_context)
        else:
            new_variables_data = new_context.variables_data | new_context.current_scope
            new_context.variables_data = new_variables_data
            result, new_context = generate_statement(
                statement, result, new_context)

    bytes_to_deallocate = 8 * len(new_context.current_scope)
    result += f"    add ${bytes_to_deallocate}, %rsp\n"
    return result, context


def generate_statement(block, result, context):
    if (isinstance(block, NullNode)):
        return result, context
    if (isinstance(block, WhileNode)):
        while_start_label = create_clause_while_start_number()
        while_end_label = create_clause_while_end_number()

        previous_start_label = context.labels.start_label
        previous_end_label = context.labels.end_label
        previous_post_expression_label = context.labels.post_expression_label

        context.labels.start_label = while_start_label
        context.labels.end_label = while_end_label
        context.labels.post_expression_label = while_start_label

        result += f"\n#While condition start\n\n"

        result += f"{while_start_label}:\n"
        result = process_expression(block.condition, result, context)
        result += f"    cmp $0, %rax\n"
        result += f"    je {while_end_label}\n"
        result += f"\n#While condition end\n\n"

        result += f"\n#While body start\n\n"
        result, context = generate_statement(block.body, result, context)

        result += f"    jmp {while_start_label}\n"
        result += f"{while_end_label}:\n"
        result += f"\n#While body end\n\n"

        context.labels.start_label = previous_start_label
        context.labels.end_label = previous_end_label
        context.labels.post_expression_label = previous_post_expression_label

        return result, context
    if (isinstance(block, DoWhileNode)):
        while_start_label = create_clause_while_start_number()
        while_end_label = create_clause_while_end_number()

        previous_start_label = context.labels.start_label
        previous_end_label = context.labels.end_label
        previous_post_expression_label = context.labels.post_expression_label

        context.labels.start_label = while_start_label
        context.labels.end_label = while_end_label
        context.labels.post_expression_label = while_start_label

        result += f"{while_start_label}:\n"
        result, context = generate_statement(block.body, result, context)

        result = process_expression(block.condition, result, context)
        result += f"    cmp $0, %rax\n"
        result += f"    jne {while_start_label}\n"

        context.labels.start_label = previous_start_label
        context.labels.end_label = previous_end_label
        context.labels.post_expression_label = previous_post_expression_label

        return result, context

    if (isinstance(block, ForNode)):
        for_start_label = create_clause_for_start_number()
        for_end_label = create_clause_for_end_number()
        for_post_expression_label = create_clause_for_post_expression_number()

        previous_start_label = context.labels.start_label
        previous_end_label = context.labels.end_label
        previous_for_post_expression_label = context.labels.post_expression_label

        context.labels.start_label = for_start_label
        context.labels.end_label = for_end_label
        context.labels.post_expression_label = for_post_expression_label

        result += '\n'
        result = process_expression(block.initial_expression, result, context)
        result += f"\n{for_start_label}:\n"

        if (isinstance(block.condition, NullNode)):
            result += f"    movq $1, %rax\n"
        else:
            result = process_expression(block.condition, result, context)

        result += f"    cmp $0, %rax\n"
        result += f"    je {for_end_label}\n\n"

        result, context = generate_statement(block.body, result, context)
        result += '\n'

        result += f"{for_post_expression_label}: "
        result = process_expression(block.post_expression, result, context)
        result += f"    jmp {for_start_label}\n"

        result += f"{for_end_label}:\n\n"

        context.labels.start_label = previous_start_label
        context.labels.end_label = previous_end_label
        context.labels.post_expression_label = previous_for_post_expression_label

        return result, context

    if (isinstance(block, ForDeclarationNode)):
        new_context = copy.deepcopy(context)
        new_context.current_scope = {}

        for_start_label = create_clause_for_start_number()
        for_end_label = create_clause_for_end_number()
        for_post_expression_label = create_clause_for_post_expression_number()

        previous_start_label = new_context.labels.start_label
        previous_end_label = new_context.labels.end_label
        previous_for_post_expression_label = new_context.labels.post_expression_label

        new_context.labels.start_label = for_start_label
        new_context.labels.end_label = for_end_label
        new_context.labels.post_expression_label = for_post_expression_label

        result += '\n'
        result, new_context = generate_declaration(
            block.initial_expression, result, new_context)
        result += f"\n#For condition start\n"

        new_variables_data = new_context.variables_data | new_context.current_scope
        new_context.variables_data = new_variables_data

        result += f"\n{for_start_label}:\n"

        if (isinstance(block.condition, NullNode)):
            result += f"    movq $1, %rax\n"
        else:
            result = process_expression(block.condition, result, new_context)

        result += f"    cmp $0, %rax\n"
        result += f"    je {for_end_label}\n\n"
        result += f"#For condition end\n"

        result += f"\n#For body start\n"
        result, new_context = generate_statement(
            block.body, result, new_context)
        result += '\n'

        result += f"#For body end\n"

        result += f"\n#For post_expression start\n"
        result += f"{for_post_expression_label}:\n"
        result = process_expression(block.post_expression, result, new_context)
        result += f"    jmp {for_start_label}\n"
        result += f"#For post_expression end\n"

        result += f"{for_end_label}:\n\n"

        bytes_to_deallocate = 8 * len(new_context.current_scope)
        result += f"    add ${bytes_to_deallocate}, %rsp\n"

        new_context.labels.start_label = previous_start_label
        new_context.labels.end_label = previous_end_label
        new_context.labels.post_expression_label = previous_for_post_expression_label

        return result, context
    if isinstance(block, CompoundNode):
        result, context = generate_block(
            block, result, context)
    elif isinstance(block, IfNode):
        result += "\n#If condition  start\n\n"

        result = process_expression(block.condition, result, context)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        post_conditional__label = create_post_conditional_number()
        result += f"    je {false_branch_label}\n"
        result += "\n#If true branch  start\n\n"
        result, context = generate_statement(
            block.true_branch, result, context)
        result += f"    jmp {post_conditional__label}\n"
        result += f"{false_branch_label}:\n"

        if(block.false_branch != None):
            result += "\n#If false branch  start\n\n"
            result, context = generate_statement(
                block.false_branch, result, context)

        result += f"{post_conditional__label}:\n"
    else:
        result = process_expression(block, result,  context)

    return result, context


def process_expression(node, result, context):
    if isinstance(node, ConstantNode):
        result += f"    movq ${node.value}, %rax\n"
    elif (isinstance(node, FunctionCallNode)):
        args = node.args

        result += f"    push %rdi\n"
        result += f"    push %rsi\n"
        result += f"    push %rdx\n"

        result += f"\n# Align start part start\n\n"
        result += f"    mov %rsp, %rax\n"
        n = (8*(len(args)))
        result += f"    sub ${n}, %rax\n"
        result += f"    xor %rdx, %rdx\n"
        result += f"    mov $16, %rcx\n"
        result += f"    idiv %rcx\n"
        result += f"    sub %rdx, %rsp\n"
        result += f"    push %rdx\n"
        result += f"\n# Align start part end\n\n"

        if (len(args) > 0):
            result += f"\n# Put first argument\n\n"
            result = process_expression(args[0], result,  context)
            result += "    movq %rax, %rdi\n"
        if (len(args) > 1):
            result += f"\n# Put second argument\n\n"
            result = process_expression(args[1], result,  context)
            result += "    movq %rax, %rsi\n"
        if (len(args) > 2):
            result += f"\n# Put third argument\n\n"
            result = process_expression(args[2], result,  context)
            result += "    movq %rax, %rdx\n"
        # @see https://courses.cs.washington.edu/courses/cse378/10au/sections/Section1_recap.pdf for 3+ args

        result += f"    callq _{node.name}\n"

        result += f"\n# Align end part start\n\n"
        result += f"    pop %rdx\n"
        result += f"    add %rdx, %rsp\n"
        result += f"\n# Align end part end\n\n"

        result += f"    pop %rdx\n"
        result += f"    pop %rsi\n"
        result += f"    pop %rdi\n"

    elif isinstance(node, BreakNode):
        result += f"    jmp {context.labels.end_label}\n"
    elif isinstance(node, ContinueNode):
        result += f"    jmp {context.labels.post_expression_label}\n"
    elif isinstance(node, VariableNode):
        variable = context.variables_data[node.name]
        result += f"    movq {variable}, %rax\n"
    elif isinstance(node, ReturnNode):
        if node.name == TokenType.return_keyword:
            result = process_expression(
                node.left, result, context)
            result += f"    jmp end_label_{context.function_name}\n"
    elif isinstance(node, AssignNode):
        result += "\n#Assignment start\n\n"
        result = process_expression(node.left, result, context)
        variable = context.variables_data[node.name]
        result += f"    movq %rax, {variable}\n"

        result += "\n#Assignment end\n\n"

    elif isinstance(node, ConditionalNode):
        result += "\n#Conditional (a ? b : c) condition  start\n\n"

        result = process_expression(
            node.condition, result, context)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        post_conditional__label = create_post_conditional_number()

        result += f"    je {false_branch_label}\n"
        result += "\n#Conditional (a ? b : c) true branch  start\n\n"

        result = process_expression(
            node.true_branch, result, context)
        result += f"    jmp {post_conditional__label}\n"
        result += "\n#Conditional (a ? b : c) false branch  start\n\n"

        result += f"{false_branch_label}:\n"
        result = process_expression(
            node.false_branch, result, context)
        result += f"{post_conditional__label}:\n"
    elif isinstance(node, UnaryOperatorNode):
        if node.name == TokenType.negation:
            result = process_expression(
                node.left, result, context)
            result += f"    neg %rax\n"
        elif node.name == TokenType.bitwise_complement:
            result = process_expression(
                node.left, result, context)
            result += f"    not %rax\n"
        elif node.name == TokenType.logical_negation:
            result = process_expression(
                node.left, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    sete %al\n"
    elif (isinstance(node, NullNode)):
        return result
    elif isinstance(node, BinaryOperatorNode):

        if node.name == TokenType.logical_or:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(
                node.left, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    je {clauseLabel}\n"
            result += f"    movq $1, %rax\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(
                node.right, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"

        elif node.name == TokenType.logical_and:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(
                node.left, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    jne {clauseLabel}\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(
                node.right, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"

        else:
            result = process_expression(
                node.right, result, context)
            result += f"    push %rax\n"
            result = process_expression(
                node.left, result, context)
            result += f"    pop %rbx\n"

            if node.name == TokenType.negation:
                result += f"    sub %rbx, %rax\n"

            elif node.name == TokenType.addition:
                result += f"    add %rbx, %rax\n"

            elif node.name == TokenType.multiplication:
                result += f"    imul %rbx, %rax\n"

            elif node.name == TokenType.division:
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

            elif node.name == TokenType.mod:
                result += f"    cqo\n"
                result += f"    idiv %rbx\n"
                result += f"    mov %rdx, %rax\n"

            else:
                raise 'wrong node'
    else:
        raise 'wrong node'
    return result
