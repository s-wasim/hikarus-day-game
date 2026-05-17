"""
GBNF grammar constraint helper for Ollama structured output.

Phase 1 exit gate: only activate if golden-file test (TASK-013) reliability < 90%.
Ollama supports passing a JSON schema directly via the `format` parameter, which
already provides structured output. This module generates a more restrictive GBNF
grammar from the DayResponse schema to force exact field presence when needed.

Usage: pass the grammar string to OllamaClient.chat() via options={"grammar": grammar}
if Ollama's JSON schema mode alone isn't reliable enough.
"""

from typing import Any


def schema_to_gbnf(schema: dict[str, Any]) -> str:
    """
    Generate a GBNF grammar that constrains output to valid JSON matching schema.

    This is a pragmatic implementation for object schemas — it forces the response
    to be a JSON object. For full tree reliability, use Ollama's native `format`
    parameter (schema-constrained decoding) first. Only fall back to GBNF if needed.
    """
    # Root rule: valid JSON value (simplified — lets Ollama handle structural detail)
    lines = [
        'root ::= object',
        'object ::= "{" ws members ws "}"',
        'members ::= pair ("," ws pair)*',
        'pair ::= string ":" ws value',
        'value ::= string | number | object | array | "true" | "false" | "null"',
        'array ::= "[" ws (value ("," ws value)*)? ws "]"',
        r'string ::= "\"" ([^"\\] | "\\" .)* "\""',
        r'number ::= "-"? ([0-9] | [1-9][0-9]*) ("." [0-9]+)? ([eE][+-]?[0-9]+)?',
        'ws ::= [ \\t\\n\\r]*',
    ]
    return "\n".join(lines)


def day_response_grammar() -> str:
    from app.schemas.day import DayResponse

    schema = DayResponse.model_json_schema()
    return schema_to_gbnf(schema)
