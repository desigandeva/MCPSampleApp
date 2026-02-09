from mcp.server.fastmcp import FastMCP
import math
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    x: float = Field(description="X value")
    y: float = Field(description="Y value")
    expression: str = Field(description="Expression used for the operation")

class OutputSchema(BaseModel):
    result: float = Field(description="Result of the operation")
    expression: str = Field(description="Expression used for the operation")

server = FastMCP("calculator", host="127.0.0.1", port=8000, stateless_http=True)

@server.tool(name="add", description="Add two numbers")
async def add(input: InputSchema) -> OutputSchema:
    result = input.x + input.y
    return OutputSchema(result= result, expression= f"{input.x} + {input.y} = {result}")

@server.tool(name="sub", description="Subtract two numbers")
async def sub(input: InputSchema) -> OutputSchema:
    result = input.x - input.y
    return OutputSchema(result= result, expression= f"{input.x} - {input.y} = {result}")

@server.tool(name="mul", description="Multiply two numbers")
async def mul(input: InputSchema) -> OutputSchema:
    result = input.x * input.y
    return OutputSchema(result= result, expression= f"{input.x} * {input.y} = {result}")

@server.tool(name="divd", description="Divide two numbers")
async def divd(input: InputSchema) -> OutputSchema:
    result = input.x / input.y
    return OutputSchema(result= result, expression= f"{input.x} / {input.y} = {result}")

@server.tool(name="sq", description="Square the number")
async def sq(input: InputSchema) -> OutputSchema:
    result = input.x * input.x
    return OutputSchema(result= result, expression= f"{input.x} ^ 2 = {result}")

@server.tool(name="sqrt", description="Square root the number")
async def sqrt(input: InputSchema) -> OutputSchema:
    result = math.sqrt(input.x)
    return OutputSchema(result= result, expression= f"sqrt({input.x}) = {result}")

@server.tool(name="exp", description="Exponent the number")
async def exp(input: InputSchema) -> OutputSchema:
    result = math.exp(input.x)
    return OutputSchema(result= result, expression= f"exp({input.x}) = {result}")

@server.tool(name="log_2", description="Logarithm of the number to base 2")
async def log_2(input: InputSchema) -> OutputSchema:
    result = math.log2(input.x)
    return OutputSchema(result= result, expression= f"log2({input.x}) = {result}")

@server.tool(name="log_10", description="Logarithm of the number to base 10")
async def log_10(input: InputSchema) -> OutputSchema:
    result = math.log10(input.x)
    return OutputSchema(result= result, expression= f"log10({input.x}) = {result}")

@server.tool(name="eval", description="Evaluate an expression")
async def eval(input: InputSchema) -> OutputSchema:
    result = eval(input.expression)
    return OutputSchema(result= result, expression= f"{input.expression} = {result}")

@server.resource(name="calculator_capabilities", description="Read-only documentation describing calculator capabilities and constraints")
async def calculator_capabilities() -> str:
    return """
Calculator MCP Server – Capabilities Reference

Available Tools:
- add(x, y): Add two numbers
- sub(x, y): Subtract y from x
- mul(x, y): Multiply two numbers
- divd(x, y): Divide x by y
- sq(x): Square a number
- sqrt(x): Square root of a number
- exp(x): Exponential function (e^x)
- log_2(x): Logarithm base 2
- log_10(x): Logarithm base 10
- eval(expression): Evaluate a mathematical expression

Constraints:
- Division by zero is not allowed.
- Square root and logarithms require positive input values.
- Expression evaluation must use valid mathematical syntax.
- All operations return structured results with explanations.

Usage Notes:
- Tools must be used for all calculations.
- This resource is read-only and intended for contextual reference.
"""


@server.prompt(name="calculator_workflow", description= "Guide the model to solve math problems using calculator tools")
async def calculator_workflow() -> OutputSchema:
    prompt = """
You are a calculator assistant operating within an MCP server.

Your role:
- Interpret the user's mathematical intent.
- Select the correct calculator tool.
- Execute the tool to compute results.
- Return the tool output verbatim.

Rules:
- Do NOT perform calculations yourself.
- Always use a calculator tool when a mathematical operation is requested.
- If multiple steps are required, execute them one at a time.
- If the request is ambiguous, ask for clarification.
- If the request is unsupported, politely explain the limitation.

Tool selection guide:
- add → addition of two numbers
- sub → subtraction of two numbers
- mul → multiplication of two numbers
- divd → division of two numbers
- sq → square of a number
- sqrt → square root of a number
- exp → exponential (e^x)
- log_2 → logarithm base 2
- log_10 → logarithm base 10
- eval → complex mathematical expressions

Input rules:
- Binary operations require x and y.
- Unary operations require x only.
- Expression evaluation requires a valid mathematical expression string.

Output rules:
- Always return the structured tool response.
- Include the expression field explaining the operation.

This prompt is intended to ensure consistent, safe, and correct calculator tool usage.
"""